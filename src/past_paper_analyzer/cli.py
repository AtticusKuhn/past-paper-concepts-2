import argparse
import os
import sys
import re
from . import config, downloader, llm_extractor, graph_store, batch_parser


def parse_filename(filename: str) -> dict | None:
    """
    Parses filenames like 'YYYY-pXX-qYY-solutions.pdf' or 'YYYY-PaperX-QY-Solutions.pdf'.
    Returns a dictionary with 'year', 'paper_code', 'question_num' or None if parsing fails.
    """
    # Pattern for YYYY-pXX-qYY... format
    match1 = re.match(
        r"(\d{4})-(p\d{1,2})-(q\d{1,2})-solutions\.pdf", filename, re.IGNORECASE
    )
    if match1:
        return {
            "year": int(match1.group(1)),
            "paper_code": match1.group(2).lower(),  # e.g., p06
            "question_num": match1.group(3).lower(),  # e.g., q01
        }

    # Pattern for YYYY-PaperX-QY... format (less common for solutions?)
    match2 = re.match(
        r"(\d{4})-Paper(\d+)-Q(\d+)-Solutions\.pdf", filename, re.IGNORECASE
    )
    if match2:
        # Convert to consistent format
        return {
            "year": int(match2.group(1)),
            "paper_code": f"p{int(match2.group(2)):02d}",  # e.g., p06
            "question_num": f"q{int(match2.group(3)):02d}",  # e.g., q01
        }

    print(
        f"Warning: Could not parse metadata from filename: {filename}", file=sys.stderr
    )
    print("Expected format like: YYYY-pXX-qYY-solutions.pdf", file=sys.stderr)
    return None


def handle_download(args):
    """Handles the 'download' command for single or batch downloads."""
    print("--- Download Command ---")

    if args.batch_file:
        if args.year or args.paper or args.question:
            print("Warning: --year, --paper, --question arguments are ignored when --batch-file is used.", file=sys.stderr)
        
        print(f"Processing batch download file: {args.batch_file}")
        paper_specs = batch_parser.load_batch_file(args.batch_file)
        
        if not paper_specs:
            print("No valid paper specifications found in the batch file. Nothing to download.", file=sys.stderr)
            sys.exit(1)

        download_count = 0
        fail_count = 0
        print(f"Found {len(paper_specs)} paper(s) to download from batch file.")

        for spec in paper_specs:
            year = spec['year']
            paper_code = spec['paper_code'] # Should be 'pXX'
            course_hint = spec['course_hint'] # Optional

            print(f"Attempting to download: Year={year}, Paper={paper_code}" + (f" (Hint: {course_hint})" if course_hint else ""))
            
            # --- IMPORTANT ---
            # The current downloader.download_pdf expects (year, paper_code, question_number).
            # For downloading a full paper's solutions PDF, the concept of a single 'question_number'
            # might not apply directly to the URL structure or the PDF itself.
            # We are using "all" as a placeholder for question_number.
            # `downloader.py` will need to be adapted to handle this,
            # or a new function like `download_paper_solutions(year, paper_code, course_hint)`
            # should be created in `downloader.py`.
            # The `course_hint` should also be utilized by the downloader or stored
            # with the downloaded file's metadata for later processing.
            # For now, we'll just pass it along if the downloader can take it.
            # Placeholder for question_number, assuming solutions are per-paper.
            question_placeholder = "all" # This needs to be reconciled with downloader.py's capabilities

            downloaded_path = downloader.download_pdf(year, paper_code, question_placeholder)
            # If downloader is updated to use course_hint:
            # downloaded_path = downloader.download_pdf(year, paper_code, question_placeholder, course_hint=course_hint)


            if downloaded_path:
                print(f"  Success: {downloaded_path}")
                download_count += 1
            else:
                print(f"  Failed to download Year={year}, Paper={paper_code}.")
                fail_count += 1
        
        print(f"Batch download summary: {download_count} successful, {fail_count} failed.")
        if fail_count > 0:
            sys.exit(1) # Exit with error if any downloads failed

    elif args.year and args.paper and args.question:
        # Original single file download logic
        print(f"Requesting single download: Year={args.year}, Paper={args.paper}, Question={args.question}")

        if not re.match(r"p\d{1,2}", args.paper, re.IGNORECASE):
            print(f"Error: Invalid paper format '{args.paper}'. Expected 'pXX'.", file=sys.stderr)
            return
        if not re.match(r"q\d{1,2}", args.question, re.IGNORECASE):
            print(f"Error: Invalid question format '{args.question}'. Expected 'qYY'.", file=sys.stderr)
            return

        paper_code_normalized = f"p{int(args.paper[1:]):02d}"
        question_num_normalized = f"q{int(args.question[1:]):02d}"

        downloaded_path = downloader.download_pdf(args.year, paper_code_normalized, question_num_normalized)

        if downloaded_path:
            print(f"Download successful: {downloaded_path}")
        else:
            print("Download failed.")
            sys.exit(1)
    else:
        print("Error: For download, you must specify EITHER --batch-file OR (--year, --paper, AND --question).", file=sys.stderr)
        parser.print_help(sys.stderr) # Accessing parser might be tricky here, print usage manually
        sys.exit(1)
        
    print("--- End Download ---")


