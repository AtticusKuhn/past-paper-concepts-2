# Active Context: Past Paper Concept Analyzer

## Current Focus

*   **Phase:** Planning and Design.
*   **Activity:** Defining core architecture, features, database schema, potential challenges, and technology stack. Refining project scope via `README.md` and Memory Bank initialization.

## Recent Changes

*   Decided on a **Graph Database** architecture as the primary storage mechanism.
*   Detailed potential **visualization** types (co-occurrence, frequency trends, concept maps, interactive exploration).
*   Refined the **database schema** (Nodes: Paper, Question, Concept; Relationships: PART_OF, MENTIONS).
*   Specified **Python** as the implementation language and outlined potential libraries/technologies.
*   Clarified **authentication** mechanism (via `.env` file).
*   Initialized the **Memory Bank**.

## Next Steps

1.  Finalize the choice of graph database backend (e.g., Neo4j vs. NetworkX with file persistence). Consider ease of setup, query language, and visualization integration.
2.  Design the initial Python project structure (modules, directories).
3.  Begin implementation, starting with core modules:
    *   PDF downloading (handling authentication).
    *   Basic graph database interaction (connecting, creating nodes/relationships).
    *   Initial LLM interaction setup (sending a sample PDF, getting a response).

## Active Decisions & Considerations

*   **Graph Backend Choice:** Need to weigh Neo4j (more features, server setup) vs. NetworkX (simpler, in-memory/file-based). NetworkX might be better for initial development simplicity.
*   **Concept Canonicalization Strategy:** This remains a key challenge requiring a concrete approach. Initial thoughts lean towards LLM prompting combined with post-processing (e.g., lowercasing, removing plurals, potentially embedding similarity for more complex cases).
*   **LLM Prompting:** Designing an effective prompt for the Vision LLM is critical for accurate concept extraction. Needs to specify desired output format (e.g., JSON list of concepts per question).
*   **Error Handling:** Need to consider failures in downloading, LLM API calls, PDF parsing, etc.

## Important Patterns & Preferences

*   Maintain clear separation of concerns between modules (download, process, store, visualize).
*   Prioritize clear documentation (README, Memory Bank, code comments).
*   Use type hinting in Python code.

## Learnings & Insights

*   Graph databases are well-suited for the project's goals, particularly visualization.
*   Concept canonicalization is a non-trivial problem requiring dedicated effort.
*   Clear definition of scope and architecture upfront (as done here) is crucial before coding begins.
