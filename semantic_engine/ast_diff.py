"""
AuraSCM - Semantic Merge Engine
--------------------------------
Parses two versions of a Python file into Abstract Syntax Trees (ASTs)
and detects SEMANTIC conflicts -- cases where the same function/class was
modified differently on two branches, even if a text-based `git diff`
would not flag an overlapping-line conflict.

This is the core novelty piece of the project: instead of comparing raw
text lines (like Git), we compare the *structure and behavior* of code.
"""

import ast
import hashlib
from dataclasses import dataclass, field


@dataclass
class FunctionSignature:
    name: str
    args: list
    defaults: list
    body_hash: str
    body_source: str
    lineno: int


@dataclass
class SemanticConflict:
    function_name: str
    conflict_type: str
    branch_a_detail: str
    branch_b_detail: str
    risk_score: float


def _hash_node(node: ast.AST) -> str:
    """Structural hash of an AST subtree, ignoring line numbers/whitespace."""
    dump = ast.dump(node, annotate_fields=False, include_attributes=False)
    return hashlib.sha256(dump.encode()).hexdigest()[:16]


def extract_functions(source_code: str) -> dict:
    """Parse source into a dict of {function_name: FunctionSignature}."""
    tree = ast.parse(source_code)
    functions = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = [a.arg for a in node.args.args]
            defaults = [ast.dump(d) for d in node.args.defaults]
            functions[node.name] = FunctionSignature(
                name=node.name,
                args=args,
                defaults=defaults,
                body_hash=_hash_node(node),
                body_source=ast.unparse(node),
                lineno=node.lineno,
            )
    return functions


def diff_versions(source_a: str, source_b: str) -> list:
    """
    Compare two versions of the same file semantically.
    Returns a list of SemanticConflict objects.
    """
    funcs_a = extract_functions(source_a)
    funcs_b = extract_functions(source_b)

    conflicts = []
    shared_names = set(funcs_a.keys()) & set(funcs_b.keys())

    for name in shared_names:
        fa, fb = funcs_a[name], funcs_b[name]

        # Case 1: signature changed differently (breaking change risk)
        if fa.args != fb.args:
            conflicts.append(SemanticConflict(
                function_name=name,
                conflict_type="SIGNATURE_MISMATCH",
                branch_a_detail=f"args={fa.args}",
                branch_b_detail=f"args={fb.args}",
                risk_score=0.9,
            ))
            continue

        # Case 2: same signature, but body logic diverged
        if fa.body_hash != fb.body_hash:
            conflicts.append(SemanticConflict(
                function_name=name,
                conflict_type="LOGIC_DIVERGENCE",
                branch_a_detail=fa.body_source.strip(),
                branch_b_detail=fb.body_source.strip(),
                risk_score=_estimate_logic_risk(fa, fb),
            ))

    # Functions removed on one branch but still relied on
    only_in_a = set(funcs_a.keys()) - set(funcs_b.keys())
    only_in_b = set(funcs_b.keys()) - set(funcs_a.keys())
    for name in only_in_a:
        conflicts.append(SemanticConflict(
            function_name=name,
            conflict_type="REMOVED_IN_BRANCH_B",
            branch_a_detail="present",
            branch_b_detail="deleted",
            risk_score=0.7,
        ))
    for name in only_in_b:
        conflicts.append(SemanticConflict(
            function_name=name,
            conflict_type="ADDED_IN_BRANCH_B_ONLY",
            branch_a_detail="missing",
            branch_b_detail="new function",
            risk_score=0.4,
        ))

    return conflicts


def _estimate_logic_risk(fa: FunctionSignature, fb: FunctionSignature) -> float:
    """
    Very simple heuristic risk scorer used as a feature for the ML model:
    more differing tokens between two versions of a function body -> higher risk.
    A real system would use embeddings; here we use a lightweight proxy
    that is transparent and explainable for a course project.
    """
    tokens_a = set(fa.body_source.split())
    tokens_b = set(fb.body_source.split())
    if not tokens_a and not tokens_b:
        return 0.1
    overlap = len(tokens_a & tokens_b) / max(len(tokens_a | tokens_b), 1)
    risk = round(1 - overlap, 2)
    return max(0.3, min(risk, 0.95))


if __name__ == "__main__":
    with open("sample_repo/branch_a.py") as f:
        src_a = f.read()
    with open("sample_repo/branch_b.py") as f:
        src_b = f.read()

    results = diff_versions(src_a, src_b)
    print(f"Found {len(results)} semantic conflict(s):\n")
    for c in results:
        print(f"  [{c.conflict_type}] function `{c.function_name}` "
              f"(risk={c.risk_score})")
