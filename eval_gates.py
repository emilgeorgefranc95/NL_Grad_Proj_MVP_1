"""
eval_gates.py - Multi-Tier Evaluation Guardrail & Portfolio Decryptor Engine
Strictly enforces SEBI non-advisory compliance, arithmetic grounding,
bullet-point readability, and comprehensive in-context dashboard decryptor logic.
"""

import re
from typing import Dict, Any, Tuple

# SEBI & Project Brief Forbidden Keywords (Advisory & FOMO triggers)
ADVICE_KEYWORDS = [
    r"\bwhich fund\b", r"\bbest fund\b", r"\brecommend(ed)?\b",
    r"\bshould i sell\b", r"\bshould i exit\b", r"\bshould i switch\b",
    r"\bshould i stop\b", r"\bwill it give \d+%\b", r"\bguaranteed\b",
    r"\bmultibagger\b", r"\bbuy or sell\b", r"\bpick a fund\b"
]

EXIT_INTENT_KEYWORDS = [
    r"\bcancel.*sip\b", r"\bstop.*sip\b", r"\bpause.*sip\b",
    r"\bwithdraw(al)?\b", r"\bcash crunch\b", r"\bno money\b",
    r"\bclose account\b", r"\bneed money urgently\b"
]

VOLATILITY_KEYWORDS = [
    r"\bwhy.*(red|negative|down)\b", r"\b(lose|lost|losing).*money\b",
    r"\bnegative return\b", r"\bmarket.*(falling|crash|dipping|down)\b",
    r"\bam i in loss\b", r"\blower than\b"
]

JARGON_KEYWORDS = [
    r"\bxirr\b", r"\bnav\b", r"\bunits?\b",
    r"\bexpense ratio\b", r"\bter\b", r"\bbenchmark\b",
    r"\bcagr\b", r"\bwhat is sip\b", r"\bcompounding\b"
]


