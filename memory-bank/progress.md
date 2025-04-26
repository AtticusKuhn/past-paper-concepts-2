# Progress: Past Paper Concept Analyzer

## Current Status

*   **Phase:** Initial Implementation / Prototyping.
*   **Overall Progress:** ~25% (Core structure, CLI, config, download, graph store, basic visualization implemented; LLM is placeholder).
*   **Last Commit:** `3ee5278` (feat: Bootstrap project with core modules and CLI)

## What Works

*   **Project Setup:** Directory structure, Nix environment (`shell.nix`), `.gitignore`.
*   **Configuration:** Loading `.env` (`config.py`), creating `data/` and `downloads/` directories.
*   **CLI:** `argparse` interface (`cli.py`) with `download`, `process`, `visualize` commands. Handles arguments, calls relevant modules, provides basic feedback and error handling.
*   **Downloading:** `download` command successfully fetches PDFs from CL website using `requests` and cookie authentication (`downloader.py`). Includes basic validation and error handling for 403/404.
*   **Graph Storage:** `NetworkX` graph (`graph_store.py`) can be loaded from and saved to `GraphML`. Functions exist to add/update `Paper`, `Question`, `Concept` nodes and `PART_OF`, `MENTIONS` relationships. Basic concept name normalization implemented.
*   **Processing (Stubbed):** `process` command takes PDF path, gets metadata (via args or filename parsing), calls placeholder LLM extractor, adds dummy data to graph, saves graph.
*   **Visualization:** `visualize` command loads the graph and generates an interactive HTML file using `pyvis`, with basic node styling by type.

## What's Left to Build

*   **LLM Integration (Core):** Implement actual Vision LLM calls in `llm_extractor.py`.
    *   PDF-to-image conversion (if needed).
    *   API interaction logic (e.g., `openai`).
    *   Prompt engineering for structured JSON output.
    *   Response parsing and error handling.
*   **Concept Canonicalization:** Implement a more robust strategy.
*   **Metadata Handling:** Finalize approach for `tripos_part` and potentially `course_module`.
*   **Querying/Analysis Features:** Add CLI commands or functions to query the graph (e.g., concept frequency, co-occurrence).
*   **Advanced Visualization:** Implement other visualization types (e.g., static plots with Matplotlib/Seaborn).
*   **Testing:** Develop unit and integration tests.
*   **Robustness:** Improve logging, input validation, edge case handling.
*   **Documentation:** User guide, more detailed setup/usage instructions.
*   **Packaging:** (Optional) Package the tool for easier distribution.

## Known Issues

*   LLM extraction (`llm_extractor.py`) is currently a placeholder returning dummy data.
*   Concept canonicalization (`graph_store.py`) is very basic (lowercase/whitespace).
*   `tripos_part` metadata is not reliably captured (defaults to "Unknown" unless specified in `process` args).
*   Limited testing coverage.

## Evolution of Project Decisions

*   **Initial:** Considered SQLite database.
*   **Current:** Decided on a Graph Database architecture.
*   **Initial:** Vague idea of LLM use.
*   **Current:** Specified using a Vision LLM on solutions PDFs.
*   **Initial:** Unspecified authentication method.
*   **Current:** Implemented using a `.env` file for the CL authentication cookie.
*   **Initial:** Considered Neo4j vs NetworkX.
*   **Current:** Selected and implemented **NetworkX** with GraphML persistence for the prototype phase.
