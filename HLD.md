AuraSCM — High-Level Design (HLD)

Project Title: AuraSCM: AI-Driven Semantic Merge, Dependency Blast-Radius & Compliance Gate
Version: 1.0
Project Team: Abhinesh G and Madhan D

1. Introduction

1.1 Purpose

This document describes the high-level architecture of AuraSCM, including its major components, data flow, interfaces, and technology stack.

1.2 Design Overview

AuraSCM follows a modular architecture. Each major component performs a specific analysis task. The command-line interface coordinates configured analysis operations, while the dashboard presents results to users.

2. System Architecture

The system consists of the following logical components:

1. User Interface.
2. Semantic Analysis Engine.
3. Dependency Graph Engine.
4. Conflict Prediction Engine.
5. Compliance Engine.
6. Self-Healing Engine.
7. Command-Line Orchestrator.
8. GitHub Actions Automation.

2.1 Architecture Diagram

           Developer / Project Team
                     |
           +---------+---------+
           |                   |
     Streamlit Dashboard   CLI Entry Point
           |               aurascm_cli.py
           |                   |
           +---------+---------+
                     |
            Analysis Workflow
                     |
       +-------------+-------------+
       |             |             |
       v             v             v
 Semantic Engine  Dependency   Conflict Prediction
                  Graph Engine      Engine
       |             |             |
       +-------------+-------------+
                     |
                     v
              Compliance Engine
                     |
                     v
              Self-Healing Engine
                     |
                     v
             Analysis Results
                     |
                     v
              User / Developer

 GitHub Repository --> GitHub Actions
                          |
                          v
                 Automated Validation

Note: This is a logical overview. Confirm the actual execution order and data flow from the implementation before presenting it as the exact runtime architecture.

3. Major Components

3.1 Semantic Analysis Engine

The Semantic Analysis Engine compares two versions of source code and identifies supported structural or semantic differences.

Input: Two versions of source code.
Processing: Code comparison using the implemented analysis methods.
Output: Detected differences for further analysis.

3.2 Dependency Graph Engine

The Dependency Graph Engine represents supported relationships between functions or software components.

Input: Source code and supported dependency information.
Processing: Construction or analysis of dependency relationships.
Output: Dependency information and potential blast-radius results.

3.3 Conflict Prediction Engine

The Conflict Prediction Engine evaluates supported change information and produces conflict classifications or risk estimates.

Input: Features produced by the configured analysis workflow.
Processing: The implemented prediction or scoring mechanism.
Output: Conflict predictions and associated risk information.

3.4 Compliance Engine

The Compliance Engine checks source code or project artifacts against the rules implemented in AuraSCM.

Input: Supported source files and configured rules.
Processing: Rule evaluation and compliance analysis.
Output: Compliance findings and validation status.

3.5 Self-Healing Engine

The Self-Healing Engine provides suggested resolutions for supported conflict types.

Input: Detected conflicts.
Processing: Selection of an applicable resolution suggestion.
Output: Recommended resolution advice for developer review.

3.6 Dashboard

The dashboard provides a visual interface for presenting analysis results and supported project information.

3.7 Command-Line Interface

The "aurascm_cli.py" entry point executes the configured analysis workflow and returns a process status that can be used by automation.

3.8 GitHub Actions

GitHub Actions executes the configured validation workflow when the specified pull-request events occur.

4. Technology Stack

Technology| Purpose
Python| Core implementation language
Git| Version control
GitHub| Repository hosting and collaboration
Visual Studio Code| Development environment
Streamlit| Dashboard interface
Python packages| Analysis and prediction dependencies
GitHub Actions| Automated validation
"requirements.txt"| Dependency specification

5. Data Flow

1. The developer supplies or selects the source-code versions to analyze.
2. The configured analysis workflow processes the available source code.
3. The Semantic Analysis Engine identifies supported differences.
4. The Dependency Graph Engine analyzes supported relationships.
5. The Conflict Prediction Engine evaluates conflict risk.
6. The Compliance Engine evaluates configured rules.
7. The Self-Healing Engine generates applicable resolution suggestions.
8. Results are presented through the supported user interface or command-line output.
9. GitHub Actions executes automated validation when triggered by the configured events.

The actual execution order may vary depending on the implementation.

6. Design Principles

- Modularity: Analysis responsibilities are separated into components.
- Maintainability: Individual modules can be updated independently where interfaces permit.
- Traceability: Git records changes to source code and documentation.
- Automation: GitHub Actions executes configured validation steps.
- Human Review: Developers review suggestions and make final merge decisions.

7. Conclusion

The high-level design of AuraSCM organizes semantic analysis, dependency analysis, conflict prediction, compliance checking, and resolution suggestions into a modular software configuration management system. GitHub and GitHub Actions support version control and automated validation.
