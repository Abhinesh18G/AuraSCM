"""
AuraSCM - Self-Healing Recommendation Engine
-----------------------------------------------
Takes the SemanticConflict objects from the semantic engine and produces
human-readable resolution suggestions. Implemented as a rule-based
expert system (transparent, deterministic, and explainable -- a good
fit for a course-project "self-healing" module, and easy to extend
later with an LLM call for free-text suggestions).
"""

TEMPLATES = {
    "SIGNATURE_MISMATCH": (
        "Function `{name}` was changed with two different signatures. "
        "Recommend: unify to the superset of parameters "
        "({branch_a} vs {branch_b}) and add default values so both "
        "call-sites remain valid. Re-run tests on all callers."
    ),
    "LOGIC_DIVERGENCE": (
        "Function `{name}` has conflicting logic changes across branches. "
        "Recommend: manual review required -- present both implementations "
        "side-by-side to the developer and ask which business rule is "
        "correct, since this cannot be auto-resolved safely."
    ),
    "REMOVED_IN_BRANCH_B": (
        "Function `{name}` was deleted in one branch but still referenced "
        "elsewhere. Recommend: block merge until all call-sites are "
        "updated or the function is restored."
    ),
    "ADDED_IN_BRANCH_B_ONLY": (
        "Function `{name}` is new in this branch. Recommend: standard "
        "review, no conflict action needed."
    ),
}


def suggest_resolution(conflict) -> str:
    """conflict is a SemanticConflict from semantic_engine.ast_diff"""
    template = TEMPLATES.get(conflict.conflict_type,
                              "No suggestion available for `{name}`.")
    return template.format(
        name=conflict.function_name,
        branch_a=conflict.branch_a_detail,
        branch_b=conflict.branch_b_detail,
    )


if __name__ == "__main__":
    import sys
    sys.path.append("..")
    from semantic_engine.ast_diff import diff_versions

    with open("sample_repo/branch_a.py") as f:
        src_a = f.read()
    with open("sample_repo/branch_b.py") as f:
        src_b = f.read()

    conflicts = diff_versions(src_a, src_b)
    for c in conflicts:
        print(f"\n[{c.conflict_type}] {c.function_name}")
        print("Suggestion:", suggest_resolution(c))