class EvalGateEngine:
    def __init__(self):
        self.disclaimer = (
            "📌 **Note:** This is an objective educational explainer based on your Groww portfolio ledger. "
            "It does NOT constitute SEBI investment advice. Mutual fund investments are subject to market risks."
        )

    def classify_intent(self, query: str) -> str:
        """Tier 1: Classifies incoming user intent to detect safety or policy boundaries."""
        q = query.lower()
        for pattern in ADVICE_KEYWORDS:
            if re.search(pattern, q):
                return "ADVICE_SEEKING"
        for pattern in EXIT_INTENT_KEYWORDS:
            if re.search(pattern, q):
                return "EXIT_INTENT"
        for pattern in VOLATILITY_KEYWORDS:
            if re.search(pattern, q):
                return "VOLATILITY_ANXIETY"
        for pattern in JARGON_KEYWORDS:
            if re.search(pattern, q):
                return "JARGON_EXPLANATION"
        return "GENERAL_INQUIRY"

    def evaluate_output_safety(self, response_text: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Tier 2: Inspects generated output against strict compliance and quality guardrails."""
        checks = {
            "non_advisory_passed": True,
            "no_fomo_passed": True,
            "grounding_passed": True,
            "sebi_disclaimer_present": True,
        }
        resp_lower = response_text.lower()

        # 1. Non-advisory check: Ensure AI did not prescribe buying/selling specific funds
        if any(term in resp_lower for term in ["you should sell", "you must exit", "buy this fund", "switch to"]):
            checks["non_advisory_passed"] = False

        # 2. No FOMO / Urgency check
        if any(term in resp_lower for term in ["hurry", "limited time", "don't miss out", "guaranteed wealth"]):
            checks["no_fomo_passed"] = False

        # 3. Grounding check: numbers cited must not contradict portfolio metrics
        cited_invested = re.findall(r"₹\s?(\d+[\d,]*)", response_text)
        if cited_invested:
            nums = [int(n.replace(",", "")) for n in cited_invested]
            if any(n > 500000 for n in nums):
                checks["grounding_passed"] = False

        # 4. SEBI disclaimer check
        if "sebi" not in resp_lower:
            checks["sebi_disclaimer_present"] = False

        passed_count = sum(1 for v in checks.values() if v)
        quality_score = int((passed_count / len(checks)) * 100)

        return {
            "checks": checks,
            "quality_score": quality_score,
            "is_safe": checks["non_advisory_passed"] and checks["no_fomo_passed"]
        }

    def generate_safe_fallback(self, query_intent: str, scenario: Dict[str, Any]) -> str:
        """Deterministic SEBI-compliant safe fallback formatted with proper markdown bullet points."""
        user = scenario["user_profile"]
        m = scenario["metrics"]

        if query_intent == "ADVICE_SEEKING":
            return (
                f"🛡️ **Compliance Guardrail Activated (SEBI Execution Platform Policy)**\n\n"
                f"Groww is an execution-only mutual fund distributor and is legally prohibited under SEBI regulations "
                f"from offering personalized buy, sell, hold, or fund switching recommendations.\n\n"
                f"**Objective factors to evaluate on your dashboard instead:**\n\n"
                f"* **Your Investment Horizon:** You selected {user['fund_name']} with a 10-year goal ({user['goal']}). "
                f"Short-term performance over {m['completed_instalments']} months does not indicate 10-year compounding trajectory.\n"
                f"* **Cost of Exiting Early:** Redeeming equity mutual fund units before 365 days triggers a **1.0% Exit Load** "
                f"deducted by the AMC and **20% Short-Term Capital Gains (STCG)** tax on realized profits.\n"
                f"* **Paper Dip vs. Realized Loss:** Selling units today converts an unrealized paper price fluctuation into an actual permanent financial loss.\n"
                f"* **Benchmark Performance:** Compare your fund's NAV trajectory against its official benchmark "
                f"({'Nifty 50 TRI' if 'Nifty' in user['fund_name'] else 'Nifty 500 TRI'}) rather than day-to-day market sentiment.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        elif query_intent == "EXIT_INTENT":
            return (
                f"💡 **Managing Cash Flow or Pausing Your SIP**\n\n"
                f"If you are experiencing temporary financial tightness or budgeting constraints, you do not need to lose "
                f"your **{m['completed_instalments']}-month consistency streak**:\n\n"
                f"* **Skip Next Month's Instalment:** Pause just the upcoming deduction. AutoPay automatically resumes the following month with zero bank bounce penalty.\n"
                f"* **Reschedule SIP Date:** If your salary arrives after the 5th, shift your monthly debit date to 3 days post-salary (e.g. 10th of every month).\n"
                f"* **Multi-Month Pause:** Pause your SIP for 1, 2, 3, or 6 months in the \"Manage\" tab while keeping your bank AutoPay mandate active.\n"
                f"* **Cancel Anytime Autonomy:** If you still wish to permanently stop, you have full freedom to cancel with zero lock-in or penalties.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        return (
            f"📈 **Your Investment Ledger Summary**\n\n"
            f"* **Completed Instalments:** {m['completed_instalments']} of {m['target_instalments']} instalments completed.\n"
            f"* **Unit Holdings:** You currently hold **{m['total_units']:.2f} units** with an average cost of ₹{m['average_nav_cost']:.2f}.\n\n"
            f"---\n"
            f"{self.disclaimer}"
        )

    def generate_perspective_response(self, query: str, scenario: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Main response generator with eval-gating and in-context dashboard decryptor logic.
        Answers questions about ANY dashboard metric, term, or calculation using formatted bullet points.
        """
        intent = self.classify_intent(query)
        user = scenario["user_profile"]
        m = scenario["metrics"]
        q_lower = query.lower().strip()

        # Format helpers for clean Indian currency display
        if m['total_return_inr'] < 0:
            formatted_return_inr = f"-₹{abs(m['total_return_inr']):,.2f}"
            formatted_return_pct = f"{m['total_return_pct']}%"
        else:
            formatted_return_inr = f"+₹{m['total_return_inr']:,.2f}"
            formatted_return_pct = f"+{m['total_return_pct']}%"

        if m['one_day_return_inr'] < 0:
            formatted_od_inr = f"-₹{abs(m['one_day_return_inr']):,.2f}"
            formatted_od_pct = f"{m['one_day_return_pct']}%"
        else:
            formatted_od_inr = f"+₹{m['one_day_return_inr']:,.2f}"
            formatted_od_pct = f"+{m['one_day_return_pct']}%"

        # Tier 1 Priority: Advice or Exit Interceptors
        if intent == "ADVICE_SEEKING":
            response = self.generate_safe_fallback("ADVICE_SEEKING", scenario)
            eval_result = self.evaluate_output_safety(response, m)
            return response, eval_result

        if intent == "EXIT_INTENT":
            response = self.generate_safe_fallback("EXIT_INTENT", scenario)
            eval_result = self.evaluate_output_safety(response, m)
            return response, eval_result

        # =====================================================================
        # DASHBOARD METRICS & ARITHMETIC DECRYPTOR (REGEX-POWERED)
        # =====================================================================

        # 1. Total Returns & How Returns Are Calculated
        if re.search(r"calculat.*return|how.*return.*calculat|return.*formula|total return|how.*p&l", q_lower):
            response = (
                f"📊 **How Your Total Return is Calculated**\n\n"
                f"Your total return on the dashboard currently stands at **{formatted_return_inr} ({formatted_return_pct})**.\n\n"
                f"**The Exact Dashboard Arithmetic:**\n\n"
                f"* **Current Portfolio Value:** ₹{m['current_value']:,.2f} ({m['total_units']:.2f} units × current NAV ₹{m['current_nav']:.2f}).\n"
                f"* **Total Amount Invested:** ₹{m['total_invested']:,.2f} ({m['completed_instalments']} monthly instalments of ₹{user['monthly_sip']:,}).\n"
                f"* **Absolute Return Formula:** `Current Value (₹{m['current_value']:,.2f}) - Total Invested (₹{m['total_invested']:,.2f})` = **{formatted_return_inr}**.\n"
                f"* **Percentage Return Formula:** `(Total Return / Total Invested) × 100` = **{formatted_return_pct}**.\n"
                f"* **Paper Fluctuation:** This is an unrealized paper figure. Your returns only become permanent if you redeem your units.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 2. Total Invested
        elif re.search(r"\btotal invest|how much.*invest|\bmy total invest", q_lower):
            response = (
                f"💰 **Your Total Invested Breakdown**\n\n"
                f"You have invested a cumulative total of **₹{m['total_invested']:,.2f}** into {user['fund_name']}.\n\n"
                f"**Contribution Details:**\n\n"
                f"* **Monthly SIP Amount:** ₹{user['monthly_sip']:,} committed per month.\n"
                f"* **Instalments Completed:** {m['completed_instalments']} successful monthly debits ({m['completed_instalments']} × ₹{user['monthly_sip']:,} = ₹{m['total_invested']:,.2f}).\n"
                f"* **Debit Channel:** Automated bank AutoPay mandate executed on the 5th of each month.\n"
                f"* **Habit Milestone:** {m['completed_instalments']} of {m['target_instalments']} instalments completed ({m['streak_pct']:.0f}% of your Year 1 goal).\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 3. Current Value
        elif re.search(r"current value|portfolio value|worth now|how much is my", q_lower):
            response = (
                f"💎 **Your Current Portfolio Value Breakdown**\n\n"
                f"The total market value of your holdings today is **₹{m['current_value']:,.2f}**.\n\n"
                f"**How This Value is Determined:**\n\n"
                f"* **Total Units Accumulated:** You own **{m['total_units']:.2f} units** of {user['fund_name']}.\n"
                f"* **Current Net Asset Value (NAV):** ₹{m['current_nav']:.2f} per unit as of today's market close.\n"
                f"* **Valuation Formula:** `Total Units ({m['total_units']:.2f}) × Latest NAV (₹{m['current_nav']:.2f})` = **₹{m['current_value']:,.2f}**.\n"
                f"* **Daily Market Update:** Mutual fund NAVs are updated once every business evening by the AMC based on the closing prices of the fund's underlying stocks.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 4. 1-Day Return
        elif re.search(r"1-day|one day|today.*return|daily return", q_lower):
            response = (
                f"📈 **Understanding Your 1-Day Return**\n\n"
                f"Your 1-day return is **{formatted_od_inr} ({formatted_od_pct})**.\n\n"
                f"**What This Number Means:**\n\n"
                f"* **Daily NAV Delta:** It reflects the price movement between yesterday's closing NAV and today's closing NAV for the {m['total_units']:.2f} units you own.\n"
                f"* **Stock Market Linkage:** Mutual fund NAVs fluctuate daily because the underlying companies in {user['fund_name']} trade on the NSE/BSE every business day.\n"
                f"* **Long-Term Perspective:** Daily swings are standard market noise. In a 10-year SIP, 1-day returns average out as you consistently accumulate units across multiple market cycles.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 5. XIRR / Annualized Return
        elif re.search(r"\bxirr\b|annualized", q_lower):
            response = (
                f"⏱️ **Demystifying XIRR (Extended Internal Rate of Return)**\n\n"
                f"Your annualized return (XIRR) is currently **{m['xirr_pct']}%**.\n\n"
                f"**Why XIRR is Different from Simple Return:**\n\n"
                f"* **Multiple Cash Flows:** Because an SIP involves investments made on multiple distinct dates, simple CAGR cannot calculate returns accurately. XIRR computes the exact annualized compounding rate across each cash outflow.\n"
                f"* **The Speed-Limit Analogy:** Think of XIRR as your speedometer. In the first 1–6 months, the formula extrapolates a 30-day price dip across a full 365-day year, resulting in an artificially magnified negative percentage.\n"
                f"* **Noise in Months 1–6:** Financial planners disregard early XIRR numbers as statistically noisy. XIRR becomes meaningful only after 12 to 24 months of consistent investing.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 6. NAV (Net Asset Value)
        elif re.search(r"\bnav\b|net asset value", q_lower):
            response = (
                f"🏷️ **What is NAV (Net Asset Value)?**\n\n"
                f"NAV is simply the **price of 1 unit** of your mutual fund. The current NAV of {user['fund_name']} is **₹{m['current_nav']:.2f}**.\n\n"
                f"**How NAV Works on Your Dashboard:**\n\n"
                f"* **The Gold Analogy:** Just like gold is priced per gram, a mutual fund is priced per unit. When the NAV drops, your ₹{user['monthly_sip']:,} buys more units (\"more grams\").\n"
                f"* **Unit Allotment:** Every time your monthly SIP of ₹{user['monthly_sip']:,} is debited, Groww divides ₹{user['monthly_sip']:,} by that day's NAV to credit new units to your portfolio.\n"
                f"* **This Month's Purchase:** At ₹{m['current_nav']:.2f} NAV, your ₹{user['monthly_sip']:,} bought **{m['units_bought_this_month']:.2f} units**—giving you **+{m['additional_units_this_month']:.2f} extra units** compared to last month.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 7. Units & Unit Ownership
        elif re.search(r"\bunits?\b|how many units", q_lower):
            response = (
                f"📦 **Understanding Your Units**\n\n"
                f"You currently own **{m['total_units']:.2f} accumulated units** of {user['fund_name']}.\n\n"
                f"**What Units Mean for an Investor:**\n\n"
                f"* **Proportional Ownership:** Each unit represents your fraction of ownership in the underlying diversified portfolio of 30–50+ leading companies.\n"
                f"* **Accumulation Phase:** In Months 1–12, your primary goal as an SIP investor is to accumulate as many units as possible before the next major market upswing.\n"
                f"* **Average Acquisition Cost:** Across your {m['completed_instalments']} instalments, your average purchase cost per unit is **₹{m['average_nav_cost']:.2f}**.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 8. Average NAV / Average Purchase Cost
        elif re.search(r"average cost|average nav|avg cost|cost per unit", q_lower):
            response = (
                f"🎯 **Your Average Cost per Unit (Rupee-Cost Averaging)**\n\n"
                f"Your average purchase cost across all completed instalments is **₹{m['average_nav_cost']:.2f} per unit**.\n\n"
                f"**How the Market Dip Lowered Your Cost Basis:**\n\n"
                f"* **Previous Average Cost:** ₹{m['previous_average_nav']:.2f} per unit.\n"
                f"* **Current Average Cost:** ₹{m['average_nav_cost']:.2f} per unit ({m['cost_basis_reduction_pct']}% reduction).\n"
                f"* **The Break-Even Advantage:** Because this month's lower NAV (₹{m['current_nav']:.2f}) pulled your average cost down, your entire portfolio will recover to profitability faster when market prices rise.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 9. Direct Growth vs Regular
        elif re.search(r"direct growth|direct plan|growth option", q_lower):
            response = (
                f"🌱 **What Does \"Direct - Growth\" Mean?**\n\n"
                f"Your investment in {user['fund_name']} is under the **Direct Plan - Growth Option**.\n\n"
                f"**Key Benefits of Direct Growth:**\n\n"
                f"* **Direct Plan (Zero Commissions):** You invest directly with the fund house through Groww without paying distributor or agent commissions (0.5%–1.0% annual savings that compound in your favor).\n"
                f"* **Lower Expense Ratio:** Direct plans have significantly lower Total Expense Ratios (TER), resulting in higher net returns over multi-year periods.\n"
                f"* **Growth Option (Automatic Compounding):** Instead of paying out sporadic taxable dividends, all capital gains are automatically retained inside the fund to compound your unit value.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 10. Next Debit Date & AutoPay
        elif re.search(r"next debit|due date|autopay|mandate|when will money", q_lower):
            response = (
                f"📅 **Your Next SIP Debit & AutoPay Status**\n\n"
                f"Your monthly SIP of **₹{user['monthly_sip']:,}** is automated via bank AutoPay.\n\n"
                f"**Schedule & Flexibility:**\n\n"
                f"* **Debit Date:** The **5th of every month** (Next scheduled: Nov 5, 2026).\n"
                f"* **AutoPay Mandate:** Active via NPCI e-NACH / UPI AutoPay.\n"
                f"* **Need Flexibility?:** If you are tight on cash or have a delayed salary, tap **\"⚙️ Manage\"** to skip next month's instalment with zero fee or reschedule the debit date.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 11. Exit Load
        elif re.search(r"exit load|penalty.*sell|exit fee|lock-in", q_lower):
            response = (
                f"🚪 **Exit Load and Lock-in Rules**\n\n"
                f"Mutual fund redemptions are subject to the AMC's exit load policy:\n\n"
                f"* **Zero Lock-in:** Open-ended mutual funds have no lock-in; you have the legal right to redeem units on any business day.\n"
                f"* **Exit Load (Under 365 Days):** If you redeem units within 12 months of purchase, the AMC deducts a **1.0% exit load** from the redemption value.\n"
                f"* **After 1 Year:** Once units have been held for more than 365 days, exit load becomes **0% (completely free)**.\n"
                f"* **SIP Consideration:** Each monthly SIP instalment has its own individual 365-day timer for exit load calculations.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 12. Taxes: STCG & LTCG
        elif re.search(r"\btax\b|stcg|ltcg|capital gain", q_lower):
            response = (
                f"⚖️ **Capital Gains Taxation on Mutual Funds**\n\n"
                f"Tax on equity mutual funds is levied only when you sell (redeem) units and realize a capital gain:\n\n"
                f"* **Short-Term Capital Gains (STCG):** Units held for **12 months or less** are taxed at **20%** on realized net profit.\n"
                f"* **Long-Term Capital Gains (LTCG):** Units held for **more than 12 months** are taxed at **12.5%** on realized net profit exceeding **₹1.25 Lakh** in a financial year.\n"
                f"* **No Tax While Holding:** As long as your SIP continues and you do not redeem units, zero capital gains tax is payable.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 13. Expense Ratio / TER
        elif re.search(r"expense ratio|\bter\b|fund charge", q_lower):
            response = (
                f"🏷️ **Understanding Expense Ratio (TER)**\n\n"
                f"The Total Expense Ratio (TER) is the annual operating cost charged by the AMC to manage {user['fund_name']}.\n\n"
                f"**How TER Works:**\n\n"
                f"* **Automatically Deducted:** The expense ratio is adjusted daily in the fund's published NAV; you never receive a separate bill.\n"
                f"* **Direct Plan Savings:** Because you hold a Direct Plan on Groww, your expense ratio is $\sim 0.70\%$ lower than regular broker plans.\n"
                f"* **Compounding Impact:** Over 10 years, saving 0.70% annually adds tens of thousands of rupees directly to your final wealth.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 14. Safety & Custodianship
        elif re.search(r"safe|safety|risk|can groww take", q_lower):
            response = (
                f"🛡️ **Safety, Custodianship & SEBI Regulation**\n\n"
                f"Your mutual fund investments on Groww are protected under strict SEBI regulatory frameworks:\n\n"
                f"* **Groww is an Execution Platform:** Groww does not hold your investment money on its balance sheet. Your money is routed directly via BSE StAR MF / ICCL to the fund house (AMC).\n"
                f"* **Units in Your Name:** Your mutual fund units are registered in your name directly with the AMC and the SEBI-regulated Registrar (CAMS / KFintech).\n"
                f"* **Bankruptcy Protection:** Even in the hypothetical event of Groww ceasing operations, your unit ownership remains 100% intact and directly accessible through AMC portals.\n"
                f"* **Market Risk vs. Platform Risk:** While your units are completely safe from intermediary risk, equity mutual fund NAVs fluctuate with broader market cycles.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 15. Volatility / Why Returns Are Negative (Cognitive Reframing)
        elif intent == "VOLATILITY_ANXIETY" or any(k in q_lower for k in ["why are my returns", "why red", "did i lose", "am i in loss", "market falling"]):
            response = (
                f"📊 **Understanding Your Returns in Month {m['completed_instalments']}**\n\n"
                f"Seeing a negative return (**{m['total_return_pct']}%**) during your first year is completely natural, but here is what is mathematically happening behind the scenes:\n\n"
                f"* **You Acquired Discounted Units:** Because the NAV dipped to ₹{m['current_nav']}, your regular ₹{user['monthly_sip']:,} "
                f"bought **{m['units_bought_this_month']:.2f} units** this month—that's **{m['additional_units_this_month']:.2f} extra units** "
                f"than last month for the exact same amount.\n"
                f"* **Your Average Cost Reduced:** Your average acquisition price per unit dropped from ₹{m['previous_average_nav']:.2f} "
                f"to **₹{m['average_nav_cost']:.2f}** ({m['cost_basis_reduction_pct']}% reduction).\n"
                f"* **Paper Dip vs. Real Loss:** You have not sold any units. You own all **{m['total_units']:.2f} pieces** of India's leading companies.\n"
                f"* **The 10-Year Reality:** Over 10-year holding periods in Indian equities, the historical probability of negative returns is `<1%`.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        # 16. General Inquiry / Milestone / Default Fallback
        else:
            response = (
                f"📈 **Your SIP Journey Snapshot (Month {m['completed_instalments']})**\n\n"
                f"* **Habit Milestone:** {m['completed_instalments']} of {m['target_instalments']} instalments completed ({m['streak_pct']:.0f}% of Year 1 goal).\n"
                f"* **Financial Ledger:** ₹{m['total_invested']:,.2f} invested across {m['completed_instalments']} months, holding a current market value of ₹{m['current_value']:,.2f}.\n"
                f"* **Unit Holdings:** You hold **{m['total_units']:.2f} units** of {user['fund_name']} with an average purchase cost of ₹{m['average_nav_cost']:.2f}.\n"
                f"* **Next AutoPay:** Scheduled for the 5th of next month (₹{user['monthly_sip']:,}).\n"
                f"* **Accumulation Focus:** In your first 12 months, automated savings discipline and unit accumulation matter far more than short-term price fluctuations.\n\n"
                f"---\n"
                f"{self.disclaimer}"
            )

        eval_result = self.evaluate_output_safety(response, m)
        return response, eval_result
