"""AuraSCM Dashboard — With Live GitHub Repository & Branch Integration"""
import sys
import os
import tempfile
import urllib.request
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from semantic_engine.ast_diff import diff_versions
from dependency_graph.dep_analyzer import build_call_graph, blast_radius, dependency_depth
from conflict_prediction.predict import load_model, predict_risk
from compliance_engine.compliance_check import evaluate_merge_gate
from self_healing.suggest import suggest_resolution

BLOCKING_TYPES = {"SIGNATURE_MISMATCH", "LOGIC_DIVERGENCE", "REMOVED_IN_BRANCH_B"}

st.set_page_config(page_title="AuraSCM — GitHub App & Merge Gate", layout="wide")
st.title("AuraSCM — AI-Driven GitHub Semantic Merge & Compliance Gate")
st.caption("Live GitHub Pull Request / Branch Inspector & CI/CD Pre-Merge Gate")

def fetch_github_file(repo: str, branch: str, filepath: str) -> str:
    """Fetches a raw Python file directly from GitHub."""
    url = f"https://raw.githubusercontent.com/{repo}/{branch}/{filepath}"
    req = urllib.request.Request(url, headers={"User-Agent": "AuraSCM-App"})
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.read().decode("utf-8")

st.sidebar.header("🔌 Input Source")
mode = st.sidebar.radio(
    "Choose how to load code:",
    ["🔗 Live GitHub Repository", "💻 Local Demo / Paste Code"]
)

default_a = open("sample_repo/branch_a.py").read()
default_b = open("sample_repo/branch_b.py").read()

if mode == "🔗 Live GitHub Repository":
    st.sidebar.subheader("GitHub Repo Settings")
    gh_repo = st.sidebar.text_input("GitHub Repo (owner/repo)", value="your-username/AuraSCM")
    gh_branch_a = st.sidebar.text_input("Base Branch (Branch A)", value="main")
    gh_branch_b = st.sidebar.text_input("PR / Feature Branch (Branch B)", value="feature-discount")
    gh_filepath = st.sidebar.text_input("Python File Path in Repo", value="sample_repo/branch_a.py")

    if st.sidebar.button("📥 Fetch Branches from GitHub"):
        try:
            st.session_state["code_a"] = fetch_github_file(gh_repo, gh_branch_a, gh_filepath)
            st.session_state["code_b"] = fetch_github_file(gh_repo, gh_branch_b, gh_filepath)
            st.sidebar.success(f"Fetched `{gh_filepath}` from `{gh_branch_a}` and `{gh_branch_b}`!")
        except Exception as e:
            st.sidebar.error(f"Could not fetch from GitHub: {e}")

code_a_init = st.session_state.get("code_a", default_a)
code_b_init = st.session_state.get("code_b", default_b)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Branch A (Base / `main`)")
    code_a = st.text_area("branch_a.py", code_a_init, height=320)
with col2:
    st.subheader("Branch B (Incoming PR Branch)")
    code_b = st.text_area("branch_b.py", code_b_init, height=320)

if st.button("🚀 Run AuraSCM Merge Analysis", type="primary"):
    st.header("1️⃣ Semantic Merge Engine")
    try:
        conflicts = diff_versions(code_a, code_b)
    except SyntaxError as e:
        st.error(f"Syntax error while parsing: {e}")
        st.stop()

    if not conflicts:
        st.success("No semantic conflicts detected.")
    for c in conflicts:
        st.warning(f"**{c.conflict_type}** in `{c.function_name}` "
                   f"(heuristic risk: {c.risk_score})")

    st.header("2️⃣ Dependency Graph Analyzer")
    graph = build_call_graph(code_b)
    for c in conflicts:
        affected = blast_radius(graph, c.function_name)
        depth = dependency_depth(graph, c.function_name)
        st.write(f"`{c.function_name}` blast radius: "
                 f"{affected if affected else 'none'} (depth={depth})")

    st.header("3️⃣ Conflict Prediction (ML)")
    model = load_model()
    ml_flagged_risky = False
    for c in conflicts:
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
        st.write(f"`{c.function_name}` → **{pred['prediction']}** "
                 f"(probability={pred['risk_probability']})")

    st.header("4️⃣ Compliance Engine")
    tmp_path = os.path.join(tempfile.gettempdir(), "_branch_b_check.py")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(code_b)
    gate = evaluate_merge_gate(tmp_path)
    if gate["merge_approved"]:
        st.success("Compliance gate: PASSED (no high-severity issues, license OK)")
    else:
        st.error("Compliance gate: BLOCKED")
    st.json(gate)

    st.header("5️⃣ Self-Healing Suggestions")
    for c in conflicts:
        st.info(f"**{c.function_name}**: {suggest_resolution(c)}")

    st.header("✅ Final Merge Decision")
    blocking = [c for c in conflicts if c.conflict_type in BLOCKING_TYPES]
    reasons = []
    if blocking:
        names = ", ".join(f"`{c.function_name}`" for c in blocking)
        reasons.append(f"semantic conflict needs manual review: {names}")
    if not gate["merge_approved"]:
        reasons.append("compliance gate failed")
    if ml_flagged_risky:
        reasons.append("ML model predicts a risky merge")

    if reasons:
        st.error("MERGE BLOCKED — " + "; ".join(reasons))
    else:
        st.success("MERGE ALLOWED")