import networkx as nx
import os
import sys
import re
from . import config


# Basic normalization: lowercase and remove extra whitespace
def normalize_concept_name(name: str) -> str:
    """Applies basic normalization to a concept name."""
    if not isinstance(name, str):
        return "invalid_concept_name"
    name = name.lower().strip()
    name = re.sub(r"\s+", " ", name)  # Replace multiple whitespace with single space
    return name


def generate_node_id(prefix: str, identifier: str) -> str:
    """Generates a safe node ID for NetworkX."""
    # Replace potentially problematic characters for IDs (e.g., spaces, slashes)
    safe_identifier = re.sub(r"\W+", "_", identifier)
    return f"{prefix}_{safe_identifier}"


def load_graph(path: str = config.GRAPH_DATA_PATH) -> nx.DiGraph:
    """Loads the concept graph from a GraphML file."""
    if os.path.exists(path):
        print(f"Loading graph from {path}")
        try:
            # Using DiGraph for directed relationships like PART_OF, MENTIONS
            # Specify node_type=str if needed, though usually inferred
            graph = nx.read_graphml(path)
            print(
                f"Graph loaded successfully with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges."
            )
            return graph
        except Exception as e:
            print(
                f"Error loading graph from {path}: {e}. Creating a new graph.",
                file=sys.stderr,
            )
            return nx.DiGraph()  # Return a new directed graph on error
    else:
        print(f"Graph file not found at {path}. Creating a new graph.")
        return nx.DiGraph()


def save_graph(graph: nx.DiGraph, path: str = config.GRAPH_DATA_PATH):
    """Saves the concept graph to a GraphML file."""
    print(
        f"Saving graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges to {path}"
    )
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        nx.write_graphml(
            graph, path, infer_numeric_types=True
        )  # infer_numeric_types helps preserve types
        print("Graph saved successfully.")
    except Exception as e:
        print(f"Error saving graph to {path}: {e}", file=sys.stderr)


def add_paper(graph: nx.DiGraph, paper_code: str, year: int, tripos_part: str) -> str:
    """Adds or updates a Paper node. Returns the node ID."""
    node_id = generate_node_id("paper", paper_code)
    # Add node with attributes, updating if it already exists
    graph.add_node(
        node_id, type="Paper", code=paper_code, year=year, tripos_part=tripos_part
    )
    # print(f"Added/Updated Paper node: {node_id}") # Less verbose logging
    return node_id


def add_question(
    graph: nx.DiGraph,
    paper_node_id: str,
    question_number: str,
    course_module: str = None,
) -> str:
    """Adds a Question node and links it to a Paper node. Returns the node ID."""
    if paper_node_id not in graph:
        print(f"Error: Paper node '{paper_node_id}' does not exist.", file=sys.stderr)
        return None
    paper_code = graph.nodes[paper_node_id]["code"]
    # Ensure question_number is treated as a string for ID generation
    q_num_str = str(question_number)
    node_id = generate_node_id("q", f"{paper_code}_{q_num_str}")

    graph.add_node(
        node_id,
        type="Question",
        number=q_num_str,  # Store as string
        course=course_module if course_module else "Unknown",  # Default if None
    )
    # Add relationship: (Question)-[:PART_OF]->(Paper)
    # Check if edge already exists to avoid duplicates if run multiple times
    if not graph.has_edge(node_id, paper_node_id):
        graph.add_edge(node_id, paper_node_id, type="PART_OF")
        # print(f"Added Question node: {node_id} (Part of {paper_node_id})")
    # else:
    # print(f"Question node {node_id} already exists and is linked to {paper_node_id}.")

    return node_id


