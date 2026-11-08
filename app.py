"""
app.py - Groww Perspective: Interactive AI-Native SIP Retention Companion
Mobile-optimized, clean, uncluttered fintech UX with Story Mode, 
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

# Set page configuration - Centered for clean mobile frame
st.set_page_config(
    page_title="Groww | Mutual Funds & SIP Companion",
    page_icon=logo_path if os.path.exists(logo_path) else "https://groww.in/groww-logo-270.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Groww aesthetic CSS - Mobile-First, Uncluttered, High Contrast
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* 1. Global Reset & Streamlit Chrome Removal */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #F4F6F9 !important;
        color: #191C1F !important;
    }
    
    /* Hide Streamlit default header, toolbar, footer and deploy button */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    [data-testid="stToolbar"] {
        display: none !important;
    }
    footer {
        display: none !important;
    }
    #MainMenu {
        display: none !important;
    }
    .stDeployButton {
        display: none !important;
    }
    div[data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Completely hide Streamlit Cloud manage-app red crown / viewer badge */
    div[class*="viewerBadge"],
    span[class*="viewerBadge"],
    a[class*="viewerBadge"],
    #manage-app-button,
    button[data-testid="manage-app-button"],
    div[data-testid="manage-app-button"],
    div[data-testid="stStatusWidget"],
    .viewerBadge_container__1QSob,
    .viewerBadge_link__1S137 {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        height: 0 !important;
        width: 0 !important;
    }
    
    /* 2. Sleek Mobile App Viewport Container (Max 480px) */
    .block-container {
        max-width: 460px !important;
        padding-top: 0.75rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        margin: 0 auto !important;
    }
    
    /* 3. High-Contrast Typography & Mobile Heading Scales */
    h1, h2, h3, h4, h5, h6 {
        color: #191C1F !important;
        letter-spacing: -0.4px !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.35rem !important;
    }
    h1 { font-size: 1.30rem !important; font-weight: 800 !important; }
    h2 { font-size: 1.15rem !important; font-weight: 700 !important; }
    h3 { font-size: 1.00rem !important; font-weight: 700 !important; }
    h4 { font-size: 0.90rem !important; font-weight: 600 !important; }
    p, span, label, div {
        color: #191C1F !important;
        font-size: 0.88rem !important;
    }
    
    /* Bullet points styling for clarity and readability */
    ul {
        margin-top: 0.4rem !important;
        margin-bottom: 0.6rem !important;
        padding-left: 1.25rem !important;
    }
    li {
        margin-bottom: 0.45rem !important;
        line-height: 1.45 !important;
        color: #191C1F !important;
    }
    li strong {
        color: #0E1116 !important;
    }
    
    .stCaption, [data-testid="stCaptionContainer"], small {
        color: #5E6573 !important;
        font-size: 0.76rem !important;
        font-weight: 500 !important;
    }
    
    /* 4. White Card Containers with crisp borders & subtle drop shadow */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE1E7 !important;
        border-radius: 14px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
        padding: 0.4rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* 5. Buttons styling - Groww Emerald Green */
    .stButton > button[kind="primary"] {
        background-color: #00D09C !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 2px 6px rgba(0, 208, 156, 0.25) !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #00B788 !important;
        box-shadow: 0 3px 8px rgba(0, 208, 156, 0.35) !important;
    }
    
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        color: #191C1F !important;
        border: 1px solid #DCE1E7 !important;
        background-color: #FFFFFF !important;
        padding: 0.45rem 0.65rem !important;
    }
    
    /* 6. Groww Badges & Pills */
    .badge-verified {
        background: #E6F9F4 !important;
        color: #007A5E !important;
        padding: 4px 10px !important;
        border-radius: 14px !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        border: 1px solid #8DE3CE !important;
        display: inline-block !important;
    }
    
    .badge-gray {
        background: #F1F4F7 !important;
        color: #5E6573 !important;
        padding: 4px 10px !important;
        border-radius: 14px !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        display: inline-block !important;
    }
    
    /* 7. Sidebar text high contrast */
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

# Single Source of Truth for Screen Navigation: "holdings" | "story" | "ask_ai" | "manage"
if "screen" not in st.session_state:
    st.session_state.screen = "holdings"
if "story_step" not in st.session_state:
    st.session_state.story_step = 0
if "sip_query" not in st.session_state:
    st.session_state.sip_query = ""
if "skipped_month" not in st.session_state:
    st.session_state.skipped_month = False
if "pause_duration" not in st.session_state:
    st.session_state.pause_duration = ""

# --- SIDEBAR: Scenario Switcher & Controls ---
with st.sidebar:
    st.markdown("### 🎛️ Investor Cohort Selector")
    st.caption("Switch user profiles to evaluate adaptive AI logic:")
    
    scenario_keys = list(SCENARIOS.keys())
    selected_key = st.selectbox(
        "Active Investor Persona:",
        scenario_keys,
        format_func=lambda k: SCENARIOS[k]["name"],
        key="persona_selector"
    )
    scenario = get_scenario(selected_key)
    user = scenario["user_profile"]
    m = scenario["metrics"]
    
    st.divider()
    st.markdown("#### 👤 Persona Details")
    st.markdown(f"**Name:** {user['name']} (Age {user['age']})")
    st.markdown(f"**Monthly SIP:** ₹{user['monthly_sip']:,}")
    st.markdown(f"**Fund:** {user['fund_name']}")
    st.markdown(f"**Tenure:** {user['current_month']}")
    st.markdown(f"**Goal:** {user['goal']}")
    
    st.divider()
    st.markdown("#### 🧭 Screen Navigation")
    for s_key, s_label in [("holdings", "📱 Holdings"), ("story", "📖 Story"), ("ask_ai", "💬 Ask AI"), ("manage", "⚙️ Manage")]:
        if st.button(s_label, key=f"sb_nav_{s_key}", use_container_width=True, type="primary" if st.session_state.screen == s_key else "secondary"):
            st.session_state.screen = s_key
            st.rerun()
    
    st.divider()
    show_telemetry = st.checkbox("🔍 Show Mentor Eval Telemetry", value=False, key="check_telemetry")
    
    st.divider()
    if st.button("🔄 Reset Prototype State", use_container_width=True, key="btn_reset_state"):
        st.session_state.screen = "holdings"
        st.session_state.story_step = 0
        st.session_state.sip_query = ""
        st.session_state.skipped_month = False
        st.session_state.pause_duration = ""
        st.rerun()

# Scenario fallback if sidebar hasn't loaded local vars
if "user" not in locals():
    scenario = get_scenario("scenario_a_dip_month3")
    user = scenario["user_profile"]
    m = scenario["metrics"]
if "show_telemetry" not in locals():
    show_telemetry = False

# =====================================================================
# SLEEK GROWW MOBILE APP BAR
# =====================================================================
st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: space-between; padding: 2px 2px 8px 2px; border-bottom: 1px solid #E6ECEF; margin-bottom: 10px;">
    <div style="display: flex; align-items: center; gap: 8px;">
        <img src="{groww_logo_uri}" width="28" height="28" style="border-radius: 7px; vertical-align: middle;" />
        <span style="color: #00D09C; font-weight: 800; font-size: 1.35rem; letter-spacing: -0.5px;">Groww</span>
        <span style="color: #8C939F; font-size: 0.85rem; font-weight: 600; margin-left: 2px;">Mutual Funds</span>
    </div>
    <div>
        <span class="badge-verified">🛡️ SEBI Safe</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Compact 4-Tab Navigation Bar (Side-by-side, perfectly proportioned for mobile)
nav_cols = st.columns(4)

with nav_cols[0]:
    if st.button("📱 Holdings", use_container_width=True, type="primary" if st.session_state.screen == "holdings" else "secondary", key="top_nav_holdings"):
        st.session_state.screen = "holdings"
        st.rerun()
with nav_cols[1]:
    if st.button("📖 Story", use_container_width=True, type="primary" if st.session_state.screen == "story" else "secondary", key="top_nav_story"):
        st.session_state.screen = "story"
        st.rerun()
with nav_cols[2]:
    if st.button("💬 Ask AI", use_container_width=True, type="primary" if st.session_state.screen == "ask_ai" else "secondary", key="top_nav_ask"):
        st.session_state.screen = "ask_ai"
        st.rerun()
with nav_cols[3]:
    if st.button("⚙️ Manage", use_container_width=True, type="primary" if st.session_state.screen == "manage" else "secondary", key="top_nav_manage"):
        st.session_state.screen = "manage"
        st.rerun()

# Clean collapsible Usability Guide
with st.expander("🧪 Test Guide & Cohort Tasks", expanded=False):
    st.markdown(f"""
    **Current User:** {user['name']} ({user['current_month']} • ₹{user['monthly_sip']:,}/mo)  
    1. **Holdings:** Review the 2x2 Overview and tap **"Open Monthly Perspective"**.  
    2. **Story:** On Card 2, test the **NAV Slider** to see how lower prices buy more units.  
    3. **Ask AI:** Ask about any number or term (e.g. *"How are returns calculated?"* or *"What is XIRR?"*).  
    4. **Manage:** Test 1-click **"Skip Next Month"** or **"Pause SIP"**.  
    """)

# =====================================================================
# SCREEN 1: GROWW PORTFOLIO DASHBOARD (MOBILE-FIRST)
# =====================================================================
if st.session_state.screen == "holdings":
    # Compact User & Fund Header
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin: 6px 0 10px 0;">
        <div>
            <div style="font-size: 1.05rem; font-weight: 800; color: #191C1F;">{user['name']}</div>
            <div style="font-size: 0.76rem; color: #6F7684; font-weight: 500;">{user['fund_name']}</div>
        </div>
        <div style="text-align: right;">
            <span class="badge-gray">{user['current_month']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Perspective Callout Card (Emerald Groww styling)
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #E8F9F3 0%, #F4FDF9 100%); border: 1.5px solid #8DE3CE; border-radius: 12px; padding: 12px 14px; margin-bottom: 12px; box-shadow: 0 2px 6px rgba(0, 208, 156, 0.08);">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 3px;">
            <span style="font-size: 1.1rem;">💡</span>
            <span style="font-size: 0.88rem; font-weight: 800; color: #007A5E;">{user['current_month']} Perspective Ready</span>
        </div>
        <div style="font-size: 0.78rem; color: #334155; line-height: 1.35; margin-bottom: 8px;">
            We translated your monthly NAV movements and unit accumulation into plain English.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Open My Monthly Perspective Story ✨", type="primary", use_container_width=True, key="btn_hero_open_story"):
        st.session_state.screen = "story"
        st.session_state.story_step = 0
        st.rerun()
    
    # Portfolio Overview: Compact 2x2 Mobile Grid (Zero scrolling needed!)
    ret_color = "#EB5757" if m['total_return_inr'] < 0 else "#00A87E"
    ret_sign = "+" if m['total_return_inr'] >= 0 else ""
    xirr_color = "#EB5757" if m['xirr_pct'] < 0 else "#00A87E"
    
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #DCE1E7; border-radius: 14px; padding: 14px 14px 12px 14px; margin-top: 10px; margin-bottom: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 0.74rem; font-weight: 700; color: #7C828D; text-transform: uppercase; letter-spacing: 0.4px;">Portfolio Overview</span>
            <span style="font-size: 0.72rem; color: #8F95A0; font-weight: 500;">{m['completed_instalments']} SIPs completed</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <!-- Top Left: Total Invested -->
            <div style="background: #F8FAFB; border-radius: 10px; padding: 9px 11px;">
                <div style="font-size: 0.68rem; color: #7C828D; font-weight: 600;">TOTAL INVESTED</div>
                <div style="font-size: 1.10rem; font-weight: 800; color: #191C1F; margin-top: 2px;">₹{m['total_invested']:,.2f}</div>
            </div>
            <!-- Top Right: Current Value -->
            <div style="background: #F8FAFB; border-radius: 10px; padding: 9px 11px;">
                <div style="font-size: 0.68rem; color: #7C828D; font-weight: 600;">CURRENT VALUE</div>
                <div style="font-size: 1.10rem; font-weight: 800; color: #191C1F; margin-top: 2px;">₹{m['current_value']:,.2f}</div>
            </div>
            <!-- Bottom Left: Total Returns -->
            <div style="background: #F8FAFB; border-radius: 10px; padding: 9px 11px;">
                <div style="font-size: 0.68rem; color: #7C828D; font-weight: 600;">TOTAL RETURNS</div>
                <div style="font-size: 1.05rem; font-weight: 800; color: {ret_color}; margin-top: 2px;">{ret_sign}₹{m['total_return_inr']:,.2f}</div>
                <div style="font-size: 0.70rem; font-weight: 700; color: {ret_color};">{ret_sign}{m['total_return_pct']}%</div>
            </div>
            <!-- Bottom Right: Annualized Return -->
            <div style="background: #F8FAFB; border-radius: 10px; padding: 9px 11px;">
                <div style="font-size: 0.68rem; color: #7C828D; font-weight: 600;">ANNUALIZED (XIRR)</div>
                <div style="font-size: 1.05rem; font-weight: 800; color: {xirr_color}; margin-top: 2px;">{m['xirr_pct']}%</div>
                <div style="font-size: 0.66rem; color: #8F95A0;">Noisy in M1–6</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Active SIP Holdings Card
    if st.session_state.skipped_month:
        status_text = f"⏸️ Paused ({st.session_state.pause_duration if st.session_state.pause_duration else 'Next Month'})"
        status_color = "#E67E22"
        next_date = "Dec 5, 2026"
    else:
        status_text = "🟢 Active AutoPay"
        status_color = "#00A87E"
        next_date = "Nov 5, 2026"
    
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #DCE1E7; border-radius: 14px; padding: 12px 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.02); margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
            <div>
                <div style="font-size: 0.88rem; font-weight: 700; color: #191C1F;">{user['fund_name']}</div>
                <div style="font-size: 0.72rem; color: {status_color}; font-weight: 600; margin-top: 2px;">{status_text} • Next: {next_date}</div>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; padding-top: 8px; border-top: 1px solid #EEF1F4;">
            <div>
                <div style="font-size: 0.66rem; color: #7C828D; font-weight: 600;">MONTHLY SIP</div>
                <div style="font-size: 0.85rem; font-weight: 700; color: #191C1F;">₹{user['monthly_sip']:,}</div>
            </div>
            <div>
                <div style="font-size: 0.66rem; color: #7C828D; font-weight: 600;">TOTAL UNITS</div>
                <div style="font-size: 0.85rem; font-weight: 700; color: #191C1F;">{m['total_units']:.2f}</div>
            </div>
            <div>
                <div style="font-size: 0.66rem; color: #7C828D; font-weight: 600;">AVG COST</div>
                <div style="font-size: 0.85rem; font-weight: 700; color: #191C1F;">₹{m['average_nav_cost']:.2f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        if st.button("What is XIRR? ℹ️", use_container_width=True, key="btn_holdings_xirr"):
            st.session_state.screen = "ask_ai"
            st.session_state.sip_query = "What does XIRR mean in simple words?"
            st.rerun()
    with col_act2:
        if st.button("Manage SIP ⚙️", use_container_width=True, key="btn_holdings_manage"):
            st.session_state.screen = "manage"
            st.rerun()

# =====================================================================
# SCREEN 2: INTERACTIVE PERSPECTIVE STORY MODE (MOBILE-FIRST)
# =====================================================================
elif st.session_state.screen == "story":
    curr_step = st.session_state.story_step
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin: 4px 0 8px 0;">
        <div style="font-size: 1.05rem; font-weight: 800; color: #191C1F;">📖 Monthly Perspective</div>
        <div style="font-size: 0.74rem; font-weight: 700; color: #00A87E;">Card {curr_step + 1} of 3</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress((curr_step + 1) / 3.0)
    
    with st.container(border=True):
        if curr_step == 0:
            st.markdown("#### 🏆 Card 1: Consistency Streak")
            st.markdown(f"**{m['completed_instalments']} of {m['target_instalments']} Instalments Completed**")
            st.progress(m['streak_pct'] / 100.0)
            
            st.markdown(f"""
            You have invested consistently for **{m['completed_instalments']} consecutive months**. You are **{m['streak_pct']:.0f}%** of the way towards your Year 1 habit milestone!
            
            **Why this matters:** In Months 1–12, building the automated discipline to save ₹{user['monthly_sip']:,} each month matters far more than short-term price swings.
            """)
            st.info(f"🔥 **Habit Score:** {m['completed_instalments']} Months Active • 100% On Track")
            
        elif curr_step == 1:
            st.markdown("#### 📊 Card 2: Rupee-Cost Averaging")
            if m["additional_units_this_month"] > 0:
                st.markdown(f"""
                <div style="background: #E8F9F3; border-radius: 10px; padding: 10px 12px; margin-bottom: 10px; border-left: 4px solid #00D09C;">
                    <div style="font-weight: 800; color: #007A5E; font-size: 0.95rem;">You Bought Units on Discount!</div>
                    <div style="font-size: 0.82rem; color: #2C3E50; margin-top: 4px;">
                        Because NAV dropped to <b>₹{m['current_nav']}</b>, your regular ₹{user['monthly_sip']:,} purchased <b>{m['units_bought_this_month']:.2f} units</b> (<b>+{m['additional_units_this_month']:.2f} extra units</b> vs last month).
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                **The Benefit:** Your average cost dropped from **₹{m['previous_average_nav']:.2f}** to **₹{m['average_nav_cost']:.2f}** ({m['cost_basis_reduction_pct']}% lower). A lower cost basis turns your portfolio profitable faster when markets recover.
                """)
            else:
                st.markdown(f"Your ₹{user['monthly_sip']:,} accumulated **{m['units_bought_this_month']:.2f} units** this month at ₹{m['current_nav']} NAV.")
            
            st.markdown("---")
            st.markdown("##### 🎮 Simulator: What if NAV fluctuates?")
            sim_nav = st.slider("Simulate NAV (₹):", min_value=30.0, max_value=55.0, value=float(m['current_nav']), step=0.5, key="story_slider_nav")
            sim_units = user['monthly_sip'] / sim_nav
            st.caption(f"At ₹{sim_nav:.2f} NAV, ₹{user['monthly_sip']:,} buys **{sim_units:.2f} units**. Lower prices accumulate more assets.")
            
        elif curr_step == 2:
            st.markdown("#### 🧭 Card 3: The Accumulator's Compass")
            st.markdown(f"""
            • **Current Market:** {m['market_condition']}  
            • **Paper Loss vs. Realized Loss:** You haven't sold any units. You own **{m['total_units']:.2f} pieces** of India's top companies.  
            • **10-Year Probability:** In Indian equities, 10-year holding periods historically carry `<1%` probability of negative returns.
            """)
            st.success("🎯 **Recommended Action:** Let your monthly AutoPay run. No manual intervention required.")
            
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        if curr_step > 0:
            if st.button("⬅ Previous Card", use_container_width=True, key="btn_story_prev"):
                st.session_state.story_step -= 1
                st.rerun()
        else:
            if st.button("⬅ Back to Holdings", use_container_width=True, key="btn_story_back_holdings"):
                st.session_state.screen = "holdings"
                st.rerun()
    with s_col2:
        if curr_step < 2:
            if st.button("Next Card ➔", type="primary", use_container_width=True, key="btn_story_next"):
                st.session_state.story_step += 1
                st.rerun()
        else:
            if st.button("Complete Story 🏁", type="primary", use_container_width=True, key="btn_story_finish"):
                st.session_state.screen = "holdings"
                st.session_state.story_step = 0
                st.rerun()

# =====================================================================
# SCREEN 3: ASK ABOUT MY SIP (MOBILE-FIRST DASHBOARD DECRYPTOR)
# =====================================================================
elif st.session_state.screen == "ask_ai":
    st.markdown("""
    <div style="margin: 4px 0 8px 0;">
        <div style="font-size: 1.05rem; font-weight: 800; color: #191C1F;">💬 Ask About My SIP</div>
        <div style="font-size: 0.76rem; color: #6F7684;">Instant plain-English decryptor for any number or term on your dashboard.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Prompt Chips Section - Category 1: Numbers & Formulas
    st.caption("🔢 Explore Dashboard Numbers & Calculations:")
    n_col1, n_col2 = st.columns(2)
    with n_col1:
        if st.button("📊 How are returns calculated?", use_container_width=True, key="chip_ret_calc"):
            st.session_state.sip_query = "How are my returns calculated?"
            st.rerun()
    with n_col2:
        if st.button("💰 Total Invested breakdown", use_container_width=True, key="chip_total_inv"):
            st.session_state.sip_query = "What is my total invested?"
            st.rerun()

    n_col3, n_col4 = st.columns(2)
    with n_col3:
        if st.button("🏷️ What is NAV & Unit Cost?", use_container_width=True, key="chip_nav_cost"):
            st.session_state.sip_query = "What is NAV in simple words?"
            st.rerun()
    with n_col4:
        if st.button("⏱️ What does XIRR mean?", use_container_width=True, key="chip_what_xirr"):
            st.session_state.sip_query = "What is XIRR and why is it showing -14%?"
            st.rerun()
            
    # Category 2: Doubts & Concepts
    st.caption("💡 Clarify Concepts & Doubts:")
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        if st.button("📉 Why are returns red?", use_container_width=True, key="chip_why_neg"):
            st.session_state.sip_query = "Why are my returns red even though I have been disciplined?"
            st.rerun()
    with d_col2:
        if st.button("🛡️ Is my money safe?", use_container_width=True, key="chip_safety"):
            st.session_state.sip_query = "Is my investment safe on Groww?"
            st.rerun()

    d_col3, d_col4 = st.columns(2)
    with d_col3:
        if st.button("🌱 What is Direct Growth?", use_container_width=True, key="chip_direct_growth"):
            st.session_state.sip_query = "What does Direct Growth mean?"
            st.rerun()
    with d_col4:
        if st.button("⚠️ Should I stop this fund?", use_container_width=True, key="chip_should_stop"):
            st.session_state.sip_query = "Should I sell this fund because it is in negative?"
            st.rerun()
    
    # Custom Question Input field
    st.markdown("---")
    q_col1, q_col2 = st.columns([4, 1])
    with q_col1:
        query_val = st.text_input(
            "Your Question:",
            value=st.session_state.sip_query,
            placeholder="Ask about any number, term, or return...",
            label_visibility="collapsed",
            key="input_ask_text"
        )
    with q_col2:
        submitted = st.button("Ask ✨", type="primary", use_container_width=True, key="btn_ask_action")
        
    active_q = query_val.strip() if query_val else st.session_state.sip_query.strip()
    
    if active_q:
        with st.spinner("Decrypting dashboard ledger with SEBI safety gates..."):
            time.sleep(0.15)
            resp, eval_meta = engine.generate_perspective_response(active_q, scenario)
            
        with st.container(border=True):
            st.markdown(resp)
            st.markdown(f"""
            <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #EEF1F4; display: flex; justify-content: space-between; align-items: center;">
                <span class="badge-verified">✔ Verified Ledger (Score: {eval_meta['quality_score']}/100)</span>
                <span style="font-size: 0.70rem; color: #8F95A0; font-weight: 600;">SEBI Non-Advisory</span>
            </div>
            """, unsafe_allow_html=True)
            
        if show_telemetry:
            with st.container(border=True):
                st.caption("🔍 Mentor Eval Telemetry")
                st.json({
                    "query": active_q,
                    "intent": engine.classify_intent(active_q),
                    "checks": eval_meta["checks"],
                    "quality_score": f"{eval_meta['quality_score']}/100",
                    "safe": eval_meta["is_safe"]
                })

