AuraSCM — AI-Driven Semantic Merge, Dependency Blast-Radius & Compliance Gate

AuraSCM is an AI-assisted Software Configuration Management (SCM) project designed to identify semantic code differences, analyze dependency impact, assess conflict risks, validate configured compliance rules, and suggest possible conflict resolutions before code changes are merged.

🌐 Live Dashboard: https://aurascm-merge-gate.streamlit.app/

---

Table of Contents

- "Project Overview" (#project-overview)
- "Problem Statement" (#problem-statement)
- "Objectives" (#objectives)
- "Key Features" (#key-features)
- "System Modules" (#system-modules)
- "System Architecture" (#system-architecture)
- "Technology Stack" (#technology-stack)
- "Repository Structure" (#repository-structure)
- "Installation and Setup" (#installation-and-setup)
- "Running AuraSCM" (#running-aurascm)
- "Testing and Validation" (#testing-and-validation)
- "Software Configuration Management" (#software-configuration-management)
- "Limitations" (#limitations)
- "Future Enhancements" (#future-enhancements)
- "Project Team" (#project-team)

---

Project Overview

Traditional version control systems identify textual differences between source-code versions. However, changes that appear different at the text level may affect the same program logic or dependent functions.

AuraSCM extends the SCM workflow with automated code analysis and validation to help developers understand potential conflicts before merging changes.

The system combines semantic difference analysis, dependency impact analysis, conflict risk assessment, compliance checking, and resolution suggestions in a modular Python-based application.

The project uses Git and GitHub for version control and collaboration, while GitHub Actions supports automated validation through a configured workflow.

Problem Statement

Traditional merge workflows may not adequately explain the semantic impact of changes across functions and dependent components. Developers may need to manually inspect source code, trace dependencies, evaluate compliance requirements, and resolve conflicts.

This can increase review time and the risk of introducing defects.

AuraSCM addresses this problem by providing a centralized workflow for analyzing supported code differences, identifying potential dependency impacts, assessing conflict risks, checking configured compliance rules, and suggesting possible resolutions.

Objectives

- Identify relevant semantic differences between source-code versions.
- Analyze dependencies and estimate the potential blast radius of changes.
- Classify supported code conflicts.
- Provide conflict risk information using the implemented prediction or scoring mechanism.
- Validate source code against configured compliance rules.
- Suggest possible resolutions for supported conflicts.
- Present analysis results through a dashboard and command-line interface.
- Support controlled changes through Git branches, commits, tags, and GitHub pull requests.
- Automate configured validation tasks using GitHub Actions.

Key Features

1. Semantic Difference Analysis

Compares supported source-code versions and identifies differences relevant to conflict analysis.

2. Dependency Blast-Radius Analysis

Analyzes supported dependency relationships to identify functions or components that may be affected by a change.

3. Conflict Prediction

Uses the implemented prediction or scoring mechanism to classify supported conflicts and provide associated risk information.

4. Compliance Validation

Checks supported code or project artifacts against the rules configured in the Compliance Engine.

5. Self-Healing Suggestions

Provides recommended resolution advice for supported conflict types. Suggestions are intended for developer review rather than unconditional automatic merging.

6. Interactive Dashboard

Presents available analysis results through the Streamlit interface.

7. Command-Line Validation

Provides a command-line entry point for executing the configured analysis workflow.

8. Automated SCM Validation

Uses GitHub Actions to execute the configured dependency installation, dataset-generation, and CLI validation steps for applicable pull requests.

---

System Modules

Module| Directory| Responsibility
Semantic Analysis Engine| "semantic_engine/"| Identifies supported differences between source-code versions.
Dependency Graph Engine| "dependency_graph/"| Represents and analyzes supported dependencies and potential change impact.
Conflict Prediction Engine| "conflict_prediction/"| Produces conflict classifications or risk information using the implemented mechanism.
Compliance Engine| "compliance_engine/"| Evaluates configured compliance rules and reports findings.
Self-Healing Engine| "self_healing/"| Provides possible resolutions for supported conflicts.
Dashboard| "dashboard/"| Presents analysis results through the user interface.
Dataset and Data Utilities| "data/"| Contains dataset-related files and data-generation utilities.
Sample Repository| "sample_repo/"| Contains sample source-code files for demonstrations and testing.
Automation Workflow| ".github/workflows/"| Contains the configured GitHub Actions workflow.

System Architecture

The following diagram represents the logical organization of AuraSCM.

              Developer / User
                     |
          +----------+----------+
          |                     |
          v                     v
   Streamlit Dashboard     CLI Entry Point
                             aurascm_cli.py
          |                     |
          +----------+----------+
                     |
              Analysis Workflow
                     |
          +----------+----------+
          |          |          |
          v          v          v
      Semantic   Dependency   Conflict
      Analysis    Analysis   Prediction
          |          |          |
          +----------+----------+
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
                 Developer

       GitHub Repository
              |
              v
       GitHub Actions
              |
              v
      Automated Validation

Note: The diagram is a logical overview. The actual execution order depends on the implemented workflow.

---

Technology Stack

Technology| Purpose
Python| Core programming language
Git| Version control and change history
GitHub| Repository hosting and collaboration
Visual Studio Code| Development environment
Streamlit| Interactive dashboard
Python virtual environment ("venv")| Isolated development environment
"requirements.txt"| Python dependency specification
GitHub Actions| Automated validation workflow

---

Repository Structure

The main project directories and files are organized as follows.

AuraSCM/
│
├── .github/
│   └── workflows/
│       └── aurascm.yml
│
├── compliance_engine/
│
├── conflict_prediction/
│
├── dashboard/
│
├── data/
│
├── dependency_graph/
│
├── sample_repo/
│   ├── branch_a.py
│   └── branch_b.py
│
├── self_healing/
│
├── semantic_engine/
│
├── docs/
│   ├── SRS.md
│   ├── HLD.md
│   └── LLD.md
│
├── .gitignore
├── README.md
├── aurascm_cli.py
└── requirements.txt

Note: The "docs/" folder and its three documents should be added to GitHub if they do not already exist. Confirm all listed paths against the actual repository before treating this tree as the final structure.

---

Installation and Setup

Prerequisites

Install the following software:

- Python 3.10 or a compatible version supported by the project dependencies.
- Git.
- Visual Studio Code or another Python development environment.

The configured GitHub Actions workflow uses Python 3.12. For consistent results, Python 3.12 is recommended if all project dependencies support it.

Step 1: Clone the Repository

Open a terminal and run:

git clone https://github.com/Abhinesh18G/AuraSCM.git

Step 2: Enter the Project Directory

cd AuraSCM

Step 3: Create a Virtual Environment

python -m venv venv

Step 4: Activate the Virtual Environment

Windows Command Prompt:

venv\Scripts\activate

Windows PowerShell:

.\venv\Scripts\Activate.ps1

Linux or macOS:

source venv/bin/activate

Step 5: Install Dependencies

python -m pip install --upgrade pip
pip install -r requirements.txt

If installation fails, check the Python version and the error reported by the affected dependency.

---

Running AuraSCM

1. Launch the Dashboard

Open the live dashboard:

https://aurascm-merge-gate.streamlit.app/

If you want to run the application locally, identify the Streamlit entry-point file in the "dashboard/" directory.

For example, if the entry point is "dashboard/app.py", run:

streamlit run dashboard/app.py

Replace "dashboard/app.py" with the actual filename if your entry point is different.

2. Run the Command-Line Interface

From the project root, run:

python aurascm_cli.py

This executes the configured CLI workflow. The displayed results depend on the current implementation and input data.

3. Test Self-Healing Suggestions

The project references "diff_versions" and "suggest_resolution" for comparing sample source code and displaying resolution suggestions.

Run the following command from the project root if the referenced modules and sample files are available:

python -c "from semantic_engine.ast_diff import diff_versions; from self_healing.suggest import suggest_resolution; a=open('sample_repo/branch_a.py').read(); b=open('sample_repo/branch_b.py').read(); [print(suggest_resolution(c)) for c in diff_versions(a,b)]"

The command prints suggestions for the differences returned by the semantic analysis function.

---

Testing and Validation

AuraSCM can be evaluated using scenarios such as the following.

Test ID| Scenario| Expected Behaviour
T1| Branches contain supported logic divergence.| The system identifies the difference and reports the configured conflict result.
T2| Both branches contain identical code.| No semantic differences are reported for identical inputs.
T3| A supported function signature changes.| The system reports a signature mismatch if that change is covered by the implemented detection logic.
T4| A configured compliance rule is violated.| The Compliance Engine reports the applicable finding.
T5| A supported conflict is passed to the self-healing module.| The module returns an applicable resolution suggestion or a supported fallback result.

These are test scenarios, not a claim that every test has already passed. Record actual results after executing each test.

---

Software Configuration Management

AuraSCM applies SCM practices throughout development.

Version Management

Git tracks changes to source code and documentation. Commits record change history, while branches support isolated development and review.

Configuration Identification

Project modules, source files, configuration files, and documentation can be identified as configuration items.

The SRS, HLD, and LLD should be stored under "docs/" if they are maintained as repository configuration items.

Configuration Control

GitHub Issues and Pull Requests support change tracking, review, and collaboration. Branch protection or rulesets can enforce additional merging requirements when configured.

Status Accounting

The following Git commands provide useful status and history information.

git log --oneline --graph --decorate --all
git shortlog -sn --all
git tag -n
git status

Configuration Auditing

Git provides commands for inspecting changes and tracking source-code history.

git diff
git diff Baseline-1..HEAD --stat
git blame semantic_engine/ast_diff.py

The baseline comparison requires the "Baseline-1" tag to exist, and the blame command requires the specified file to be present.

Automated Validation

The configured GitHub Actions workflow is stored at:

".github/workflows/aurascm.yml"

It installs the configured Python dependencies, runs the dataset-generation script, and executes the CLI validation command when the specified pull-request events trigger it.

Merge blocking depends on the workflow's result and the repository's branch protection or ruleset configuration.

---

Limitations

- Conflict detection is limited to the source-code structures and cases supported by the implementation.
- Prediction results depend on the implemented model, features, and available data.
- Dependency impact analysis depends on the relationships the system can identify.
- Compliance validation covers only the rules configured in the project.
- Self-healing suggestions require developer evaluation.
- Passing automated validation does not guarantee that software is free of defects.

Future Enhancements

Potential improvements include:

- Expanding semantic analysis to support more programming constructs.
- Improving dependency extraction and blast-radius analysis.
- Evaluating prediction quality with larger and more diverse datasets.
- Adding more configurable compliance rules.
- Expanding the range of supported conflict-resolution suggestions.
- Improving automated test coverage.
- Adding structured reports for audit and release activities.

These are proposed enhancements, not necessarily implemented features.

---

Project Team

Name| Registration Number
Abhinesh G| 24MIS0370
Madhan D| 24MIS0372

Department: Information Technology

Live Application

Access the AuraSCM dashboard:

https://aurascm-merge-gate.streamlit.app/

---

Conclusion

AuraSCM combines software configuration management practices with semantic code analysis, dependency impact analysis, conflict risk assessment, compliance validation, and resolution suggestions.

By combining Git, GitHub, Python, Streamlit, and GitHub Actions, the project demonstrates how automated analysis and controlled development workflows can help developers review changes and improve software maintainability.