def handle_process(args):
    """Handles the 'process' command."""
    print("--- Process Command ---")
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
        if not re.match(r"p\d{1,2}", args.paper, re.IGNORECASE) or not re.match(
            r"q\d{1,2}", args.question, re.IGNORECASE
        ):
            print(
                "Error: Invalid --paper or --question format provided.", file=sys.stderr
            )
            sys.exit(1)
        metadata = {
            "year": args.year,
            "paper_code": f"p{int(args.paper[1:]):02d}",
            "question_num": f"q{int(args.question[1:]):02d}",
            "tripos_part": (
                args.tripos_part if args.tripos_part else "Unknown"
            ),  # Use provided or default
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
            metadata["tripos_part"] = (
                args.tripos_part if args.tripos_part else "Unknown"
            )  # Use provided or default
            print(f"Parsed metadata: {metadata}")
        else:
            print(
                "Error: Could not determine paper metadata. Use --year, --paper, --question arguments or ensure filename format is YYYY-pXX-qYY-solutions.pdf.",
                file=sys.stderr,
            )
            sys.exit(1)

    # --- LLM Extraction ---
    print("Starting LLM concept extraction...")
    # TODO: Pass course_hint to llm_extractor if available from batch download metadata
    concepts_data = llm_extractor.extract_concepts_from_pdf(pdf_path)
    if not concepts_data:
        print("Error: No concepts extracted or LLM call failed.", file=sys.stderr)
        sys.exit(1)
    print(f"LLM extraction returned {len(concepts_data)} concepts.")

    # --- Update Graph ---
    print("Loading concept graph...")
    graph = graph_store.load_graph()
    print("Updating graph with extracted data...")

    full_paper_code = f"{metadata['year']}-{metadata['paper_code']}"

    paper_id = graph_store.add_paper(
        graph,
        paper_code=full_paper_code,
        year=metadata["year"],
        tripos_part=metadata["tripos_part"],
    )

    # TODO: If processing a full paper PDF, need to iterate through questions within it.
    # The current model assumes one PDF = one question's solution, which might be incorrect
    # for solutions PDFs that cover an entire paper.
    # The `metadata['question_num']` might come from filename parsing (e.g. YYYY-pXX-qYY-solutions.pdf)
    # or be a specific question if the PDF is indeed for a single question.
    # If the PDF is for a whole paper (e.g. YYYY-pXX-solutions.pdf), then `question_num`
    # needs to be derived during LLM extraction for each concept.

    question_id = graph_store.add_question(
        graph,
        paper_node_id=paper_id,
        question_number=metadata["question_num"], # This needs careful handling if PDF is multi-question
        course_module=args.course, # This could also come from batch file's course_hint
    )

    concepts_added_count = 0
    links_added_count = 0
    for concept_info in concepts_data:
        concept_name = concept_info.get("concept_name")
        if not concept_name:
            print(
                f"Warning: Skipping concept with missing name: {concept_info}",
                file=sys.stderr,
            )
            continue

        concept_id = graph_store.add_concept(
            graph, concept_name=concept_name, definition=concept_info.get("definition")
        )
        if concept_id: # True if concept was added or already existed
            # Check if link already exists before incrementing (graph_store.link_question_to_concept might do this)
            # For now, assume link_question_to_concept handles duplicates gracefully or we count all attempts.
            graph_store.link_question_to_concept(graph, question_id, concept_id)
            links_added_count += 1
        
        # How to count concepts_added_count? Only if new node created?
        # graph_store.add_concept returns node_id. We can check if it was new.
        # For simplicity, let's assume it's fine for now.
        # A more accurate count would be:
        # if graph.nodes[concept_id].get('is_new', False): concepts_added_count +=1
        # (requires add_concept to mark new nodes)

    # A simple count of unique concepts processed in this run:
    unique_concept_names_processed = {c.get("concept_name") for c in concepts_data if c.get("concept_name")}
    concepts_added_count = len(unique_concept_names_processed)


    print(
        f"Processed {concepts_added_count} unique concepts and created/verified {links_added_count} links for question {metadata.get('question_num', 'N/A')} in paper {full_paper_code}."
    )

    graph_store.save_graph(graph)
    print(
        f"Successfully processed '{os.path.basename(pdf_path)}' and saved updated graph."
    )
    print("--- End Process ---")


def handle_visualize(args):
    """Handles the 'visualize' command."""
    print("--- Visualize Command ---")
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

    try:
        from pyvis.network import Network

        net = Network(
            notebook=False,
            directed=True,
            height="800px",
            width="100%",
            bgcolor="#222222",
            font_color="white",
        )
        net.from_nx(graph)

        for node in net.nodes:
            node_id = node["id"]
            if node_id in graph.nodes:
                node_data = graph.nodes[node_id]
                node_type = node_data.get("type", "Unknown")
                color_map = {
                    "Paper": "#FFD700", "Question": "#ADD8E6", "Concept": "#90EE90"
                }
                size_map = {"Paper": 25, "Question": 15, "Concept": 10}
                
                node["color"] = color_map.get(node_type, "#FFFFFF") # Default white
                node["size"] = size_map.get(node_type, 10)
                
                title_parts = [f"ID: {node_id}"]
                for k, v in node_data.items():
                    title_parts.append(f"{k}: {v}")
                node["title"] = "\n".join(title_parts)
        
        net.show_buttons(filter_=["physics"])
        net.save_graph(output_file)
        print("Interactive graph visualization saved successfully.")

    except ImportError:
        print(
            "Error: 'pyvis' library not found. Please install it (should be in shell.nix environment).",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during visualization: {e}", file=sys.stderr)
        sys.exit(1)

    print("--- End Visualize ---")

# Store the global parser instance to access it from handle_download if needed for help text
parser = None

def main():
    global parser # Allow assignment to global parser

    if not config.INITIAL_CONFIG_OK:
        print(
            "Initial configuration check failed. Please check your .env file and directory permissions.",
            file=sys.stderr,
        )

    parser = argparse.ArgumentParser(
        description="Past Paper Concept Analyzer: Extract and visualize concepts from Cambridge CS Tripos solutions.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # --- Download Command ---
    parser_download = subparsers.add_parser(
        "download", 
        help="Download solutions PDF(s). Use EITHER --batch-file OR (--year, --paper, --question)."
    )
    # Arguments for single download (mutually exclusive with batch)
    parser_download.add_argument("--year", type=int, help="Exam year (e.g., 2022) for single download.")
    parser_download.add_argument("--paper", type=str, help="Paper code (e.g., p06) for single download.")
    parser_download.add_argument(
        "--question", type=str, help="Question number (e.g., q01) for single download."
    )
    # Argument for batch download
    parser_download.add_argument(
        "--batch-file", type=str, help="Path to a batch file specifying multiple papers to download."
    )
    parser_download.set_defaults(func=handle_download)

    # --- Process Command ---
    parser_process = subparsers.add_parser(
        "process",
        help="Process a downloaded PDF: extract concepts via LLM and update the graph.",
    )
    parser_process.add_argument(
        "pdf_path",
        type=str,
        help="Path to the downloaded solutions PDF file (e.g., downloads/2022-p06-q01-solutions.pdf)",
    )
    parser_process.add_argument(
        "--year",
        type=int,
        help="Optional: Specify exam year (overrides filename parsing)",
    )
    parser_process.add_argument(
        "--paper",
        type=str,
        help="Optional: Specify paper code (e.g., p06) (overrides filename parsing)",
    )
    parser_process.add_argument(
        "--question",
        type=str,
        help="Optional: Specify question number (e.g., q01) (overrides filename parsing). Important if PDF contains multiple questions.",
    )
    parser_process.add_argument(
        "--tripos-part",
        type=str,
        choices=["IA", "IB", "II", "Unknown"],
        default="Unknown",
        help="Specify Tripos Part (IA, IB, II)",
    )
    parser_process.add_argument(
        "--course", type=str, help="Optional: Specify associated course module name (can also come from batch file hint)"
    )
    parser_process.set_defaults(func=handle_process)

    # --- Visualize Command ---
    parser_visualize = subparsers.add_parser(
        "visualize",
        help="Generate an interactive HTML visualization of the concept graph.",
    )
    parser_visualize.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file path for the visualization (default: graph_visualization.html)",
    )
    parser_visualize.set_defaults(func=handle_visualize)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {type(e).__name__}: {e}", file=sys.stderr)
        # import traceback # Uncomment for full traceback during development
        # traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
