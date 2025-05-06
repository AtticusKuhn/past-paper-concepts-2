# Project Brief: Past Paper Concept Analyzer

## Core Goal

To create a system that analyzes University of Cambridge Computer Science Tripos past paper solutions (PDFs) to extract, store, and visualize key concepts.

## Scope

*   **Input:** Official solutions PDFs for individual questions from CS Tripos papers (Parts IA, IB, II) from the CL website. Each PDF file (e.g., `YYYY-pXX-qYY-solutions.pdf`) contains the solution for a single question.
*   **Batch Downloading:** Capability to download multiple single-question solutions PDFs at once using a user-defined list file. This file will support shorthand notations for specifying ranges of years/papers and optional course module hints.
*   **Processing:** Use a Vision LLM (e.g., GPT-4o) to identify and extract concepts from each single-question solutions PDF.
*   **Storage:** Store extracted concepts and metadata (paper, question, year, tripos part, course module, definition) in a graph database.
*   **Output:** Provide data and visualizations to help students identify recurring topics, understand concept relationships, and optimize revision.
*   **Interface:** Command-Line Interface (CLI).
*   **Target Users:** Current Cambridge Computer Science undergraduate students (all years).

## Critical Implementation Paths

*   Reliable PDF downloading with authentication for single-question solution files.
*   Parsing and processing of batch download specification files, including handling shorthand notations and managing multiple download operations for individual question PDFs.
*   Effective prompting strategy for the Vision LLM to extract relevant and well-formed concepts from each single-question PDF.
*   Implementing a robust concept canonicalization strategy.
*   Designing efficient graph database queries for the desired visualizations.
