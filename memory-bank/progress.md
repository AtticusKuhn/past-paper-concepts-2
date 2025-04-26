# Progress: Past Paper Concept Analyzer

## Current Status

*   **Phase:** Planning and Design (as of initialization date).
*   **Overall Progress:** 0% implemented.

## What Works

*   N/A - No implementation yet.

## What's Left to Build

*   **Everything:**
    *   Project setup (directory structure, virtual environment, dependencies).
    *   Configuration handling (`.env` loading).
    *   PDF Downloading module (including authentication).
    *   LLM Interaction module (API connection, prompt sending, response handling).
    *   Concept Extraction/Canonicalization logic.
    *   Graph Database Interaction module (connecting, CRUD operations for nodes/relationships based on chosen backend).
    *   Querying logic.
    *   Visualization generation module.
    *   CLI interface implementation.
    *   Testing suite.
    *   Documentation (user guide, setup instructions beyond README).

## Known Issues

*   N/A - No implementation yet.

## Evolution of Project Decisions

*   **Initial:** Considered SQLite database.
*   **Current:** Decided on a Graph Database architecture due to the nature of the data (relationships) and visualization goals.
*   **Initial:** Vague idea of LLM use.
*   **Current:** Specified using a Vision LLM on solutions PDFs.
*   **Initial:** Unspecified authentication method.
*   **Current:** Planned to use a `.env` file for the CL authentication cookie.
