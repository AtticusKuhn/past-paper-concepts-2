# System Patterns: Past Paper Concept Analyzer

## Architecture

The system follows a pipeline architecture: Download -> Process (LLM) -> Extract -> Store (Graph DB) -> Visualize.

## Data Flow

1.  **Input:** PDF files (solutions papers).
2.  **Download Module:** Fetches PDFs from CL website using user credentials.
3.  **Processing Module:** Sends PDF content/images to a Vision LLM API.
4.  **Extraction Module:** Parses LLM response to identify concepts and associated metadata (question context). Handles concept canonicalization (strategy TBD).
5.  **Storage Module:** Connects to a graph database (backend TBD, e.g., Neo4j, NetworkX). Creates/updates `Paper`, `Question`, and `Concept` nodes and `PART_OF`, `MENTIONS` relationships based on extracted data.
6.  **Query/Visualization Module:** Executes queries against the graph database (e.g., Cypher for Neo4j, NetworkX methods) and uses libraries (e.g., Matplotlib, pyvis) to generate outputs.

## Key Technical Decisions

*   **Graph Database:** Chosen to model the many-to-many relationships between concepts and questions effectively and support relationship-based queries and visualizations.
*   **Vision LLM:** Required for processing PDF content which includes text, layout, and potentially diagrams.
*   **CLI Interface:** Chosen for simplicity and ease of integration into scripting workflows.

## Component Relationships

