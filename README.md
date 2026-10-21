# AuraSCM — Working MVP

AI-Driven Semantic Merge Conflict Prediction, Compliance Enforcement, and
Self-Healing Configuration Management System.

This is a **working, runnable MVP** covering all 5 modules from your SRS,
scaled to what's realistically buildable and demoable in 2 days. Every
module here actually executes — nothing is faked or hardcoded to "look"
like it works.

## What's real vs. simplified (be upfront about this in your viva/demo)

| Module | What's genuinely working | Simplification vs. a production system |
|---|---|---|
| Semantic Merge Engine | Real AST parsing (`ast` module), structural hashing, signature/body comparison | Only single-file Python; no cross-file semantic analysis |
| Dependency Graph Analyzer | Real call-graph built with `networkx`, blast-radius via graph traversal | Static call detection only (no dynamic dispatch, no imports across files) |
| Conflict Prediction (ML) | Real trained `scikit-learn` Logistic Regression, train/test split, accuracy report | Trained on synthetic data (400 rows) since no real Git history was available — documented as a limitation, not hidden |
| Compliance Engine | Real `bandit` security scan (industry SAST tool) + real regex license check | License list is a small allow-list, not full SPDX parsing |
| Self-Healing Engine | Real rule-based suggestion generator, deterministic and explainable | Rule-based, not LLM-generated (documented as "Phase 2" in your report) |
| Dashboard | Real interactive Streamlit app tying all modules together | — |

Framing it this way in your report/viva is a strength, not a weakness —
it shows you understand engineering tradeoffs under a deadline.

## Project structure
```
AuraSCM/
├── semantic_engine/ast_diff.py        # Module 1: AST-based semantic diff
├── dependency_graph/dep_analyzer.py   # Module 2: call graph + blast radius
├── conflict_prediction/predict.py     # Module 3: ML risk model
├── compliance_engine/compliance_check.py  # Module 4: security + license gate
├── self_healing/suggest.py            # Module 5: resolution suggestions
├── dashboard/app.py                   # Streamlit UI tying it all together
├── data/generate_dataset.py           # synthetic merge-history generator
├── data/merge_history.csv             # generated training data
├── sample_repo/branch_a.py            # demo conflict: branch A
├── sample_repo/branch_b.py            # demo conflict: branch B
└── requirements.txt
```

## Setup (5 minutes)
```bash
cd AuraSCM
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run each module standalone (to verify + for screenshots in your report)
```bash
# 1. Semantic conflict detection
python3 semantic_engine/ast_diff.py

# 2. Dependency graph / blast radius
python3 dependency_graph/dep_analyzer.py

# 3. Generate training data, then train + test the ML model
python3 data/generate_dataset.py
python3 conflict_prediction/predict.py

# 4. Compliance / security gate
python3 compliance_engine/compliance_check.py

# 5. Self-healing suggestions (run from project root)
python3 -c "
from semantic_engine.ast_diff import diff_versions
from self_healing.suggest import suggest_resolution
a = open('sample_repo/branch_a.py').read()
b = open('sample_repo/branch_b.py').read()
for c in diff_versions(a, b):
    print(suggest_resolution(c))
"
```

## Run the full dashboard (this is your live demo)
```bash
streamlit run dashboard/app.py
```
This opens a browser UI where you paste/edit two branch versions and hit
"Run AuraSCM Merge Analysis" — it walks through all 5 modules live and
gives a final MERGE ALLOWED / MERGE BLOCKED verdict. **Use this for your
demo/viva**, it's the most impressive part.

---

## Your 2-day execution plan

### Day 1
- [ ] Hour 0–1: Set up repo, venv, run `pip install -r requirements.txt`, confirm every script above runs without errors
- [ ] Hour 1–2: Read through `ast_diff.py` and `dep_analyzer.py` until you can explain, in your own words, how AST comparison differs from Git's line-based diff (this WILL be asked in viva)
- [ ] Hour 2–4: Create 2–3 more sample conflict pairs like `branch_a.py`/`branch_b.py` (e.g. a signature-mismatch case, a removed-function case) to show your engine handles multiple conflict types, not just one
- [ ] Hour 4–6: Run the dashboard, take screenshots of each of the 5 sections for your report
- [ ] Hour 6–7: Start the SRS/report doc reusing your uploaded document's structure, filling in the "Configuration Identification" and "Development Methodology" sections (already drafted)

### Day 2
- [ ] Hour 0–2: Write the Design section — draw a simple architecture diagram (5 boxes: Semantic Engine → Dependency Graph → ML Predictor → Compliance Gate → Self-Healing, with Dashboard on top) using draw.io or PowerPoint
- [ ] Hour 2–3: Write Test Plan section — list the test cases you already have (signature mismatch, logic divergence, removed function, security scan clean/dirty, license violation) as a table with expected vs actual result
- [ ] Hour 3–4: Write Results/Evaluation section — include your ML model's accuracy report and a note on the synthetic-data limitation (shows maturity)
- [ ] Hour 4–5: Practice your live demo end-to-end 2–3 times so it's smooth
- [ ] Hour 5–6: Final polish — README, code comments, zip the repo
- [ ] Hour 6+: Buffer for fixing anything that breaks

## Likely viva questions — be ready for these
1. **"How is this different from Git's merge conflict detection?"** → Git compares text lines; we parse code into ASTs and compare structure/behavior, so we catch conflicts even when the changed lines don't textually overlap (show the `branch_a.py`/`branch_b.py` example — same lines, different meaning).
2. **"Is your ML model really learning, or is it just rules?"** → It's a real Logistic Regression trained via `scikit-learn` on labeled data with a train/test split — show `predict.py`'s output. Be honest that training data is synthetic due to time constraints.
3. **"What does bandit actually check?"** → It's a real static analysis security tool that scans Python code for common vulnerability patterns (hardcoded passwords, SQL injection risk, use of `eval`, etc.) — not something you wrote yourself, which is a legitimate design choice (reuse proven tools rather than reinvent security scanning).
4. **"What would you build next / Phase 2?"** → Cross-file semantic analysis, real Git-history mining for training data, LLM-generated (not just rule-based) self-healing suggestions.
