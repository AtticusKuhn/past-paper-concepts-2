# Tech Context: Past Paper Concept Analyzer

## Core Technology

*   **Language:** Python 3.x

## Key Libraries & Frameworks

*   **LLM Interaction:** `openai` (Included in environment, placeholder logic exists in `llm_extractor.py`).
*   **PDF Processing:** Currently relying on Vision LLM. *Dependencies like `pdf2image` and `Pillow` (via `python3Packages.pillow`) might be needed if image conversion is chosen for LLM input.*
*   **Graph Database Interaction:** `networkx` (Used for graph manipulation and storage via GraphML in `graph_store.py`).
*   **Data Visualization:**
    *   `pyvis` (Used in `cli.py` for interactive HTML graph output).
    *   `matplotlib`, `seaborn` (Included in environment, planned for static plots).
*   **Configuration:** `python-dotenv` (Used in `config.py` for loading `.env` files).
*   **CLI Framework:** `argparse` (Standard library, used in `cli.py`).
*   **HTTP Requests:** `requests` (Used in `downloader.py` for downloading PDFs).
*   **Code Quality:** `black`, `ruff` (Included in environment for formatting and linting).

## Development Setup

*   **Environment:** Managed via `Nix` using `shell.nix` on NixOS. `PYTHONPATH` is set in `shellHook`.
*   **Dependencies:** Defined in `shell.nix`.
*   **Version Control:** Git.

## Technical Constraints

*   Requires internet access for downloading papers and interacting with LLM APIs.
*   Dependent on the CL website structure and authentication method remaining stable.
*   LLM API costs and rate limits (specifically OpenAI's if used).
*   Performance may depend on the number of papers processed and the size of the resulting NetworkX graph in memory and the GraphML file size. NetworkX operations might become slow for very large graphs.

## Tool Usage Patterns

*   Use `.env` file for sensitive credentials (CL auth cookie, OPENAI_API_KEY). Copy from `.env.example`.
*   Run via `python main.py <command> [options]` from the project root directory.
*   CLI commands implemented: `download`, `process`, `visualize`.
*   Graph data persisted to `data/concept_graph.graphml` by default (configurable via `GRAPH_DATA_PATH` in `.env`).
*   Downloaded PDFs stored in `downloads/`.
