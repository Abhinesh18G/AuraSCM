AuraSCM — Low-Level Design (LLD)

Project Title: AuraSCM: AI-Driven Semantic Merge, Dependency Blast-Radius & Compliance Gate
Version: 1.0
Project Team: Abhinesh G and Madhan D

1. Introduction

1.1 Purpose

This document describes the detailed design of the main AuraSCM software modules, their responsibilities, inputs, processing steps, and outputs.

1.2 Scope

The LLD covers the semantic analysis, dependency graph, conflict prediction, compliance, self-healing, dashboard, and command-line components.

2. Module Structure

The project contains the following main module directories:

- "semantic_engine/"
- "dependency_graph/"
- "conflict_prediction/"
- "compliance_engine/"
- "self_healing/"
- "dashboard/"
- "data/"
- "sample_repo/"
- ".github/workflows/"

The precise implementation of each module should be verified against its source files.

3. Semantic Analysis Module

Location: "semantic_engine/"

Purpose

To compare supported source-code versions and identify differences relevant to conflict analysis.

Input

- Source code from Branch A.
- Source code from Branch B.

Processing

1. Read the two source-code versions.
2. Apply the implemented comparison logic.
3. Identify supported differences.
4. Return the detected differences to the calling component.

Output

A collection of detected differences for further processing.

Example Interface

The project includes a referenced function named "diff_versions" in "semantic_engine.ast_diff".

Example usage:

from semantic_engine.ast_diff import diff_versions

branch_a = open("sample_repo/branch_a.py").read()
branch_b = open("sample_repo/branch_b.py").read()

differences = diff_versions(branch_a, branch_b)
print(differences)

4. Dependency Graph Module

Location: "dependency_graph/"

Purpose

To represent supported dependencies between functions or software components and identify potentially affected components.

Input

Supported source-code and dependency information.

Processing

1. Identify supported dependency relationships.
2. Represent the relationships using the implemented graph structure.
3. Analyze relationships relevant to a detected change.
4. Report potentially affected components and dependency depth where supported.

Output

Dependency relationships and potential blast-radius information.

5. Conflict Prediction Module

Location: "conflict_prediction/"

Purpose

To classify supported conflicts and produce risk information.

Input

Features or change information produced by the configured analysis workflow.

Processing

1. Receive the supported input features.
2. Apply the configured prediction or scoring mechanism.
3. Produce the supported conflict category and risk output.

Output

Conflict classification and associated risk information.

The exact model, features, training procedure, and scoring thresholds must be documented from the actual implementation.

6. Compliance Engine

Location: "compliance_engine/"

Purpose

To evaluate supported code or project artifacts against configured compliance rules.

Input

Source files and applicable rules.

Processing

1. Receive the artifacts to be checked.
2. Evaluate the configured rules.
3. Record detected findings.
4. Produce the resulting compliance status.

Output

Compliance findings and validation status.

7. Self-Healing Module

Location: "self_healing/"

Purpose

To provide possible resolution suggestions for supported conflict types.

Input

A detected conflict produced by the semantic analysis workflow.

Processing

1. Receive the detected conflict.
2. Identify an applicable resolution suggestion.
3. Return the suggested resolution for developer review.

Output

Resolution advice.

Example Interface

The project includes a referenced function named "suggest_resolution" in "self_healing.suggest".

Example usage:

from semantic_engine.ast_diff import diff_versions
from self_healing.suggest import suggest_resolution

branch_a = open("sample_repo/branch_a.py").read()
branch_b = open("sample_repo/branch_b.py").read()

differences = diff_versions(branch_a, branch_b)

for conflict in differences:
    print(suggest_resolution(conflict))

8. Dashboard Module

Location: "dashboard/"

Purpose

To present the analysis results through a user interface.

Main Responsibilities

- Present supported conflict information.
- Display risk and dependency information where available.
- Display compliance results where integrated.
- Present resolution suggestions where integrated.

The exact dashboard inputs and output fields depend on the implemented interface.

9. Command-Line Interface

File: "aurascm_cli.py"

Purpose

To execute the configured analysis and validation workflow from the command line.

Processing

1. Start the CLI.
2. Execute the configured analysis steps.
3. Report findings and validation results.
4. Return the configured process exit status.

Example Command

python aurascm_cli.py

The exit status and failure conditions should match the actual implementation.

10. Automated Validation

Workflow: ".github/workflows/aurascm.yml"

The configured GitHub Actions workflow performs the following steps:

1. Checks out the repository.
2. Sets up the configured Python version.
3. Installs dependencies from "requirements.txt".
4. Executes the dataset-generation script.
5. Executes the AuraSCM CLI validation command.

Example commands from the workflow:

pip install -r requirements.txt
python data/generate_dataset.py
python aurascm_cli.py

A failing validation step can cause the workflow to fail. Merge blocking depends on the repository's branch protection or ruleset configuration.

11. Error Handling

The system should handle relevant operational errors, including:

- Missing source files.
- Missing Python dependencies.
- Invalid or unsupported source-code input.
- Failed compliance checks.
- Exceptions during analysis.
- Failed automated validation.

Actual error-handling behavior depends on the implemented code.

12. Testing Considerations

The following scenarios can be used to evaluate the system:

Test ID| Scenario| Expected Result
T1| Branches contain supported logic divergence| The system identifies the difference and reports the configured conflict result.
T2| Both branches contain identical code| No semantic differences are reported for the identical input.
T3| A supported function signature changes| The system reports a mismatch if that change is covered by its implemented detection logic.
T4| A compliance rule is violated| The Compliance Engine reports the configured finding.
T5| A supported conflict is passed to the resolution module| The module returns an applicable suggestion or a supported fallback result.

Actual test outcomes must be recorded from executed tests.

13. Conclusion

The low-level design describes the responsibilities and interfaces of AuraSCM's principal modules. It provides a basis for implementation, testing, maintenance, and configuration auditing.