def add_concept(graph: nx.DiGraph, concept_name: str, definition: str = None) -> str:
    """
    Adds or updates a Concept node using a normalized name.
    Returns the node ID of the concept.
    """
    original_name = concept_name
    canonical_name = normalize_concept_name(concept_name)
    if not canonical_name:  # Handle empty or invalid names
        print(
            f"Warning: Skipping invalid concept name '{original_name}'", file=sys.stderr
        )
        return None

    node_id = generate_node_id("concept", canonical_name)

    # If node exists, update definition if a new one is provided and better?
    # For now, just add/overwrite attributes.
    graph.add_node(
        node_id,
        type="Concept",
        name=canonical_name,  # Store the canonical name
        definition=(
            definition
            if definition
            else graph.nodes.get(node_id, {}).get(
                "definition", "No definition provided"
            )
        ),  # Keep old def if new one is None
        # Store original names if needed for disambiguation later?
        # original_names=set(graph.nodes.get(node_id, {}).get('original_names', [])) | {original_name}
    )
    # print(f"Added/Updated Concept node: {node_id} (Name: {canonical_name})")
    return node_id


def link_question_to_concept(
    graph: nx.DiGraph, question_node_id: str, concept_node_id: str
):
    """Adds a MENTIONS relationship from a Question to a Concept."""
    if question_node_id is None or concept_node_id is None:
        print(
            f"Warning: Skipping link due to invalid node ID (Q: {question_node_id}, C: {concept_node_id})",
            file=sys.stderr,
        )
        return
    if question_node_id not in graph:
        print(
            f"Warning: Question node '{question_node_id}' not found. Cannot link concept.",
            file=sys.stderr,
        )
        return
    if concept_node_id not in graph:
        print(
            f"Warning: Concept node '{concept_node_id}' not found. Cannot link from question.",
            file=sys.stderr,
        )
        return

    # Check if edge already exists
    if not graph.has_edge(question_node_id, concept_node_id):
        graph.add_edge(question_node_id, concept_node_id, type="MENTIONS")
        # print(f"Linked Question {question_node_id} -> MENTIONS -> Concept {concept_node_id}")
    # else:
    # print(f"Link already exists: Question {question_node_id} -> MENTIONS -> Concept {concept_node_id}")


# Example usage (for direct testing):
# if __name__ == '__main__':
#     g = load_graph() # Load existing or create new
#
#     # Add some data idempotently
#     paper_id = add_paper(g, paper_code="2022-p06", year=2022, tripos_part="IB")
#     q1_id = add_question(g, paper_id, question_number="q01", course_module="Example Course")
#     concept_a_id = add_concept(g, concept_name="Dummy Concept A ", definition="A placeholder concept.") # Test normalization
#     concept_b_id = add_concept(g, concept_name="Dummy Concept B", definition="Another placeholder.")
#
#     if q1_id and concept_a_id: link_question_to_concept(g, q1_id, concept_a_id)
#     if q1_id and concept_b_id: link_question_to_concept(g, q1_id, concept_b_id)
#
#     # Add another concept mentioned elsewhere
#     concept_c_id = add_concept(g, "Shared Concept C")
#     if q1_id and concept_c_id: link_question_to_concept(g, q1_id, concept_c_id)
#
#     # Simulate another question mentioning concept C
#     q2_id = add_question(g, paper_id, question_number="q02")
#     if q2_id and concept_c_id: link_question_to_concept(g, q2_id, concept_c_id)
#
#     # Test adding duplicate concept name
#     concept_a_dup_id = add_concept(g, concept_name="dummy concept a", definition="Updated definition?")
#     if q2_id and concept_a_dup_id: link_question_to_concept(g, q2_id, concept_a_dup_id)
#
#     print("\n--- Graph State ---")
#     print(f"Nodes ({g.number_of_nodes()}):")
#     # for node, data in g.nodes(data=True):
#     #     print(f"  {node}: {data}")
#     print(f"Edges ({g.number_of_edges()}):")
#     # for u, v, data in g.edges(data=True):
#     #     print(f"  {u} -[{data.get('type', 'RELATED')}]-> {v}")
#     print("-------------------")
#
#     save_graph(g)
