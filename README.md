# Past Paper Concept Analyzer

A system for analyzing University of Cambridge Computer Science Tripos past papers (solutions PDFs) to extract, store, and analyze key concepts and themes.

## Goal

The primary goal is to build a structured database of concepts frequently appearing in CS Tripos papers (Parts IA, IB, and II). This aims to help current Cambridge Computer Science undergraduate students identify recurring topics, understand relationships between concepts, and optimize their revision strategy.

The system will process official solutions PDFs (which typically include the questions) downloaded from the Computer Laboratory website (`cl.cam.ac.uk`). It will use a Vision Language Model (LLM), such as GPT-4o, to identify and extract key concepts from each question's solution.

## Features

*   **Automated Downloading:** Capability to download specific past paper solutions PDFs from the CL website (requires user authentication cookie).
*   **Concept Extraction:** Utilizes Vision LLMs to analyze PDFs and extract relevant computer science concepts.
*   **Structured Storage:** Stores extracted concepts and associated metadata in a queryable graph database.
*   **Subject Organization:** Keeps data organized by paper, question, year, and potentially the corresponding course module.
*   **Data Visualization:** Offers various ways to visualize the relationships and trends within the extracted data.

## How it Works

1.  **Download:** The tool fetches specified solutions PDFs from the CL website, using a user-provided authentication cookie for access.
2.  **Process:** Each PDF is sent to a Vision LLM.
3.  **Extract:** The LLM is prompted to identify and list the key concepts covered in each question/solution.
4.  **Store:** The extracted concepts, along with metadata, are stored in a graph database.
5.  **Visualize:** The tool provides interfaces or generates outputs for visualizing the stored graph data.

## Database Schema

A **Graph Database** architecture has been chosen to effectively model the many-to-many relationships between concepts and questions, and to facilitate complex queries and visualizations.

The schema models entities as nodes and relationships as edges:

*   **Nodes:**
    *   `Paper` (Properties: `paper_code` [Unique], `year`, `tripos_part`)
    *   `Question` (Properties: `question_number`, `course_module` [Optional])
    *   `Concept` (Properties: `name` [Unique, Canonical], `definition` [Optional])
*   **Relationships:**
    *   `(:Question)-[:PART_OF]->(:Paper)`: Connects a question to the specific paper it belongs to.
    *   `(:Question)-[:MENTIONS]->(:Concept)`: Connects a question to a concept it covers. (Alternatively, `(:Concept)-[:APPEARS_IN]->(:Question)`)

**Technology Choice Rationale:**

*   **Graph Database:** Chosen for its strength in representing and querying interconnected data. This structure is ideal for exploring how concepts relate to each other across different papers, questions, and potentially courses. It also opens up possibilities for visualizing the concept landscape.
*   **Potential Backends:** While a specific backend isn't finalized, options include:
    *   **Neo4j:** A popular, robust graph database server. Interaction would likely be via the official Python driver.
    *   **NetworkX:** A Python library for graph manipulation. Could be used for simpler, in-memory graph analysis or as an intermediate step, potentially persisting the graph to a file format.

The final backend choice will depend on scalability requirements and the complexity of desired queries and visualizations.

## Visualization Possibilities

The graph structure enables several insightful visualizations:

*   **Concept Co-occurrence Network:** Visualize which concepts frequently appear together in the same questions. Edges can be weighted by co-occurrence frequency, revealing clusters of related topics.
*   **Concept Frequency Trends:** Track how often concepts appear over different exam years using line charts or bar charts, highlighting enduring themes and changing focus areas.
*   **Paper/Course Concept Maps:** Generate graphs showing the key concepts covered in a specific paper or course module, providing a focused overview.
*   **Interactive Exploration:** Allow users to dynamically explore the full graph using interactive tools (potentially web-based), enabling filtering, zooming, and discovering connections on their own.

**Potential Visualization Tools:**

*   **Python Libraries:** `Matplotlib`, `Seaborn` (for static charts), `NetworkX` (for graph structure analysis and basic plotting), `pyvis` (for interactive NetworkX graphs in HTML).
*   **Graph Database Tools:** Neo4j Browser, Neo4j Bloom (for interactive exploration if using Neo4j).
*   **Web Technologies:** Frameworks like Flask/Django combined with JavaScript libraries (e.g., D3.js, Sigma.js) for custom, interactive web-based visualizations.

## Difficult Issues / Challenges

These are key challenges anticipated during development:

*   **Concept Canonicalization:** Ensuring consistent naming (`name` property on `Concept` node) for the same concept across different papers and questions is crucial. For example, the LLM might extract "Bellman-Ford" from one paper and "Bellman-Ford-Moore algorithm" from another. Potential strategies include:
    *   Sophisticated LLM prompting to enforce a canonical naming scheme.
    *   Post-processing steps to normalize extracted concept names (e.g., using string similarity, synonym lists, or embedding comparisons).
    *   Manual review and mapping of extracted terms.
*   **Authentication for Downloads:** Accessing solutions PDFs requires authentication. The tool needs a secure and user-friendly way for users to provide their CL authentication cookie. The planned approach is via a configuration file (e.g., a `.env` file).
*   **Accuracy of LLM Extraction:** The quality and relevance of extracted concepts depend heavily on the LLM's capabilities and the prompting strategy used.
*   **Mapping Concepts to Courses:** Reliably associating extracted concepts (`course_module` property on `Question` node) with the specific course module they belong to might require additional logic or data sources.

## Project Status & Usage

*   **Status:** Currently in the **planning and design phase**.
*   **Language:** To be implemented in **Python**, leveraging its strong ecosystem for AI/LLM interactions, data processing, and visualization libraries.
*   **Interface:** Planned as a **Command-Line Interface (CLI)** tool, potentially generating visualization outputs (e.g., HTML files, image files) or offering commands to launch interactive sessions.

## Setup & Authentication

*(Details to be added once implementation begins)*

The tool will require Python and relevant libraries. Users will need to provide their CL authentication cookie via a configuration file (e.g., `.env`) to enable the downloading of solutions papers. Example:

