"""
AuraSCM - Real GitHub CI/CD Pull Request Gate (CLI)
---------------------------------------------------
Runs automatically inside GitHub Actions on every Pull Request, or locally
between any two Git branches/files. Exits with code 1 to BLOCK the GitHub PR
merge if semantic conflicts, ML risk, or security/license violations are found.
"""
import sys
import os
import tempfile
import argparse

from semantic_engine.ast_diff import diff_versions
from dependency_graph.dep_analyzer import build_call_graph, blast_radius, dependency_depth
from conflict_prediction.predict import load_model, predict_risk
from compliance_engine.compliance_check import evaluate_merge_gate
from self_healing.suggest import suggest_resolution

BLOCKING_TYPES = {"SIGNATURE_MISMATCH", "LOGIC_DIVERGENCE", "REMOVED_IN_BRANCH_B"}

def analyze_files(file_a_path: str, file_b_path: str, display_name: str = "target.py") -> bool:
    with open(file_a_path, "r", encoding="utf-8") as f:
        code_a = f.read()
    with open(file_b_path, "r", encoding="utf-8") as f:
        code_b = f.read()

    print("=" * 65)
    print(f"🚀 AuraSCM GitHub PR Gate — Analyzing: {display_name}")
    print("=" * 65)

    # 1. Semantic Merge Engine
    conflicts = diff_versions(code_a, code_b)
    print(f"\n[1] SEMANTIC MERGE ENGINE: {len(conflicts)} conflict(s) detected")
    for c in conflicts:
        print(f"    ⚠️  {c.conflict_type} in `{c.function_name}` (heuristic risk: {c.risk_score})")

    # 2. Dependency Graph & 3. ML Predictor
    graph = build_call_graph(code_b)
    model = load_model()
    ml_flagged_risky = False

    print("\n[2 & 3] DEPENDENCY BLAST RADIUS & ML RISK PREDICTION:")
    if not conflicts:
        print("    ✅ No modified function conflicts to evaluate.")
    for c in conflicts:
        affected = blast_radius(graph, c.function_name)
        depth = dependency_depth(graph, c.function_name)
        features = {
            "lines_changed": len(c.branch_b_detail.splitlines()) or 1,
            "functions_touched": 1,
            "dependency_depth": depth,
            "signature_changed": 1 if c.conflict_type == "SIGNATURE_MISMATCH" else 0,
            "token_overlap_ratio": 1 - c.risk_score,
        }
        pred = predict_risk(features, model)
        if pred["prediction"] == "RISKY":
            ml_flagged_risky = True
        print(f"    🔍 `{c.function_name}` -> Blast Radius: {affected or 'none'} (depth={depth}) "
              f"| ML Verdict: {pred['prediction']} (prob={pred['risk_probability']})")

    # 4. Compliance Engine
    tmp_path = os.path.join(tempfile.gettempdir(), "_branch_b_ci_check.py")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(code_b)
    gate = evaluate_merge_gate(tmp_path)
    print(f"\n[4] COMPLIANCE ENGINE (Bandit SAST & License):")
    print(f"    🛡️  Approved: {gate['merge_approved']} | Issues Found: {gate['security_summary'].get('issues_found', 0)}")

    # 5. Self-Healing Engine
    if conflicts:
        print("\n[5] SELF-HEALING SUGGESTIONS:")
        for c in conflicts:
            print(f"    💡 `{c.function_name}`: {suggest_resolution(c)}")

    # Final Decision
    blocking = [c for c in conflicts if c.conflict_type in BLOCKING_TYPES]
    reasons = []
    if blocking:
        names = ", ".join(f"`{c.function_name}`" for c in blocking)
        reasons.append(f"Semantic conflict needs manual review ({names})")
    if not gate["merge_approved"]:
        reasons.append("Security/License compliance gate failed")
    if ml_flagged_risky:
        reasons.append("ML model predicted high merge risk")

    print("\n" + "=" * 65)
    if reasons:
        print("❌ FINAL VERDICT: MERGE BLOCKED")
        for r in reasons:
            print(f"   - {r}")
        print("=" * 65)
        return False
    else:
        print("✅ FINAL VERDICT: MERGE ALLOWED")
        print("=" * 65)
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AuraSCM GitHub CI/CD Gate")
    parser.add_argument("base_file", help="Path to Branch A (base/main) Python file")
    parser.add_argument("head_file", help="Path to Branch B (incoming PR) Python file")
    args = parser.parse_args()

    allowed = analyze_files(args.base_file, args.head_file, display_name=args.head_file)
    sys.exit(0 if allowed else 1)