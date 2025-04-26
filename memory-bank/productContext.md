# Product Context: Past Paper Concept Analyzer

## Problem

Cambridge CS students revise using past papers, but manually identifying recurring themes, key concepts per paper/course, and relationships between topics across years is time-consuming and difficult. There's no structured way to analyze the conceptual landscape of past exams.

## Solution

This tool automates the analysis of past paper solutions PDFs. It uses a Vision LLM to extract key concepts from each question and stores this information, along with metadata (paper, year, question number, etc.), in a structured graph database.

## How it Should Work

1.  User provides CL authentication cookie via a config file (`.env`).
2.  User invokes the CLI tool, specifying papers/years to analyze.
3.  The tool downloads the relevant solutions PDFs.
4.  Each PDF is processed by a Vision LLM to extract concepts per question.
5.  Extracted data (concepts, paper info, question info) is stored in the graph database, linking concepts to the questions they appear in.
6.  The tool offers commands to query the database and generate visualizations (e.g., concept co-occurrence networks, frequency trends).

## User Experience Goals

*   **Insightful:** Provide clear visualizations and data summaries that help students understand exam trends and concept relationships.
*   **Easy to Use:** Simple CLI interface for downloading, processing, and querying. Straightforward configuration for authentication.
*   **Accurate:** Strive for high accuracy in concept extraction and canonicalization, acknowledging this is a challenge.
