# Tech Context: Past Paper Concept Analyzer

## Core Technology

*   **Language:** Python 3.x

## Key Libraries & Frameworks

*   **LLM Interaction:** Library for interacting with a chosen Vision LLM API (e.g., `openai` for GPT models).
*   **PDF Processing:** Potentially libraries like `PyMuPDF` or similar if pre-processing is needed before sending to the LLM, or rely solely on the Vision LLM's capabilities.
*   **Graph Database Interaction:**
    *   If **Neo4j:** `neo4j` (official Python driver).
    *   If **NetworkX:** `networkx` library.
*   **Data Visualization:**
    *   `matplotlib`, `seaborn` (for static plots like frequency trends).
    *   `networkx` (for graph structure analysis and basic plotting).
    *   `pyvis` (for interactive NetworkX graphs rendered as HTML).
*   **Configuration:** `python-dotenv` (for loading `.env` files).
*   **CLI Framework:** Potentially `argparse` (standard library) or `click`, `typer`.
*   **HTTP Requests:** `requests` (for downloading PDFs).

## Development Setup

This project is being developed using `Nix` on `NixOs`. Any development tools should
be placed inside `shell.nix`.

## Technical Constraints

*   Requires internet access for downloading papers and interacting with LLM APIs.
*   Dependent on the CL website structure and authentication method remaining stable.
*   LLM API costs and rate limits.
*   Performance may depend on the number of papers processed and the size of the resulting graph database.

## Tool Usage Patterns

*   Use `.env` file for sensitive credentials (CL auth cookie, LLM API key).
*   CLI commands for distinct actions: download, process, query, visualize.