# =====================================================================
# SCREEN 4: SMART EXIT & FLEXIBILITY FLOW (MOBILE-FIRST)
# =====================================================================
elif st.session_state.screen == "manage":
    st.markdown("""
    <div style="margin: 4px 0 8px 0;">
        <div style="font-size: 1.05rem; font-weight: 800; color: #191C1F;">⚙️ Manage & Pause Options</div>
        <div style="font-size: 0.76rem; color: #6F7684;">Adjust dates, skip upcoming debit, or pause instalments.</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f"**{user['fund_name']}**")
        st.caption(f"₹{user['monthly_sip']:,}/mo • Status: {'⏸️ Paused' if st.session_state.skipped_month else '🟢 Active AutoPay'}")
        
        st.markdown("---")
        st.markdown("##### What is prompting your change?")
        exit_reason = st.radio(
            "Select reason:",
            [
                "💸 Tight on cash this month",
                "📉 Worried about market dips",
                "🛑 Permanently cancel SIP mandate"
            ],
            label_visibility="collapsed",
            key="radio_manage_reason"
        )
        
        st.markdown("---")
        if "Tight on cash" in exit_reason:
            st.info("💡 **Flexible Options:** Avoid bank bounce fees without terminating your long-term wealth habit.")
            
            if st.button("Skip Next Month's Instalment", type="primary", use_container_width=True, key="btn_action_skip"):
                st.session_state.skipped_month = True
                st.session_state.pause_duration = "1 Month"
                st.balloons()
                st.success("Next instalment skipped with zero fee! AutoPay resumes automatically next month.")
                
            if st.button("Move Date to 10th (Post-Salary)", use_container_width=True, key="btn_action_move_date"):
                st.success("SIP debit date rescheduled to the 10th of every month.")
                
        elif "Worried about market dips" in exit_reason:
            st.info(f"ℹ️ You own **{m['total_units']:.2f} units** with average cost of **₹{m['average_nav_cost']:.2f}**. Temporary dips accumulate more units at discounts.")
            
            st.markdown("##### ⏸️ Pause Your SIP")
            pause_choice = st.selectbox(
                "Select pause duration:",
                [
                    "1 Month (Resume in Dec 2026)",
                    "2 Months (Resume in Jan 2027)",
                    "3 Months (Resume in Feb 2027)",
                    "6 Months (Resume in May 2027)"
                ],
                key="select_pause_months"
            )
            if st.button("Proceed with Pausing ✨", type="primary", use_container_width=True, key="btn_action_pause"):
                st.session_state.skipped_month = True
                st.session_state.pause_duration = pause_choice.split(" ")[0] + " " + pause_choice.split(" ")[1]
                st.balloons()
                st.success(f"Done! Your SIP is paused for {pause_choice}. Your AutoPay mandate stays active.")
                
            if st.button("Read Monthly Perspective 📖", use_container_width=True, key="btn_manage_go_story"):
                st.session_state.screen = "story"
                st.session_state.story_step = 0
                st.rerun()
                
        else:
            st.caption("You have full control over your funds. Zero lock-in.")
            if st.button("Proceed with SIP Cancellation", type="primary", use_container_width=True, key="btn_action_cancel"):
                st.session_state.skipped_month = False
                st.session_state.pause_duration = ""
                st.warning(f"Your SIP mandate has been cancelled. Your {m['total_units']:.2f} accumulated units remain safe in your Groww portfolio.")
