"""
app.py - Groww Perspective: Interactive AI-Native SIP Retention Companion
Multi-screen, highly interactive Groww prototype with Story Mode, 
Rupee-Cost Averaging Simulator, Eval-Gated Chat, and Smart Exit Flow.
"""

import streamlit as st
import time
import os
import base64
from portfolio_data import SCENARIOS, get_scenario
from eval_gates import EvalGateEngine

# Load official Groww brand logo
logo_path = os.path.join(os.path.dirname(__file__), "groww_logo.png")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        groww_logo_uri = f"data:image/png;base64,{logo_b64}"
else:
    groww_logo_uri = "https://groww.in/groww-logo-270.png"

# Set page configuration with official Groww icon
st.set_page_config(
    page_title="Groww | Mutual Funds & SIP Companion",
    page_icon=logo_path if os.path.exists(logo_path) else "https://groww.in/groww-logo-270.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Groww aesthetic CSS - High Contrast Theme Enforcement
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background-color: #F4F6F9 !important;
        color: #191C1F !important;
    }
    
    /* Force high-contrast dark text on ALL headings, paragraphs, and markdown */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #191C1F !important;
    }
    
    /* Secondary and caption text in readable charcoal */
    .stCaption, [data-testid="stCaptionContainer"], small {
        color: #555B68 !important;
        font-weight: 500 !important;
    }
    
    /* White Card Containers with crisp borders & subtle drop shadow */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #DCE1E7 !important;
        border-radius: 14px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        padding: 0.5rem !important;
    }
    
    /* Text inside bordered cards */
    [data-testid="stVerticalBlockBorderWrapper"] h1,
    [data-testid="stVerticalBlockBorderWrapper"] h2,
    [data-testid="stVerticalBlockBorderWrapper"] h3,
    [data-testid="stVerticalBlockBorderWrapper"] h4,
    [data-testid="stVerticalBlockBorderWrapper"] p,
    [data-testid="stVerticalBlockBorderWrapper"] span {
        color: #191C1F !important;
    }
    
    .groww-logo {
        color: #00A87E !important;
        font-weight: 800 !important;
        font-size: 1.7rem !important;
        letter-spacing: -0.5px !important;
    }
    
    /* Badge styling */
    .badge-verified {
        background: #E6F9F4 !important;
        color: #007A5E !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        border: 1.5px solid #8DE3CE !important;
        display: inline-block !important;
    }
    
    /* Metric styling */
    .negative-metric {
        color: #D32F2F !important;
        font-weight: 700 !important;
        font-size: 1.35rem !important;
    }
    
    .positive-metric {
        color: #00875A !important;
        font-weight: 700 !important;
        font-size: 1.35rem !important;
    }
    
    /* Buttons styling - Groww Emerald Green */
    .stButton > button[kind="primary"] {
        background-color: #00D09C !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
    }
    
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        color: #191C1F !important;
    }
    
    /* Sidebar text high contrast */
    [data-testid="stSidebar"] {
        background-color: #181A20 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #F0F2F5 !important;
    }
    [data-testid="stSidebar"] .stCaption, [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #A0A6B2 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize engine & session state
engine = EvalGateEngine()

if "current_screen" not in st.session_state:
    st.session_state.current_screen = "📱 Dashboard"
if "story_step" not in st.session_state:
    st.session_state.story_step = 0
if "sip_query" not in st.session_state:
    st.session_state.sip_query = ""
if "skipped_month" not in st.session_state:
    st.session_state.skipped_month = False

# --- SIDEBAR: Scenario Switcher & Controls ---
with st.sidebar:
    st.markdown("### 🎛️ Mentor Sandbox")
    st.caption("Switch user cohorts to evaluate AI adaptation:")
    
    scenario_keys = list(SCENARIOS.keys())
    selected_key = st.selectbox(
        "Active Investor Persona:",
        scenario_keys,
        format_func=lambda k: SCENARIOS[k]["name"]
    )
    scenario = get_scenario(selected_key)
    user = scenario["user_profile"]
    m = scenario["metrics"]
    
    st.divider()
    st.markdown("#### 👤 Investor Profile")
    st.markdown(f"**Name:** {user['name']} (Age {user['age']})")
    st.markdown(f"**Monthly SIP:** ₹{user['monthly_sip']:,}")
    st.markdown(f"**Fund:** {user['fund_name']}")
    st.markdown(f"**Tenure:** {user['current_month']}")
    st.markdown(f"**Goal:** {user['goal']}")
    
    st.divider()
    st.markdown("#### 🧭 Screen Navigation")
    screens = [
        "📱 Dashboard",
        "📖 Monthly Perspective Story",
        "💬 Ask About My SIP",
        "⚙️ Manage / Exit Flow"
    ]
    st.session_state.current_screen = st.radio("Go to Screen:", screens, index=screens.index(st.session_state.current_screen))
    
    st.divider()
    show_telemetry = st.checkbox("🔍 Show Mentor Eval Telemetry", value=False)
    
    st.divider()
    if st.button("🔄 Reset Prototype State", use_container_width=True):
        st.session_state.current_screen = "📱 Dashboard"
        st.session_state.story_step = 0
        st.session_state.sip_query = ""
        st.session_state.skipped_month = False
        st.rerun()

# --- TOP GROWW NAVBAR ---
col_nav1, col_nav2 = st.columns([3, 1])
with col_nav1:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.5rem;">
        <img src="{groww_logo_uri}" width="38" height="38" style="border-radius: 8px; vertical-align: middle; box-shadow: 0 2px 6px rgba(0,0,0,0.06);" />
        <span style="color: #00D09C; font-weight: 800; font-size: 1.85rem; letter-spacing: -0.6px;">Groww</span>
        <span style="color: #7C828D; font-size: 1.15rem; font-weight: 500; margin-left: 2px;">| Mutual Funds</span>
    </div>
    """, unsafe_allow_html=True)
with col_nav2:
    st.markdown("<div style='text-align:right;'><span class='badge-verified'>✔ Non-Advisory Mode Active</span></div>", unsafe_allow_html=True)

# Mobile-friendly top navigation tabs
nav_c1, nav_c2, nav_c3, nav_c4 = st.columns(4)
with nav_c1:
    if st.button("📱 Dashboard", use_container_width=True, type="primary" if st.session_state.current_screen == "📱 Dashboard" else "secondary"):
        st.session_state.current_screen = "📱 Dashboard"
        st.rerun()
with nav_c2:
    if st.button("📖 Perspective Story", use_container_width=True, type="primary" if st.session_state.current_screen == "📖 Monthly Perspective Story" else "secondary"):
        st.session_state.current_screen = "📖 Monthly Perspective Story"
        st.rerun()
with nav_c3:
    if st.button("💬 Ask My SIP", use_container_width=True, type="primary" if st.session_state.current_screen == "💬 Ask About My SIP" else "secondary"):
        st.session_state.current_screen = "💬 Ask About My SIP"
        st.rerun()
with nav_c4:
    if st.button("⚙️ Manage / Exit", use_container_width=True, type="primary" if st.session_state.current_screen == "⚙️ Manage / Exit Flow" else "secondary"):
        st.session_state.current_screen = "⚙️ Manage / Exit Flow"
        st.rerun()

# Usability Testing Guide Card (Collapsible)
with st.expander("🧪 Usability Test Guide (Click to expand test instructions)", expanded=False):
    st.markdown(f"""
    **Welcome to the Groww Perspective Prototype Test!**  
    You are testing as **{user['name']}**, an investor in **{user['current_month']}** holding **{user['fund_name']}**.
    
    **Try completing these 4 simple tasks:**
    1. **Task 1 (Understand Your Returns):** Check your Dashboard and click **"Open My Monthly Perspective Story ✨"**. Step through the 3 cards to see why your drop is explained as buying units at a discount.
    2. **Task 2 (Interactive Simulation):** On Card 2 of the story, drag the **NAV Slider** to simulate what happens if market prices drop to ₹35 or rise to ₹50 next month.
    3. **Task 3 (Ask a Doubt):** Go to **"Ask About My SIP"** and test a question (e.g. click *"📉 Why is my return negative?"* or *"⏱️ What does XIRR mean?"*).
    4. **Task 4 (Managing Cash Flow):** Go to **"Manage / Exit Flow"**, choose *"Tight on cash this month"*, and test the 1-click **"Skip Next Month's Debit"** feature.
    """)

st.divider()

# =====================================================================
# SCREEN 1: GROWW PORTFOLIO DASHBOARD
# =====================================================================
if st.session_state.current_screen == "📱 Dashboard":
    st.markdown(f"## Mutual Fund Holdings • {user['name']}")
    st.caption(f"Portfolio health for {user['fund_name']}")
    
    # Hero Callout Banner for Perspective
    with st.container():
        st.info(
            f"💡 **Your {user['current_month']} Perspective is Ready!** We translated your monthly NAV movement and unit "
            f"accumulation into plain English. "
        )
        if st.button("Open My Monthly Perspective Story ✨", type="primary", use_container_width=True):
            st.session_state.current_screen = "📖 Monthly Perspective Story"
            st.rerun()
    
    st.markdown("### Portfolio Overview")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        with st.container(border=True):
            st.caption("Total Invested")
            st.markdown(f"### ₹{m['total_invested']:,.2f}")
            st.caption(f"{m['completed_instalments']} instalments completed")
            
    with c2:
        with st.container(border=True):
            st.caption("Current Value")
            st.markdown(f"### ₹{m['current_value']:,.2f}")
            ret_sign = "+" if m['total_return_inr'] >= 0 else ""
            ret_color = "positive-metric" if m['total_return_inr'] >= 0 else "negative-metric"
            st.markdown(f"<span class='{ret_color}'>{ret_sign}₹{m['total_return_inr']:,.2f} ({ret_sign}{m['total_return_pct']}%)</span>", unsafe_allow_html=True)
            
    with c3:
        with st.container(border=True):
            st.caption("1-Day Return")
            od_sign = "+" if m['one_day_return_inr'] >= 0 else ""
            od_color = "positive-metric" if m['one_day_return_inr'] >= 0 else "negative-metric"
            st.markdown(f"### <span class='{od_color}'>{od_sign}₹{m['one_day_return_inr']:,.2f}</span>", unsafe_allow_html=True)
            st.caption(f"{od_sign}{m['one_day_return_pct']}% today")
            
    with c4:
        with st.container(border=True):
            st.caption("Annualized Return (XIRR)")
            x_color = "positive-metric" if m['xirr_pct'] >= 0 else "negative-metric"
            st.markdown(f"### <span class='{x_color}'>{m['xirr_pct']}%</span>", unsafe_allow_html=True)
            st.caption("⚠️ Noisy in Months 1–6")
            if st.button("What is XIRR? ℹ️", key="btn_xirr_dash"):
                st.session_state.current_screen = "💬 Ask About My SIP"
                st.session_state.sip_query = "What does XIRR mean in simple words?"
                st.rerun()

    # Holdings details
    st.markdown("### Active SIPs")
    with st.container(border=True):
        f_col1, f_col2, f_col3, f_col4 = st.columns([3, 2, 2, 2])
        with f_col1:
            st.markdown(f"**{user['fund_name']}**")
            status_text = "⏸️ Paused for next month" if st.session_state.skipped_month else "🟢 Active SIP • AutoPay Enabled"
            st.caption(status_text)
        with f_col2:
            st.markdown(f"**Monthly SIP:** ₹{user['monthly_sip']:,}")
            st.caption(f"Next Debit: {'Dec 5, 2026' if st.session_state.skipped_month else 'Nov 5, 2026'}")
        with f_col3:
            st.markdown(f"**Total Units:** {m['total_units']:.2f}")
            st.caption(f"Avg Cost: ₹{m['average_nav_cost']:.2f}")
        with f_col4:
            if st.button("Manage SIP ⚙️", key="btn_manage_holdings"):
                st.session_state.current_screen = "⚙️ Manage / Exit Flow"
                st.rerun()

# =====================================================================
# SCREEN 2: INTERACTIVE PERSPECTIVE STORY MODE (Instagram / Spotify Wrapped Style)
# =====================================================================
elif st.session_state.current_screen == "📖 Monthly Perspective Story":
    st.markdown("## 📖 Monthly Wealth Perspective")
    st.caption("Step-by-step plain-language story of what happened to your SIP this month.")
    
    steps = ["1. Habit Streak", "2. Rupee-Cost Averaging", "3. Long-Term Compass"]
    st.progress((st.session_state.story_step + 1) / 3.0)
    
    # Story Card Container
    with st.container(border=True):
        if st.session_state.story_step == 0:
            st.markdown("### 🏆 Card 1 of 3: Your Habit Consistency Streak")
            st.markdown(f"#### **{m['completed_instalments']} of {m['target_instalments']} Instalments Completed**")
            st.progress(m['streak_pct'] / 100.0)
            st.markdown(
                f"You have invested consistently for **{m['completed_instalments']} consecutive months**. "
                f"You are **{m['streak_pct']:.0f}%** of the way towards your Year 1 habit milestone!\n\n"
                f"**Why this matters:** In the first 12 months, building the automated discipline to save ₹{user['monthly_sip']:,} "
                f"every month matters far more than short-term price movements."
            )
            st.metric(label="Consistency Streak", value=f"{m['completed_instalments']} Months Active", delta="100% on track")
            
        elif st.session_state.story_step == 1:
            st.markdown("### 📊 Card 2 of 3: Rupee-Cost Averaging in Action")
            if m["additional_units_this_month"] > 0:
                st.markdown(f"#### **You Bought Units on Discount!**")
                st.markdown(
                    f"Because the market dipped to an NAV of **₹{m['current_nav']}**, your regular ₹{user['monthly_sip']:,} "
                    f"bought **{m['units_bought_this_month']:.2f} units** this month—that's **+{m['additional_units_this_month']:.2f} extra units** "
                    f"compared to last month for the exact same ₹{user['monthly_sip']:,} investment!"
                )
                st.markdown(
                    f"**The Mathematical Benefit:** Your average cost per unit dropped from **₹{m['previous_average_nav']:.2f}** "
                    f"to **₹{m['average_nav_cost']:.2f}** ({m['cost_basis_reduction_pct']}% reduction). "
                    f"This lower cost basis means your portfolio will break even and turn profitable faster when the market recovers."
                )
            else:
                st.markdown("#### **Steady Unit Accumulation**")
                st.markdown(f"Your ₹{user['monthly_sip']:,} purchased **{m['units_bought_this_month']:.2f} units** this month at ₹{m['current_nav']} NAV.")
            
            st.divider()
            # Interactive Slider Simulator for Mentors/Users
            st.markdown("##### 🎮 Interactive Simulator: What happens if NAV fluctuates?")
            sim_nav = st.slider("Simulate Next Month's NAV (₹):", min_value=30.0, max_value=55.0, value=float(m['current_nav']), step=0.5)
            sim_units = user['monthly_sip'] / sim_nav
            st.info(f"If next month's NAV is **₹{sim_nav:.2f}**, your ₹{user['monthly_sip']:,} will automatically buy **{sim_units:.2f} units**! Lower prices accumulate more assets.")
            
        elif st.session_state.story_step == 2:
            st.markdown("### 🧭 Card 3 of 3: The Accumulator's Compass")
            st.markdown("#### **Short-Term Fluctuations vs. 10-Year Goals**")
            st.markdown(
                f"• **Current Market Context:** {m['market_condition']}\n"
                f"• **Why Red Numbers Don't Mean Destruction:** You have not sold any units. You own **{m['total_units']:.2f} pieces** "
                f"of top Indian companies. As long as you stay invested, short-term paper fluctuations wash out.\n"
                f"• **Historical Fact:** Over 10-year holding periods in Indian equities, the probability of negative returns is historically `<1%`."
            )
            st.success("🎯 **Recommended Action:** Sit back and let your monthly AutoPay do the work. No manual changes needed.")
    
    # Story Navigation Buttons
    nav_c1, nav_c2, nav_c3 = st.columns([1, 2, 1])
    with nav_c1:
        if st.session_state.story_step > 0:
            if st.button("⬅ Previous Card"):
                st.session_state.story_step -= 1
                st.rerun()
    with nav_c3:
        if st.session_state.story_step < 2:
            if st.button("Next Card ➔", type="primary"):
                st.session_state.story_step += 1
                st.rerun()
        else:
            if st.button("Back to Dashboard 🏁", type="primary"):
                st.session_state.current_screen = "📱 Dashboard"
                st.session_state.story_step = 0
                st.rerun()

# =====================================================================
# SCREEN 3: "ASK ABOUT MY SIP" CONVERSATIONAL COMPANION
# =====================================================================
elif st.session_state.current_screen == "💬 Ask About My SIP":
    st.markdown("## 💬 Ask About My SIP")
    st.caption("Confused about negative returns, jargon, or market dips? Ask in plain language.")
    
    # Quick Suggested Chips
    st.markdown("**Common Questions:**")
    q_col1, q_col2, q_col3 = st.columns(3)
    
    if q_col1.button("📉 Why is my return negative?"):
        st.session_state.sip_query = "Why are my returns red even though I have been disciplined?"
    if q_col2.button("⏱️ What does XIRR mean?"):
        st.session_state.sip_query = "What does XIRR mean in simple words?"
    if q_col3.button("⚠️ Should I sell this fund?"):
        st.session_state.sip_query = "Should I sell this fund because it is in negative?"
    
    # Search / Input Form
    with st.form(key="chat_query_form"):
        f_in, f_btn = st.columns([5, 1])
        with f_in:
            query_val = st.text_input(
                "Your Question:",
                value=st.session_state.sip_query,
                placeholder="e.g. What is NAV? Why did my money decrease today?",
                label_visibility="collapsed"
            )
        with f_btn:
            submitted = st.form_submit_button("Ask ✨", type="primary", use_container_width=True)
            
    active_q = query_val.strip() if query_val else None
    
    if active_q:
        with st.spinner("Analyzing verified portfolio ledger with SEBI safety gates..."):
            time.sleep(0.3)
            resp, eval_meta = engine.generate_perspective_response(active_q, scenario)
            
        with st.container(border=True):
            st.markdown(resp)
            st.divider()
            b1, b2, b3 = st.columns([2, 1, 1])
            with b1:
                st.markdown(f"<span class='badge-verified'>✔ Verified against Groww Ledger (Score: {eval_meta['quality_score']}/100)</span>", unsafe_allow_html=True)
            with b2:
                st.caption("Non-Advisory Guardrail: Active")
            with b3:
                st.caption("SEBI Compliant")
                
        if show_telemetry:
            with st.container(border=True):
                st.markdown("##### 🔍 Mentor Eval Telemetry")
                st.json({
                    "query": active_q,
                    "detected_intent": engine.classify_intent(active_q),
                    "guardrail_checks": eval_meta["checks"],
                    "quality_score": f"{eval_meta['quality_score']}/100",
                    "is_safe_for_production": eval_meta["is_safe"]
                })

# =====================================================================
# SCREEN 4: SMART EXIT & FLEXIBILITY FLOW (Downstream Safety Net)
# =====================================================================
elif st.session_state.current_screen == "⚙️ Manage / Exit Flow":
    st.markdown("## ⚙️ SIP Management & Pause Options")
    st.caption("Manage your SIP frequency, skip instalments, or adjust debit dates.")
    
    with st.container(border=True):
        st.markdown(f"### Manage: {user['fund_name']}")
        st.markdown(f"**Monthly Commitment:** ₹{user['monthly_sip']:,} on the 5th of every month")
        st.markdown(f"**Current Status:** {'⏸️ Paused for next month' if st.session_state.skipped_month else '🟢 Active'}")
        
        st.divider()
        st.markdown("#### Considering pausing or cancelling your SIP?")
        st.caption("Tell us what is prompting this decision so we can offer flexible relief:")
        
        exit_reason = st.radio(
            "Select primary reason:",
            [
                "💸 Tight on cash this month (Temporary salary delay or expense)",
                "📉 Worried about market dips and negative returns",
                "🛑 I want to permanently cancel this SIP mandate"
            ]
        )
        
        st.divider()
        if "Tight on cash" in exit_reason:
            st.success("💡 **Recommended Flexibility:** You do not need to cancel your 10-year wealth plan over a 1-month cash crunch!")
            st.markdown(
                "• **Skip Next Month (Zero Penalty):** We will pause only your upcoming debit. Your bank will not charge any bounce fees.\n"
                "• **Reschedule Date:** You can move your SIP date to 3 days after your salary credit date."
            )
            col_skip1, col_skip2 = st.columns(2)
            with col_skip1:
                if st.button("Confirm: Skip Next Month's Debit ✨", type="primary", use_container_width=True):
                    st.session_state.skipped_month = True
                    st.balloons()
                    st.success("Done! Your next instalment is skipped without breaking your SIP. AutoPay will resume the following month.")
            with col_skip2:
                if st.button("Move SIP Date to 10th (Post-Salary)", use_container_width=True):
                    st.success("SIP debit date updated to the 10th of every month.")
                    
        elif "Worried about market dips" in exit_reason:
            st.warning(f"📉 **Factual Reminder:** Your average unit cost is currently ₹{m['average_nav_cost']:.2f}.")
            st.markdown(
                f"If you cancel today, your cost basis is frozen at a paper loss. Continuing your monthly ₹{user['monthly_sip']:,} "
                f"at current lower NAVs (₹{m['current_nav']}) buys extra units, lowering your recovery hurdle."
            )
            if st.button("Read My Monthly Perspective Instead 📖", type="primary"):
                st.session_state.current_screen = "📖 Monthly Perspective Story"
                st.rerun()
                
        else:
            st.error("You have complete autonomy. If you wish to cancel your SIP mandate entirely, you may do so:")
            if st.button("Proceed with Immediate SIP Cancellation"):
                st.warning("Your SIP mandate has been cancelled as requested. You can restart anytime.")
