AuraSCM — Software Requirements Specification (SRS)

Project Title: AuraSCM: AI-Driven Semantic Merge, Dependency Blast-Radius & Compliance Gate
Version: 1.0
Project Team: Abhinesh G and Madhan D
Department: Information Technology

1. Introduction

1.1 Purpose

The purpose of AuraSCM is to develop an intelligent software configuration management system that assists developers in identifying semantic code conflicts, analyzing dependency relationships, predicting conflict risks, checking compliance, and suggesting possible conflict resolutions.

Traditional version control systems primarily identify textual differences between files. However, two changes may be textually different while affecting the same program logic or dependent functions. AuraSCM aims to provide additional analysis to help developers identify these risks before merging changes.

1.2 Scope

AuraSCM combines software configuration management practices with code analysis and automated validation.

The major project functions are:

- Semantic code difference analysis.
- Dependency graph construction and blast-radius analysis.
- Conflict classification and risk prediction.
- Compliance checking.
- Self-healing resolution suggestions.
- Dashboard-based presentation of analysis results.
- Automated validation through GitHub Actions.

AuraSCM supports developers in reviewing changes. It does not replace developer approval or guarantee that every possible conflict will be detected.

1.3 Intended Users

- Software developers.
- Software configuration managers.
- Project team members.
- Software testers.
- Academic evaluators.

2. Overall Description

2.1 Product Perspective

AuraSCM is a Python-based software project maintained in GitHub. Its components analyze code changes, identify potential conflicts, evaluate configured compliance rules, and present results through a dashboard and command-line interface.

2.2 Product Functions

1. Compare two versions of source code.
2. Identify relevant semantic differences.
3. Analyze dependencies between functions.
4. Estimate the potential impact of code changes.
5. Classify detected conflicts.
6. Calculate or assign conflict risk scores.
7. Evaluate configured compliance rules.
8. Suggest possible conflict resolutions.
9. Display analysis results.
10. Execute automated validation through a CI workflow.

2.3 Operating Environment

- Operating system: Windows or Linux.
- Programming language: Python.
- Version control: Git.
- Repository hosting: GitHub.
- Development environment: Visual Studio Code.
- Dashboard: Streamlit.
- Automation: GitHub Actions.
- Dependencies: Python packages specified in "requirements.txt".

3. Functional Requirements

FR-01: Semantic Difference Analysis
The system shall compare two versions of source code and identify relevant differences using the implemented semantic analysis methods.

FR-02: Dependency Analysis
The system shall analyze supported code dependencies and identify functions or components that may be affected by a change.

FR-03: Conflict Classification
The system shall classify detected conflicts according to the categories supported by the implementation.

FR-04: Conflict Risk Assessment
The system shall produce conflict risk information using the configured prediction or scoring mechanism.

FR-05: Compliance Validation
The system shall evaluate source code against the compliance rules implemented in the Compliance Engine.

FR-06: Resolution Suggestions
The system shall provide suggested resolutions for supported conflict types.

FR-07: Dashboard
The system shall present available analysis results through a user interface.

FR-08: Command-Line Execution
The system shall provide a command-line entry point for executing the configured analysis workflow.

FR-09: Automated Validation
The configured GitHub Actions workflow shall install project dependencies and execute the specified validation commands.

FR-10: Configuration History
The project shall use Git to track source code and documentation changes.

4. Non-Functional Requirements

NFR-01: Usability
The dashboard should present analysis results in an understandable format.

NFR-02: Maintainability
The project should use modular components so that individual analysis functions can be maintained separately.

NFR-03: Reliability
The system should report errors when required files, dependencies, or inputs are unavailable.

NFR-04: Performance
The system should complete analysis within a reasonable time for the supported project size.

NFR-05: Traceability
Git commits, branches, tags, and pull requests should support tracking of changes.

NFR-06: Security
The project should avoid exposing credentials or sensitive configuration information in source code.

5. Constraints

- Analysis capabilities depend on the supported programming language and implemented algorithms.
- Prediction quality depends on the available training data and model.
- Compliance results depend on the rules configured in the system.
- Resolution suggestions require developer review.
- Automated checks cannot guarantee the absence of all defects.

6. External Interfaces

User Interface: Streamlit dashboard.
Command-Line Interface: Python entry point "aurascm_cli.py".
Version Control Interface: Git and GitHub.
Automation Interface: GitHub Actions workflow.
Configuration Interface: Python dependencies specified in "requirements.txt".

7. Acceptance Criteria

1. The system executes its configured analysis workflow.
2. Supported semantic differences can be identified.
3. Dependency analysis produces results for supported source code.
4. The conflict prediction component produces its configured output.
5. The Compliance Engine evaluates configured rules.
6. The self-healing component provides suggestions for supported conflicts.
7. The dashboard displays available results.
8. The configured CI workflow executes successfully for valid test conditions.

8. Conclusion

AuraSCM aims to improve software configuration management by combining version control practices with semantic analysis, dependency impact analysis, conflict risk assessment, compliance checking, and resolution suggestions. It provides developers with additional information for making safer and more informed merge decisions.
