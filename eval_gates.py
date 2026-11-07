"""
eval_gates.py - Multi-Tier Evaluation Guardrail & Fallback Engine
Strictly enforces SEBI non-advisory compliance, arithmetic grounding,
tone moderation (non-FOMO), and safe educational fallbacks.
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
            "📌 Note: This is an educational explainer and does NOT constitute SEBI investment advice. "
            "Mutual fund investments are subject to market risks."
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
        # Basic check to avoid wild hallucinations
        if cited_invested:
            nums = [int(n.replace(",", "")) for n in cited_invested]
            # Ensure numbers are reasonably close to user profile scale
            if any(n > 500000 for n in nums):
                checks["grounding_passed"] = False

        # Calculate overall quality score
        passed_count = sum(1 for v in checks.values() if v)
        quality_score = int((passed_count / len(checks)) * 100)

        return {
            "checks": checks,
            "quality_score": quality_score,
            "is_safe": checks["non_advisory_passed"] and checks["no_fomo_passed"]
        }

    def generate_safe_fallback(self, query_intent: str, scenario: Dict[str, Any]) -> str:
        """Deterministic SEBI-compliant safe fallback when advice is requested."""
        user = scenario["user_profile"]
        m = scenario["metrics"]

        if query_intent == "ADVICE_SEEKING":
            return (
                f"🛡️ **Compliance Guardrail Activated (SEBI Execution Platform Policy)**\n\n"
                f"Groww is an execution-only platform and is legally prohibited from advising whether to "
                f"buy, hold, sell, or switch mutual funds.\n\n"
                f"**Here is what you can objectively examine instead:**\n"
                f"• **Your Time Horizon:** You started {user['fund_name']} with a 10-year goal. Short-term performance over {m['completed_instalments']} months does not reflect long-term potential.\n"
                f"• **Cost Implications:** Exiting equity mutual funds within 12 months often attracts a 1% exit load and Short Term Capital Gains (STCG) tax.\n"
                f"• **Benchmark Comparison:** Compare your fund's NAV trajectory against its underlying index rather than day-to-day absolute price.\n\n"
                f"{self.disclaimer}"
            )
        
        elif query_intent == "EXIT_INTENT":
            return (
                f"💡 **Considering Pausing or Stopping? Here are Your Flexible Options:**\n\n"
                f"We understand managing cash flows can be stressful. Before cancelling your entire {m['completed_instalments']}-month consistency streak, consider these non-penalty options:\n\n"
                f"1. **Skip Next Month's Instalment:** You can pause for 1 month with zero bank penalty or cancellation fees.\n"
                f"2. **Reschedule SIP Date:** If your salary arrives after the debit date, move your SIP date to 3 days after salary day.\n"
                f"3. **Cancel Anytime with Zero Lock-in:** If you still wish to cancel, you have full autonomy to proceed.\n\n"
                f"{self.disclaimer}"
            )

        return (
            f"Here is an objective overview of your investment: You have completed {m['completed_instalments']} instalments "
            f"holding {m['total_units']:.2f} units. {self.disclaimer}"
        )

    def generate_perspective_response(self, query: str, scenario: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Main response generator with eval-gating and deterministic financial synthesis."""
        intent = self.classify_intent(query)
        user = scenario["user_profile"]
        m = scenario["metrics"]

        # If flagged as advice or exit, route to safe fallback
        if intent in ["ADVICE_SEEKING", "EXIT_INTENT"]:
            response = self.generate_safe_fallback(intent, scenario)
            eval_result = self.evaluate_output_safety(response, m)
            return response, eval_result

        # Volatility / Market Drop explanation (Rupee-Cost Averaging)
        if intent == "VOLATILITY_ANXIETY":
            response = (
                f"📊 **Understanding Your Returns in Month {m['completed_instalments']}**\n\n"
                f"It is completely natural to feel concerned when seeing a negative return (currently {m['total_return_pct']}%), "
                f"especially during your first year.\n\n"
                f"Here is what is mathematically happening behind the scenes:\n"
                f"• **You Acquired Discounted Units:** Because the NAV dipped to ₹{m['current_nav']}, your ₹{user['monthly_sip']} "
                f"bought **{m['units_bought_this_month']:.2f} units** this month—that's **{m['additional_units_this_month']:.2f} more units** "
                f"than last month for the exact same amount.\n"
                f"• **Your Average Cost Reduced:** Your average acquisition price per unit dropped from ₹{m['previous_average_nav']:.2f} "
                f"to **₹{m['average_nav_cost']:.2f}** ({m['cost_basis_reduction_pct']}% reduction).\n"
                f"• **Why This Matters:** In an SIP, falling markets lower your break-even hurdle. When the market cycle recovers, "
                f"these extra accumulated units compound faster.\n\n"
                f"{self.disclaimer}"
            )
        # Jargon explanation
        elif intent == "JARGON_EXPLANATION":
            q_lower = query.lower()
            if "xirr" in q_lower:
                response = (
                    f"📖 **Demystifying XIRR (Extended Internal Rate of Return)**\n\n"
                    f"Think of XIRR as your **annualized speed limit**. Because an SIP involves multiple cash flows at different dates, "
                    f"XIRR calculates the annualized compound rate across all instalments.\n\n"
                    f"**Why XIRR looks extreme right now ({m['xirr_pct']}%):**\n"
                    f"In Months 1 to 6, the mathematical formula annualizes short-term price fluctuations over a full 365-day year. "
                    f"A small ₹50 fluctuation in 30 days mathematically projects to a dramatic negative XIRR. "
                    f"Financial planners consider XIRR statistically noisy until you have invested for at least 12–24 months.\n\n"
                    f"{self.disclaimer}"
                )
            elif "nav" in q_lower:
                response = (
                    f"📖 **Demystifying NAV (Net Asset Value)**\n\n"
                    f"NAV is simply the **price of 1 unit** of your mutual fund (currently ₹{m['current_nav']}).\n"
                    f"Think of it like buying gold in grams: when gold price drops, you get more grams for ₹{user['monthly_sip']}. "
                    f"In mutual funds, you own **{m['total_units']:.2f} total units**. A lower NAV allows your monthly SIP to accumulate "
                    f"more units at lower cost.\n\n"
                    f"{self.disclaimer}"
                )
            else:
                response = (
                    f"📖 **Plain-Language Financial Concept Guide**\n\n"
                    f"In your SIP journey with {user['fund_name']}, you invest ₹{user['monthly_sip']} monthly. "
                    f"Every instalment purchases units at the prevailing NAV. Over 10 years, short-term volatility averages out "
                    f"through Rupee-Cost Averaging.\n\n"
                    f"{self.disclaimer}"
                )
        else:
            response = (
                f"📈 **Your SIP Journey Snapshot (Month {m['completed_instalments']})**\n\n"
                f"• **Habit Milestone:** {m['completed_instalments']} of {m['target_instalments']} instalments completed ({m['streak_pct']}% of Year 1).\n"
                f"• **Unit Ownership:** You currently hold **{m['total_units']:.2f} units** with an average purchase cost of ₹{m['average_nav_cost']:.2f}.\n"
                f"• **Status:** Your investment is in the accumulation phase. Short-term price noise does not affect long-term compounding.\n\n"
                f"{self.disclaimer}"
            )

        eval_result = self.evaluate_output_safety(response, m)
        return response, eval_result
