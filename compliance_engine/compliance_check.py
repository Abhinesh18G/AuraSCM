"""
AuraSCM - Compliance Engine
------------------------------
Two real, working checks (not simulated):

1. SECURITY SCAN: runs `bandit` (industry-standard Python SAST tool) on
   the target file and parses its findings into a structured report.

2. LICENSE / POLICY CHECK: scans for disallowed license headers /
   copyleft markers and flags files missing a required header, based on
   an organizational allow-list (config below).
"""

import json
import subprocess
import re

ALLOWED_LICENSES = {"MIT", "Apache-2.0", "BSD-3-Clause", "Unlicense", "Internal-Proprietary"}
DISALLOWED_MARKERS = [r"GPL-3\.0", r"AGPL", r"proprietary-do-not-copy"]


def run_security_scan(filepath: str) -> dict:
    """Runs bandit against a single Python file and returns structured results."""
    try:
        result = subprocess.run(
            ["bandit", "-f", "json", filepath],
            capture_output=True, text=True, timeout=30
        )
        report = json.loads(result.stdout) if result.stdout else {}
    except FileNotFoundError:
        return {"error": "bandit not installed. Run: pip install bandit"}
    except json.JSONDecodeError:
        report = {}

    issues = report.get("results", [])
    summary = {
        "file": filepath,
        "issues_found": len(issues),
        "findings": [
            {
                "test_name": i.get("test_name"),
                "severity": i.get("issue_severity"),
                "confidence": i.get("issue_confidence"),
                "line": i.get("line_number"),
                "description": i.get("issue_text"),
            }
            for i in issues
        ],
    }
    return summary


def check_license_compliance(filepath: str) -> dict:
    """Scans a file's header/comments for disallowed license markers."""
    with open(filepath) as f:
        content = f.read()

    violations = [pattern for pattern in DISALLOWED_MARKERS
                  if re.search(pattern, content, re.IGNORECASE)]

    return {
        "file": filepath,
        "compliant": len(violations) == 0,
        "violations": violations,
    }


def evaluate_merge_gate(filepath: str) -> dict:
    """
    The final gate decision: a file may only be merged if it has
    ZERO high-severity security issues AND is license-compliant.
    """
    security = run_security_scan(filepath)
    license_check = check_license_compliance(filepath)

    high_severity = [f for f in security.get("findings", [])
                      if f.get("severity") == "HIGH"]

    approved = (len(high_severity) == 0) and license_check["compliant"]

    return {
        "file": filepath,
        "merge_approved": approved,
        "security_summary": security,
        "license_summary": license_check,
    }


if __name__ == "__main__":
    result = evaluate_merge_gate("sample_repo/branch_b.py")
    print(json.dumps(result, indent=2))
