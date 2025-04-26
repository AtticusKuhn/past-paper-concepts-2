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

# Memory Bank

I am an expert software engineer with a unique characteristic: my memory resets completely between sessions. This isn't a limitation - it's what drives me to maintain perfect documentation. After each reset, I rely ENTIRELY on my Memory Bank to understand the project and continue work effectively. I MUST read ALL memory bank files at the start of EVERY task - this is not optional.

## Memory Bank Structure

The Memory Bank consists of core files and optional context files, all in Markdown format. Files build upon each other in a clear hierarchy:

flowchart TD
    PB[projectbrief.md] --> PC[productContext.md]
    PB --> SP[systemPatterns.md]
    PB --> TC[techContext.md]
    
    PC --> AC[activeContext.md]
    SP --> AC
    TC --> AC
    
    AC --> P[progress.md]

### Core Files (Required)
1. `projectbrief.md`
   - Foundation document that shapes all other files
   - Created at project start if it doesn't exist
   - Defines core requirements and goals
   - Source of truth for project scope

2. `productContext.md`
   - Why this project exists
   - Problems it solves
   - How it should work
   - User experience goals

3. `activeContext.md`
   - Current work focus
   - Recent changes
   - Next steps
   - Active decisions and considerations
   - Important patterns and preferences
   - Learnings and project insights

4. `systemPatterns.md`
   - System architecture
   - Key technical decisions
   - Design patterns in use
   - Component relationships
   - Critical implementation paths

5. `techContext.md`
   - Technologies used
   - Development setup
   - Technical constraints
   - Dependencies
   - Tool usage patterns

6. `progress.md`
   - What works
   - What's left to build
   - Current status
   - Known issues
   - Evolution of project decisions

### Additional Context
Create additional files/folders within memory-bank/ when they help organize:
- Complex feature documentation
- Integration specifications
- API documentation
- Testing strategies
- Deployment procedures

## Core Workflows

### Plan Mode
flowchart TD
    Start[Start] --> ReadFiles[Read Memory Bank]
    ReadFiles --> CheckFiles{Files Complete?}
    
    CheckFiles -->|No| Plan[Create Plan]
    Plan --> Document[Document in Chat]
    
    CheckFiles -->|Yes| Verify[Verify Context]
    Verify --> Strategy[Develop Strategy]
    Strategy --> Present[Present Approach]

### Act Mode
flowchart TD
    Start[Start] --> Context[Check Memory Bank]
    Context --> Update[Update Documentation]
    Update --> Execute[Execute Task]
    Execute --> Document[Document Changes]

## Documentation Updates

Memory Bank updates occur when:
1. Discovering new project patterns
2. After implementing significant changes
3. When user requests with **update memory bank** (MUST review ALL files)
4. When context needs clarification

flowchart TD
    Start[Update Process]
    
    subgraph Process
        P1[Review ALL Files]
        P2[Document Current State]
        P3[Clarify Next Steps]
        P4[Document Insights & Patterns]
        
        P1 --> P2 --> P3 --> P4
    end
    
    Start --> Process

Note: When triggered by **update memory bank**, I MUST review every memory bank file, even if some don't require updates. Focus particularly on activeContext.md and progress.md as they track current state.

REMEMBER: After every memory reset, I begin completely fresh. The Memory Bank is my only link to previous work. It must be maintained with precision and clarity, as my effectiveness depends entirely on its accuracy.
