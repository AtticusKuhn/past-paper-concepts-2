# Project Brief: Past Paper Concept Analyzer

## Core Goal

To create a system that analyzes University of Cambridge Computer Science Tripos past paper solutions (PDFs) to extract, store, and visualize key concepts.

## Scope

*   **Input:** Official solutions PDFs for CS Tripos papers (Parts IA, IB, II) from the CL website.
*   **Processing:** Use a Vision LLM (e.g., GPT-4o) to identify and extract concepts from each question/solution.
*   **Storage:** Store extracted concepts and metadata (paper, question, year, tripos part, course module, definition) in a graph database.
*   **Output:** Provide data and visualizations to help students identify recurring topics, understand concept relationships, and optimize revision.
*   **Interface:** Command-Line Interface (CLI).
*   **Target Users:** Current Cambridge Computer Science undergraduate students (all years).

## Critical Implementation Paths

*   Reliable PDF downloading with authentication.
*   Effective prompting strategy for the Vision LLM to extract relevant and well-formed concepts.
*   Implementing a robust concept canonicalization strategy.
*   Designing efficient graph database queries for the desired visualizations.
