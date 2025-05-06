# Product Context: Past Paper Concept Analyzer

## Problem

Cambridge CS students revise using past papers, but manually identifying recurring themes, key concepts per paper/course, and relationships between topics across years is time-consuming and difficult. There's no structured way to analyze the conceptual landscape of past exams.

## Solution

This tool automates the analysis of past paper solutions PDFs. It uses a Vision LLM to extract key concepts from each question and stores this information, along with metadata (paper, year, question number, etc.), in a structured graph database. Each solutions PDF processed corresponds to a single question.

## How it Should Work

1.  User provides CL authentication cookie via a config file (`.env`).
2.  User invokes the CLI tool, specifying single-question solutions PDFs to analyze either individually (by year, paper, question) or by providing a batch download file.
3.  The tool downloads the relevant single-question solutions PDFs. Each downloaded PDF (e.g., `YYYY-pXX-qYY-solutions.pdf`) contains the solution for exactly one question.
    *   If a batch file is used, the tool parses it to determine the list of individual question PDFs to download. The batch file can include optional course module hints for the specified papers/questions.
4.  Each single-question PDF is processed by a Vision LLM to extract concepts. Any course module hints can be used to guide this process.
5.  Extracted data (concepts, paper info, question info) is stored in the graph database, linking concepts to the specific question they appear in.
6.  The tool offers commands to query the database and generate visualizations (e.g., concept co-occurrence networks, frequency trends).

## User Experience Goals

*   **Insightful:** Provide clear visualizations and data summaries that help students understand exam trends and concept relationships.
*   **Easy to Use:** Simple CLI interface for downloading (individually or in batch), processing, and querying. Straightforward configuration for authentication and batch downloads.
*   **Accurate:** Strive for high accuracy in concept extraction and canonicalization, acknowledging this is a challenge.
