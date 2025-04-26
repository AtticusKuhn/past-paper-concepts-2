import argparse
import os
import sys
import re
from . import config, downloader, llm_extractor, graph_store

def parse_filename(filename: str) -> dict | None:
    """
    Parses filenames like 'YYYY-pXX-qYY-solutions.pdf' or 'YYYY-PaperX-QY-Solutions.pdf'.
    Returns a dictionary with 'year', 'paper_code', 'question_num' or None if parsing fails.
    """
    # Pattern for YYYY-pXX-qYY... format
    match1 = re.match(r"(\d{4})-(p\d{1,2})-(q\d{1,2})-solutions\.pdf", filename, re.IGNORECASE)
    if match1:
        return {
            "year": int(match1.group(1)),
            "paper_code": match1.group(2).lower(), # e.g., p06
            "question_num": match1.group(3).lower() # e.g., q01
        }

    # Pattern for YYYY-PaperX-QY... format (less common for solutions?)
    match2 = re.match(r"(\d{4})-Paper(\d+)-Q(\d+)-Solutions\.pdf", filename, re.IGNORECASE)
    if match2:
         # Convert to consistent format
        return {
            "year": int(match2.group(1)),
            "paper_code": f"p{int(match2.group(2)):02d}", # e.g., p06
            "question_num": f"q{int(match2.group(3)):02d}" # e.g., q01
        }

    print(f"Warning: Could not parse metadata from filename: {filename}", file=sys.stderr)
    print("Expected format like: YYYY-pXX-qYY-solutions.pdf", file=sys.stderr)
    return None


def handle_download(args):
    """Handles the 'download' command."""
    print(f"--- Download Command ---")
    print(f"Requesting: Year={args.year}, Paper={args.paper}, Question={args.question}")

    # Basic validation of paper/question format
    if not re.match(r"p\d{1,2}", args.paper, re.IGNORECASE):
        print(f"Error: Invalid paper format '{args.paper}'. Expected 'pXX'.", file=sys.stderr)
        return
    if not re.match(r"q\d{1,2}", args.question, re.IGNORECASE):
        print(f"Error: Invalid question format '{args.question}'. Expected 'qYY'.", file=sys.stderr)
        return

    # Normalize paper/question codes (e.g., p6 -> p06, q1 -> q01) - optional but good
    paper_code = f"p{int(args.paper[1:]):02d}"
    question_num = f"q{int(args.question[1:]):02d}"

    downloaded_path = downloader.download_pdf(args.year, paper_code, question_num)

    if downloaded_path:
        print(f"Download successful: {downloaded_path}")
    else:
        print("Download failed.")
        sys.exit(1) # Exit with error code if download fails
    print(f"--- End Download ---")


def handle_process(args):
    """Handles the 'process' command."""
    print(f"--- Process Command ---")
    pdf_path = args.pdf_path
    print(f"Processing PDF: {pdf_path}")
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}", file=sys.stderr)
        sys.exit(1)

    # --- Get Metadata ---
    metadata = None
    # Prioritize command-line args if provided
    if args.year and args.paper and args.question:
         # Basic validation
         if not re.match(r"p\d{1,2}", args.paper, re.IGNORECASE) or \
            not re.match(r"q\d{1,2}", args.question, re.IGNORECASE):
             print("Error: Invalid --paper or --question format provided.", file=sys.stderr)
             sys.exit(1)
         metadata = {
             "year": args.year,
             "paper_code": f"p{int(args.paper[1:]):02d}",
             "question_num": f"q{int(args.question[1:]):02d}",
             "tripos_part": args.tripos_part if args.tripos_part else "Unknown" # Use provided or default
         }
         print("Using metadata from command-line arguments.")
    else:
        # Fallback to filename parsing
        print("Attempting to parse metadata from filename...")
        filename = os.path.basename(pdf_path)
        parsed_meta = parse_filename(filename)
        if parsed_meta:
            metadata = parsed_meta
            # Still need tripos part - require it if not parsing?
            metadata["tripos_part"] = args.tripos_part if args.tripos_part else "Unknown" # Use provided or default
            print(f"Parsed metadata: {metadata}")
        else:
            print("Error: Could not determine paper metadata. Use --year, --paper, --question arguments or ensure filename format is YYYY-pXX-qYY-solutions.pdf.", file=sys.stderr)
            sys.exit(1)

    # --- LLM Extraction ---
    print("Starting LLM concept extraction...")
    concepts_data = llm_extractor.extract_concepts_from_pdf(pdf_path)
    if not concepts_data:
        print("Error: No concepts extracted or LLM call failed.", file=sys.stderr)
        # Decide if this is a fatal error - maybe allow proceeding with 0 concepts?
        # For now, let's exit.
        sys.exit(1)
    print(f"LLM extraction returned {len(concepts_data)} concepts.")

    # --- Update Graph ---
    print("Loading concept graph...")
    graph = graph_store.load_graph()
    print("Updating graph with extracted data...")

    # Combine year and paper code for a unique paper identifier in the graph
    full_paper_code = f"{metadata['year']}-{metadata['paper_code']}"

    paper_id = graph_store.add_paper(graph,
                                     paper_code=full_paper_code,
                                     year=metadata['year'],
                                     tripos_part=metadata['tripos_part'])

    question_id = graph_store.add_question(graph,
                                           paper_node_id=paper_id,
                                           question_number=metadata['question_num'],
                                           course_module=args.course) # Add optional course module

    concepts_added_count = 0
    links_added_count = 0
    for concept_info in concepts_data:
        concept_name = concept_info.get("concept_name")
        if not concept_name:
            print(f"Warning: Skipping concept with missing name: {concept_info}", file=sys.stderr)
            continue

        concept_id = graph_store.add_concept(graph,
                                             concept_name=concept_name,
                                             definition=concept_info.get("definition"))
        if concept_id:
            concepts_added_count += 1 # Count concepts successfully added/updated
            # Link the question to this concept
            graph_store.link_question_to_concept(graph, question_id, concept_id)
            links_added_count += 1 # Count successful links

    print(f"Added/Updated {concepts_added_count} concepts and created {links_added_count} links for question {metadata['question_num']}.")

    # --- Save Graph ---
    graph_store.save_graph(graph)
    print(f"Successfully processed '{os.path.basename(pdf_path)}' and saved updated graph.")
    print(f"--- End Process ---")


