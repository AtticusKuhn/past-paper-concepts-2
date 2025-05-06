# Active Context: Past Paper Concept Analyzer

## Current Focus

*   **Phase:** Initial Implementation / Prototyping.
*   **Activity:** Implementing batch download feature, refining CLI, and preparing for LLM integration.

## Recent Changes

*   **Commit:** `7c447c1` (fix: Clarify single-question PDF assumption in comments and docs)
*   **Documentation:** Updated comments in `cli.py` and memory bank files (`projectbrief.md`, `productContext.md`, `activeContext.md`) to correctly reflect that each solutions PDF pertains to a single question.
*   **Batch Downloading:** Implemented `batch_parser.py` to parse specification files. Updated `cli.py` to include a `--batch-file` option for the `download` command.
    *   The batch file supports year/paper ranges and optional course module hints.
    *   The download logic in `cli.py` iterates through parsed specifications. The call to `downloader.download_pdf` uses a placeholder `question_placeholder = "all"` which needs to be updated to use specific question numbers derived from the batch spec for downloading individual question PDFs.
*   **Selected Graph Backend:** Chose **NetworkX** with GraphML file persistence for the initial prototype.
*   **Core Modules Implemented:** `config.py`, `downloader.py` (summary), `llm_extractor.py` (placeholder), `graph_store.py` (summary), `cli.py`, `main.py`, `batch_parser.py`.
*   **Environment:** `shell.nix` configured.

## Next Steps

1.  **Refine Batch Download for Question-Specific PDFs:**
    *   Update `batch_parser.py`'s `SPECIFIER_PATTERN` and parsing logic to include question numbers or ranges (e.g., `y<YYYY>p<XX>q<ZZ>` or `y<YYYY>p<XX>q[<ZZ>-<ZZ>]`).
    *   Modify `cli.py` in `handle_download` to use the parsed `question_number` from the batch spec when calling `downloader.download_pdf`, instead of the `question_placeholder = "all"`.
    *   Ensure `downloader.download_pdf` is correctly structured to accept `year`, `paper_code`, and `question_number` to fetch individual question-specific solution PDFs.
2.  **Implement LLM Interaction:** Replace the placeholder in `llm_extractor.py`.
    *   Develop prompt strategy for single-question PDFs.
    *   Handle PDF data input to Vision LLM.
    *   Parse LLM's JSON response.
3.  **Refine `process` Command & Metadata:**
    *   Ensure `tripos_part` is reliably captured.
    *   Integrate `course_hint` from batch downloads into the `process` command and potentially pass to `llm_extractor.py`.
4.  **Implement Concept Canonicalization Strategy:** (See "Concept Canonicalization Strategies" below).
5.  **Testing:** Add tests for batch file parsing (including question numbers), download logic, graph operations, CLI.

## Active Decisions & Considerations

*   **Batch File Specifier for Questions:**
    *   **Decision:** The batch download feature *must* aim to download specific single-question solution PDFs. The `batch_parser.py` and its specifiers (`SPECIFIER_PATTERN`) need to be updated to include question numbers/ranges (e.g., `y2022p06q[01-03]`). This is critical as each PDF is for one question.
*   **Concept Canonicalization Strategies:** This is a key challenge to avoid duplicate concept nodes (e.g., "first wave HCI" vs. "first-wave HCI", "FHCI" vs. "Further HCI"). Brainstormed strategies include:
    *   **Enhanced String Normalization:** Beyond lowercase/trim; handle punctuation, internal whitespace consistently.
    *   **Acronym Management:** Maintain a dictionary mapping acronyms to full canonical forms (e.g., "FHCI" -> "Further Human Computer Interaction"). Store canonical form, optionally alias acronym.
    *   **Stemming/Lemmatization:** Reduce words to root/dictionary form. Lemmatization preferred.
    *   **Synonym Sets/Thesaurus:** Curated lists mapping synonyms to a preferred canonical term.
    *   **LLM-Powered Canonicalization:**
        *   At extraction: Prompt LLM for canonical forms/aliases.
        *   Post-processing: Ask LLM to compare new terms with existing canonical terms.
    *   **Embedding-Based Similarity:** Generate vector embeddings for concept names/definitions. Compare new concepts to existing ones using cosine similarity. Flag high similarity as potential duplicates.
    *   **Hybrid Approaches & Manual Review:** Combine automated methods (normalization, acronyms, embeddings) with a manual review queue for uncertain cases. This allows for building a high-quality, curated list over time.
*   **LLM Prompting for Single-Question PDFs:** Simplified as the LLM context is one question at a time.
*   **PDF to LLM Input:** Decide on the best method (direct bytes or images).
*   **Error Handling:** Continue improving for batch operations and LLM calls.

## Important Patterns & Preferences

*   Maintain separation of concerns between modules.
*   Use type hinting in Python code.
*   Provide informative error messages and exit codes in the CLI.
*   Keep Memory Bank updated after significant changes.

## Learnings & Insights

*   Batch downloading significantly enhances usability.
*   The "one PDF per question" clarification simplifies the `process` command's logic and LLM prompting strategy, but requires the batch download mechanism to correctly identify and fetch these individual question PDFs.
*   The `batch_parser.py` needs adaptation for question-level granularity.
