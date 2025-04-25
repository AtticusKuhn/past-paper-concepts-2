# Past Paper Concept Analyzer

A system for analyzing University of Cambridge Computer Science Tripos past papers (solutions PDFs) to extract, store, and analyze key concepts and themes.

## Goal

The primary goal is to build a structured database of concepts frequently appearing in CS Tripos papers (Parts IA, IB, and II). This aims to help current Cambridge Computer Science undergraduate students identify recurring topics and optimize their revision strategy.

The system will process official solutions PDFs (which typically include the questions) downloaded from the Computer Laboratory website (`cl.cam.ac.uk`). It will use a Vision Language Model (LLM), such as GPT-4o, to identify and extract key concepts from each question's solution.

## Features

*   **Automated Downloading:** Capability to download specific past paper solutions PDFs from the CL website (requires user authentication cookie).
*   **Concept Extraction:** Utilizes Vision LLMs to analyze PDFs and extract relevant computer science concepts.
*   **Structured Storage:** Stores extracted concepts and associated metadata in a queryable database.
*   **Subject Organization:** Keeps data organized by paper, question, year, and potentially the corresponding course module.

## How it Works

1.  **Download:** The tool fetches specified solutions PDFs from the CL website, using a user-provided authentication cookie for access.
2.  **Process:** Each PDF is sent to a Vision LLM.
3.  **Extract:** The LLM is prompted to identify and list the key concepts covered in each question/solution.
4.  **Store:** The extracted concepts, along with metadata, are stored in a database.

## Database Schema

The relationship between concepts and questions is many-to-many. The database schema needs to reflect this. Below are potential structures for relational (SQLite) and graph databases.

**Option 1: Relational Database (e.g., SQLite)**

This approach uses multiple tables linked by foreign keys.

*   **`Papers` Table:** Stores information about each exam paper.
    *   `paper_id` (Primary Key)
    *   `paper_code` (e.g., "2022-p06", Unique)
    *   `year` (e.g., 2022)
    *   `tripos_part` (e.g., "IB")
*   **`Questions` Table:** Stores information about each question within a paper.
    *   `question_id` (Primary Key)
    *   `paper_id` (Foreign Key referencing `Papers.paper_id`)
    *   `question_number` (e.g., "q01")
    *   `course_module` (Optional/Best Effort, e.g., "Algorithms")
*   **`Concepts` Table:** Stores unique concepts identified across all papers.
    *   `concept_id` (Primary Key)
    *   `concept_name` (Canonical name, e.g., "Binary Search Tree", Unique)
    *   `concept_definition` (Optional, LLM-generated or curated definition)
*   **`QuestionConcepts` Table (Join Table):** Links questions to the concepts they cover.
    *   `question_id` (Foreign Key referencing `Questions.question_id`)
    *   `concept_id` (Foreign Key referencing `Concepts.concept_id`)
    *   *(Composite Primary Key: (`question_id`, `concept_id`))*
    *   *(Optional: Store context-specific details here if needed)*

**Option 2: Graph Database (e.g., Neo4j, NetworkX)**

This approach models entities as nodes and relationships as edges.

*   **Nodes:**
    *   `Paper` (Properties: `paper_code`, `year`, `tripos_part`)
    *   `Question` (Properties: `question_number`, `course_module`)
    *   `Concept` (Properties: `name`, `definition`)
*   **Relationships:**
    *   `(:Question)-[:PART_OF]->(:Paper)`
    *   `(:Question)-[:MENTIONS]->(:Concept)` (or `(:Concept)-[:APPEARS_IN]->(:Question)`)

**Choice of Technology:**

*   **SQLite:** Simple, portable, file-based, good for straightforward querying. Requires careful schema design for relationships.
*   **Graph Database:** Excellent for visualizing and querying complex relationships between concepts, papers, and courses. Might have a steeper learning curve or require more setup (e.g., Neo4j server).

The final choice will depend on the desired query complexity and visualization needs.

## Difficult Issues / Challenges

These are key challenges anticipated during development:

*   **Concept Canonicalization:** Ensuring consistent naming for the same concept (`concept_name` in `Concepts` table or `name` property on `Concept` node) across different papers and questions is crucial. For example, the LLM might extract "Bellman-Ford" from one paper and "Bellman-Ford-Moore algorithm" from another. Potential strategies include:
    *   Sophisticated LLM prompting to enforce a canonical naming scheme.
    *   Post-processing steps to normalize extracted concept names (e.g., using string similarity, synonym lists, or embedding comparisons).
    *   Manual review and mapping of extracted terms.
*   **Authentication for Downloads:** Accessing solutions PDFs requires authentication. The tool needs a secure and user-friendly way for users to provide their CL authentication cookie. The planned approach is via a configuration file (e.g., a `.env` file).
*   **Accuracy of LLM Extraction:** The quality and relevance of extracted concepts depend heavily on the LLM's capabilities and the prompting strategy used.
*   **Mapping Concepts to Courses:** Reliably associating extracted concepts (`course_module` in `Questions` table or property on `Question` node) with the specific course module they belong to might require additional logic or data sources.

## Project Status & Usage

*   **Status:** Currently in the **planning and design phase**.
*   **Language:** To be implemented in **Python**, leveraging its strong ecosystem for AI/LLM interactions and data processing.
*   **Interface:** Planned as a **Command-Line Interface (CLI)** tool.

## Setup & Authentication

*(Details to be added once implementation begins)*

The tool will require Python and relevant libraries. Users will need to provide their CL authentication cookie via a configuration file (e.g., `.env`) to enable the downloading of solutions papers. Example:

