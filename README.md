# Groww Perspective: AI-Native SIP Retention Companion

> **NextLeap Product Management Graduation Project (Growth Track)**  
> **North Star Metric:** Increase the % of first-time mutual fund investors who still have an active SIP 12 months after starting their first one.

---

## 🌟 Overview
**Groww Perspective** is an in-app, eval-gated AI companion designed for first-time retail investors on Groww. It tackles the **"Post-Onboarding Conviction Deficit"** during the critical Month 2–6 drop-off window by:
1. Translating confusing financial telemetry (NAV, XIRR, red/green P&L) into **plain-language monthly debriefs**.
2. Demonstrating the superpower of **Rupee-Cost Averaging** (buying discounted units during market dips).
3. Providing an **eval-gated "Ask About My SIP" assistant** that strictly refuses investment advice while offering clear, reassuring financial education.
4. Surfacing a **Smart Exit Flexibility Flow** that prevents premature churn due to short-term cash crunches.

---

## 🏗️ Technical & Compliance Architecture

```
User Query / Session Open
            │
            ▼
┌───────────────────────────────────────┐
│ Tier 1: Input Intent & Policy Gate    │──► [Advisory Trap Detected] ──► Block & Serve Safe Fallback
└───────────────────────────────────────┘
            │ (Pass)
            ▼
┌───────────────────────────────────────┐
│ Deterministic Ledger Engine           │ (Zero arithmetic hallucination; all math computed via code)
└───────────────────────────────────────┘
            │ (Verified JSON Context)
            ▼
┌───────────────────────────────────────┐
│ Plain-Language Synthesis Engine       │ (Patient Financial Coach tone)
└───────────────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────┐
│ Tier 2: Output Eval & Quality Gate    │──► [Non-Advisory Check, Non-FOMO Check, Arithmetic Grounding]
└───────────────────────────────────────┘
            │ (Pass: Score 100/100)
            ▼
Render with Visible Quality Badge & Telemetry Inspector
```

---

## 🚀 How to Run Locally

1. **Clone or navigate to this folder:**
   ```bash
   cd "Antigravity - project folder"
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Launch the application:**
   ```bash
   streamlit run app.py
   ```
   Open your browser at `http://localhost:8501`.

---

## 🌐 1-Click Deployment to Production (For Mentors)

To get a publicly clickable URL for mentors (e.g. `https://groww-perspective.streamlit.app`):
1. Push this repository to **GitHub** (public repo).
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub account, select this repository, set Main file path to `app.py`, and click **Deploy**.
4. You now have a live, production-deployed link to put in your deck and submission form!

---

## 📁 Repository Structure
* [`app.py`](app.py): The interactive Streamlit web application.
* [`eval_gates.py`](eval_gates.py): The multi-tier guardrail and safe fallback engine.
* [`portfolio_data.py`](portfolio_data.py): Deterministic financial models and realistic beginner portfolios.
* [`golden_set.py`](golden_set.py): Automated benchmark script for the 20 test cases.
* [`golden_set_results.json`](golden_set_results.json): Benchmark execution results (100% agreement).
* [`ai_evidence_log.md`](ai_evidence_log.md): Official AI Evidence Log deliverable.
* [`user_interviews.md`](user_interviews.md): Primary user research notes (5 detailed interviews).
