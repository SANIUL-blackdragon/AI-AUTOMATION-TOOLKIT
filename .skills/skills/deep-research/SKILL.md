---
name: deep-research
description: "Executes deep, multi-step online investigations. Uses a recursive notebook approach to break down complex topics, perform iterative searches, validate conflicting data, and synthesize findings. Use for comprehensive market analysis, technical deep dives, or any research task requiring more than a single search. Triggered by queries demanding 'deep dive', 'thorough research', 'market analysis', or 'investigate'."
---

# Deep Research

## Overview

Deep Research is a recursive investigation workflow. Unlike standard search, it treats research as a multi-layered process of discovery, validation, and synthesis. It uses a persistent "Notebook" in the `agent-playground/` folder to track open questions and findings across multiple search iterations.

## Core Workflow

### 1. Preparation
1.  **Define Scope**: Ask the user for the depth of research (e.g., "How many search iterations or layers should I go?") and any specific areas of interest.
2.  **Initialize Workspace**: Create a session directory in `agent-playground/research_[timestamp]/`.
3.  **Setup Notebook**: Use `scripts/init_notebook.py` to create `notebook.md` in that directory.

### 2. The Recursive Investigation Loop
For each layer of research:

1.  **Decompose**: Break the primary research goal into 3-5 targeted sub-questions.
2.  **Execute Search**: Use `google_web_search`.
3.  **Process Content**: Use `web_fetch` or `curl` to extract data from relevant URLs. Use a mix of summarization and raw data extraction.
4.  **Update Notebook**:
    *   Log findings with strict citations: `[Title](URL) - Access Date`.
    *   **Flag Conflicts**: If Source A contradicts Source B, explicitly note this as a "Conflict" in the notebook.
5.  **Iterate**: Based on findings, identify new gaps or questions. If the depth limit hasn't been reached and questions remain, start the next layer.

### 3. Synthesis & Reporting
1.  **Resolve Conflicts**: Perform targeted searches to resolve any flagged conflicts by weighing logic, source authority, and consensus.
2.  **Generate Outputs**:
    *   **Markdown Report**: A human-readable summary (Executive Summary, Findings by Category, Sources).
    *   **JSON Report**: A structured data file for programmatic use.
3.  **Cleanup**: Offer to archive or delete the session directory in `agent-playground/`.

## Directives & Best Practices

- **Notebook First**: Never hold findings in memory. Write them to the session notebook immediately to preserve context and save tokens.
- **Citations Mandatory**: No assertion is valid without a cited source.
- **Deep Dive on Conflicts**: Resolving contradictions is the primary goal of "Deep" research.
- **Incremental Progress**: If a session is interrupted, the agent can resume by reading the existing notebook in `agent-playground/`.

## Resources

- **Scripts**:
    - `scripts/init_notebook.py`: Scaffolds the research session.
- **Assets**:
    - `assets/templates/research_notebook.md`: Template for tracking investigations.
    - `assets/templates/final_report.md`: Template for the final output.
