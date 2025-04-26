# Active Context: Past Paper Concept Analyzer

## Current Focus

*   **Phase:** Initial Implementation / Prototyping.
*   **Activity:** Setting up project structure, implementing core module stubs (download, LLM, graph store), basic CLI, and configuration loading based on initial design. Testing basic commands.

## Recent Changes

*   **Commit:** `3ee5278`
*   **Selected Graph Backend:** Chose **NetworkX** with GraphML file persistence for the initial prototype due to simplicity.
*   **Project Structure:** Created initial directory layout (`src/past_paper_analyzer`, `main.py`, `data/`, `downloads/`).
*   **Core Modules Implemented:**
    *   `config.py`: Loads settings from `.env`, checks config, creates directories.
    *   `downloader.py`: Function to download PDFs using `requests` and CL cookie, with basic error handling and validation.
    *   `llm_extractor.py`: Placeholder function for concept extraction (returns dummy data, checks for API key). Includes commented-out structure for actual implementation.
    *   `graph_store.py`: Functions to load/save NetworkX graph (GraphML), add Paper, Question, Concept nodes and PART_OF, MENTIONS relationships. Includes basic concept name normalization (lowercase, whitespace) and safe node ID generation.
    *   `cli.py`: CLI using `argparse` with `download`, `process`, and `visualize` commands. Includes filename parsing fallback and option to provide metadata via args for `process`. Basic `pyvis` visualization implemented. Added input validation and error handling.
    *   `main.py`: Entry point script, ensures `src` is in `PYTHONPATH`.
*   **Environment:** Updated `shell.nix` with required Python packages (`requests`, `networkx`, `python-dotenv`, `openai`, `pyvis`, `matplotlib`, `black`, `ruff`). Created `.env.example`. Added `data/` and `downloads/` to `.gitignore`.

## Next Steps

1.  **Implement LLM Interaction:** Replace the placeholder in `llm_extractor.py` with actual calls to a Vision LLM API (e.g., OpenAI GPT-4o). This involves:
    *   Choosing the specific API call/library usage (e.g., `openai.chat.completions.create`).
    *   Developing the initial prompt strategy (system prompt, user prompt with JSON format request).
    *   Handling PDF data input to the Vision LLM (e.g., converting pages to images and encoding). Requires adding libraries like `pdf2image` and `Pillow`.
    *   Parsing the LLM's JSON response robustly.
    *   Adding error handling for API calls and response parsing.
2.  **Refine `process` Command & Metadata:**
    *   Determine a reliable way to get `tripos_part` (e.g., require as argument, infer from paper code patterns if possible).
    *   Consider how to handle multi-question PDFs if they exist, or confirm solutions are always single-question.
3.  **Improve Concept Canonicalization:** Move beyond simple lowercasing in `graph_store.py`. Explore strategies mentioned in README (e.g., more sophisticated LLM prompting, maybe simple synonym mapping).
4.  **Testing:** Add basic tests for core functions (downloading a known public file, graph operations, CLI argument parsing).

## Active Decisions & Considerations

*   **LLM Prompting:** This is the next major hurdle. How to reliably get structured concept data (name, definition, context) from the PDF? Output format needs to be consistent (JSON preferred). How to handle variations in PDF layout?
*   **PDF to LLM Input:** Decide on the best method: send PDF bytes directly (if API supports), or convert to images (page-by-page)? Image conversion adds dependencies (`pdf2image`, `poppler-utils`).
*   **Error Handling:** Continue improving error handling and user feedback in all modules.
*   **Graph Schema Refinement:** Review if the current node properties and relationships in `graph_store.py` are sufficient as real data comes in (e.g., storing `question_context` from LLM).

## Important Patterns & Preferences

*   Maintain separation of concerns between modules.
*   Use type hinting in Python code.
*   Provide informative error messages and exit codes in the CLI.
*   Keep Memory Bank updated after significant changes.

## Learnings & Insights

*   Bootstrapping the project structure and CLI provides a solid foundation.
*   NetworkX with GraphML is working well for the initial prototype stage.
*   Metadata handling for processing PDFs requires careful consideration (CLI args vs. filename parsing).
*   LLM integration is the most complex remaining part of the core pipeline.