def handle_visualize(args):
    """Handles the 'visualize' command."""
    print(f"--- Visualize Command ---")
    print("Loading graph...")
    graph = graph_store.load_graph()
    if not graph:
        print("Graph is empty or could not be loaded.", file=sys.stderr)
        sys.exit(1)
    if graph.number_of_nodes() == 0:
        print("Graph contains no nodes. Nothing to visualize.", file=sys.stderr)
        sys.exit(1)

    output_file = args.output if args.output else "graph_visualization.html"
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    print(f"Generating interactive visualization to: {output_file}")

    # Basic pyvis visualization
    try:
        from pyvis.network import Network
        # Set height and width for better display
        net = Network(notebook=False, directed=True, height="800px", width="100%", bgcolor="#222222", font_color="white")
        net.from_nx(graph)

        # Optional: Customize appearance based on node type?
        for node in net.nodes:
            node_id = node["id"]
            if node_id in graph.nodes:
                node_type = graph.nodes[node_id].get("type", "Unknown")
                if node_type == 'Paper':
                    node["color"] = "#FFD700" # Gold
                    node["size"] = 25
                elif node_type == 'Question':
                    node["color"] = "#ADD8E6" # Light Blue
                    node["size"] = 15
                elif node_type == 'Concept':
                    node["color"] = "#90EE90" # Light Green
                    node["size"] = 10
                # Add title for hover info
                node["title"] = f"ID: {node_id}\n" + "\n".join(f"{k}: {v}" for k, v in graph.nodes[node_id].items())


        # Optional: Add physics controls
        net.show_buttons(filter_=['physics'])
        net.save_graph(output_file)
        print(f"Interactive graph visualization saved successfully.")

    except ImportError:
        print("Error: 'pyvis' library not found. Please install it (should be in shell.nix environment).", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during visualization: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"--- End Visualize ---")


def main():
    # Check config on startup
    if not config.INITIAL_CONFIG_OK:
        print("Initial configuration check failed. Please check your .env file and directory permissions.", file=sys.stderr)
        # Decide if we should exit immediately
        # sys.exit(1) # Uncomment to make config errors fatal

    parser = argparse.ArgumentParser(
        description="Past Paper Concept Analyzer: Extract and visualize concepts from Cambridge CS Tripos solutions.",
        formatter_class=argparse.RawTextHelpFormatter # Preserve newline formatting in help
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # --- Download Command ---
    parser_download = subparsers.add_parser("download", help="Download a specific solutions PDF from the CL website.")
    parser_download.add_argument("year", type=int, help="Exam year (e.g., 2022)")
    parser_download.add_argument("paper", type=str, help="Paper code (e.g., p06)")
    parser_download.add_argument("question", type=str, help="Question number (e.g., q01)")
    parser_download.set_defaults(func=handle_download)

    # --- Process Command ---
    parser_process = subparsers.add_parser("process", help="Process a downloaded PDF: extract concepts via LLM and update the graph.")
    parser_process.add_argument("pdf_path", type=str, help="Path to the downloaded solutions PDF file (e.g., downloads/2022-p06-q01-solutions.pdf)")
    parser_process.add_argument("--year", type=int, help="Optional: Specify exam year (overrides filename parsing)")
    parser_process.add_argument("--paper", type=str, help="Optional: Specify paper code (e.g., p06) (overrides filename parsing)")
    parser_process.add_argument("--question", type=str, help="Optional: Specify question number (e.g., q01) (overrides filename parsing)")
    parser_process.add_argument("--tripos-part", type=str, choices=['IA', 'IB', 'II', 'Unknown'], default='Unknown', help="Specify Tripos Part (IA, IB, II)")
    parser_process.add_argument("--course", type=str, help="Optional: Specify associated course module name")
    parser_process.set_defaults(func=handle_process)

    # --- Visualize Command ---
    parser_visualize = subparsers.add_parser("visualize", help="Generate an interactive HTML visualization of the concept graph.")
    parser_visualize.add_argument("-o", "--output", type=str, help="Output file path for the visualization (default: graph_visualization.html)")
    # Add arguments later to specify visualization type (e.g., --type co-occurrence)
    parser_visualize.set_defaults(func=handle_visualize)

    # --- Add other commands later: query, stats, etc. ---

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Execute the function associated with the chosen command
    try:
        args.func(args)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        # Optionally add more detailed traceback logging here for debugging
        # import traceback
        # traceback.print_exc()
        sys.exit(1)

