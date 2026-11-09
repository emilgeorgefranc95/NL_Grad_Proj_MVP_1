import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # High-Contrast Color Palette
    DARK_NAVY = RGBColor(15, 23, 42)      # #0F172A (Deep Slate - High contrast)
    EMERALD   = RGBColor(5, 150, 105)     # #059669 (Groww Green)
    CORAL_RED = RGBColor(220, 38, 38)     # #DC2626 (Alert Red)
    SLATE_BODY= RGBColor(30, 41, 59)      # #1E293B (Dark Slate for body text)
    SLATE_MUT = RGBColor(71, 85, 105)     # #475569 (Medium Slate for secondary)
    CARD_BG   = RGBColor(248, 250, 252)   # #F8FAFC
    CARD_BDR  = RGBColor(203, 213, 225)   # #CBD5E1 (Visible border)
    WHITE     = RGBColor(255, 255, 255)
    LIGHT_EMR = RGBColor(236, 253, 245)   # #ECFDF5
    LIGHT_RED = RGBColor(254, 242, 242)   # #FEF2F2
    LIGHT_HDR = RGBColor(241, 245, 249)   # #F1F5F9

    def add_header(slide, title_text, subtitle_text):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.733), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.name = "Arial"
        p2.font.size = Pt(13)
        p2.font.color.rgb = SLATE_MUT

    def add_footer(slide, placeholder_text, slide_num):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        
        # Left link
        p.text = f"{placeholder_text}   |   NextLeap PM Graduation Project • Groww Growth Track • Strictly Anonymized"
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = SLATE_MUT
        
        # Right slide number
        tb_num = slide.shapes.add_textbox(Inches(10.5), Inches(7.0), Inches(2.033), Inches(0.35))
        tf_num = tb_num.text_frame
        tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
        p_num = tf_num.paragraphs[0]
        p_num.text = f"Slide {slide_num} of 10"
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.font.name = "Arial"
        p_num.font.size = Pt(10)
        p_num.font.bold = True
        p_num.font.color.rgb = DARK_NAVY

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BDR):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1)
        else:
            shape.line.fill.background()
        return shape

    def format_cell(cell, text, font_size=10, bold=False, color=DARK_NAVY, align=PP_ALIGN.LEFT, bg_color=WHITE):
        cell.text = text
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_color
        for p in cell.text_frame.paragraphs:
            p.font.name = "Arial"
            p.font.size = Pt(font_size)
            p.font.bold = bold
            p.font.color.rgb = color
            p.alignment = align
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(font_size)
                r.font.bold = bold
                r.font.color.rgb = color

    # ==========================================
    # SLIDE 1: Business Metric Decomposition
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    add_header(slide1, "Breaking Down 12-Month SIP Continuation for First-Time Investors",
               "Decomposing Retention into North Star, Primary, L1 Operational Metrics & The 5-Stage Lifecycle Journey")
    
    # 3 Top Metric Cards
    # Card 1: North Star
    c1 = add_card(slide1, Inches(0.8), Inches(1.5), Inches(3.7), Inches(2.3), bg_color=LIGHT_EMR, border_color=EMERALD)
    tb1 = slide1.shapes.add_textbox(Inches(0.95), Inches(1.6), Inches(3.4), Inches(2.1))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0
    p = tf1.paragraphs[0]
    p.text = "🌟 NORTH STAR METRIC"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = EMERALD
    p.space_after = Pt(4)
    
    p = tf1.add_paragraph()
    p.text = "% of First-Time Investors with an Active SIP at Month 12"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_NAVY
    p.space_after = Pt(4)
    
    p = tf1.add_paragraph()
    p.text = "Formula: Active = ≥1 successful instalment in trailing 30 days at Month 12 / Total First-Time Cohort."
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.color.rgb = SLATE_BODY
    p.space_after = Pt(4)

    p = tf1.add_paragraph()
    p.text = "Core Goal: Defends genuine compounding habit. Filters out one-off setup spikes."
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.color.rgb = SLATE_MUT

    # Card 2: Primary Metrics
    c2 = add_card(slide1, Inches(4.75), Inches(1.5), Inches(3.7), Inches(2.3))
    tb2 = slide1.shapes.add_textbox(Inches(4.9), Inches(1.6), Inches(3.4), Inches(2.1))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
    p = tf2.paragraphs[0]
    p.text = "🎯 PRIMARY METRICS"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_NAVY
    p.space_after = Pt(4)
    
    bullets_p2 = [
        ("12-Mo SIP Retention Rate: ", "Baseline ~50% ➔ Target 56% (+6% absolute lift / +12% relative)."),
        ("Month 2–6 Churn Cliff: ", "Reduce drop-off during peak friction window from 45% to <30%."),
        ("Average Inflow Retention: ", "Sustain avg monthly instalment (~₹2,500/month) across cohort.")
    ]
    for b_title, b_desc in bullets_p2:
        p = tf2.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + b_title
        run1.font.name = "Arial"
        run1.font.bold = True
        run1.font.size = Pt(11)
        run1.font.color.rgb = DARK_NAVY
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.name = "Arial"
        run2.font.size = Pt(10.5)
        run2.font.color.rgb = SLATE_BODY
        p.space_after = Pt(2)

    # Card 3: L1 Input Metrics
    c3 = add_card(slide1, Inches(8.7), Inches(1.5), Inches(3.833), Inches(2.3))
    tb3 = slide1.shapes.add_textbox(Inches(8.85), Inches(1.6), Inches(3.533), Inches(2.1))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_top = tf3.margin_right = tf3.margin_bottom = 0
    p = tf3.paragraphs[0]
    p.text = "⚙️ L1 / INPUT METRICS"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_NAVY
    p.space_after = Pt(4)
    
    bullets_p3 = [
        ("Mandate Execution Success: ", "% debits cleared without bank bounce fees (>95%)."),
        ("Contextual Engagement: ", "% reviewing monthly Perspective debrief (≥65%)."),
        ("In-App Query Resolution: ", "% jargon/doubt queries resolved in-app (>85%)."),
        ("Flexibility vs. Churn Ratio: ", "% choosing Skip/Pause over cancellation (>50%).")
    ]
    for b_title, b_desc in bullets_p3:
        p = tf3.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + b_title
        run1.font.name = "Arial"
        run1.font.bold = True
        run1.font.size = Pt(10.5)
        run1.font.color.rgb = DARK_NAVY
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.name = "Arial"
        run2.font.size = Pt(10)
        run2.font.color.rgb = SLATE_BODY
        p.space_after = Pt(2)

    # Bottom Table: 5-Stage Lifecycle Journey
    t_shape = slide1.shapes.add_table(4, 5, Inches(0.8), Inches(4.0), Inches(11.733), Inches(2.8))
    table = t_shape.table
    col_w = Inches(11.733 / 5)
    for i in range(5):
        table.columns[i].width = col_w

    headers_s1 = [
        "Month 0: Setup & First Mandate",
        "Month 1: First Automated Debit",
        "Months 2–6: The Churn Cliff 🔥",
        "Months 7–11: Habit Consolidation",
        "Month 12+: Compounding & Step-Up"
    ]
    for i, h in enumerate(headers_s1):
        cell = table.cell(0, i)
        bg_col = LIGHT_RED if i == 2 else LIGHT_HDR
        txt_col = CORAL_RED if i == 2 else DARK_NAVY
        format_cell(cell, h, font_size=10.5, bold=True, color=txt_col, align=PP_ALIGN.CENTER, bg_color=bg_col)

    row_data_s1 = [
        ("User Journey & Actions", [
            "Frictionless UPI auto-pay setup; initial fund selection.",
            "1st automated debit processes; SMS account confirmation.",
            "Encounter 1st market dip (-5% to -10%). Peak churn window.",
            "Routine stabilizes; market begins mean-reversion.",
            "12-month investing anniversary reached."
        ]),
        ("User Psychology & Friction", [
            "High optimism, low market literacy. Expects linear returns.",
            "Verifies debit. Disappointed by flat return (+₹10).",
            "Acute panic: Red returns (-₹520) & XIRR (-14%). Feels money vanished.",
            "Observes recovery; ignores daily noise if RCA understood.",
            "Habit cemented; receptive to voluntary annual step-up."
        ]),
        ("Desired Product Outcome", [
            "Frictionless setup; set realistic 3–5 year wealth horizon.",
            "1st milestone badge; initiate consistency streak.",
            "Cognitive Reframing: Reframe dips as unit discount; plain XIRR; 1-click skip.",
            "Celebrate 6-month streak; quarterly portfolio health check.",
            "12-month graduation badge; prompt 10% annual SIP step-up."
        ])
    ]

    for row_idx, (r_name, r_vals) in enumerate(row_data_s1, start=1):
        for col_idx, text_val in enumerate(r_vals):
            cell = table.cell(row_idx, col_idx)
            bg_col = RGBColor(255, 245, 245) if col_idx == 2 else WHITE
            format_cell(cell, text_val, font_size=9.5, bold=False, color=SLATE_BODY, align=PP_ALIGN.LEFT, bg_color=bg_col)

    add_footer(slide1, "[Placeholder: Link to Business Metric Decomposition Doc]", 1)

    # ==========================================
    # SLIDE 2: Secondary Research & AI Discovery Engine
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    slide2_img_path = "/tmp/slide2_user_hd.png"
    if os.path.exists(slide2_img_path):
        slide2.shapes.add_picture(slide2_img_path, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    else:
        add_header(slide2, "Public Investor Voice Reveals a Post-Onboarding Conviction Deficit",
                   "AI Synthesis of 327,385 Public Retail Investor Items Across Reddit, Play Store & YouTube")
        add_footer(slide2, "[Placeholder: Link to AI Evidence Log & Claude Discovery Engine]", 2)

    # ==========================================
    # SLIDE 3: Primary User Research
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Primary User Research: Confusion and Support Voids Drive Cancellation Intent",
               "5 In-Depth Qualitative 1-on-1 Interviews (30–45 Mins) with Retail SIP Investors across Groww & Competitors")
    
    interview_cards = [
        ("UI Overload Designed for Veterans",
         "Legacy trading layouts spook long-term beginners with high data density and live price updates.",
         "“Everything is tailor-made for veterans... Lot of numbers getting updated in real-time without clarity in layman language.”",
         "— Pradhul (36, Salaried IT Professional, Groww user)",
         Inches(0.8), Inches(1.5)),
        ("Dashboard Confusion Drives Churn Intent",
         "Inability to track progress or understand what matters induces cognitive fatigue and exit intent.",
         "“As a first-timer, identifying what to track in the dashboard was very difficult. At some point, it made me consider stopping my SIP... thought this would be too hectic for my routine.”",
         "— Sushant (27, First-Time SIP Investor, Groww user)",
         Inches(6.8), Inches(1.5)),
        ("The Support & Handholding Void",
         "Zero in-app contextual reassurance forces users to abandon the platform for YouTube and Google search.",
         "“No one gives investment advice, but there was no handholding... had to search Google and YouTube to understand what was happening with my funds.”",
         "— Bijoy (38, Retail Investor, Groww & Zerodha user)",
         Inches(0.8), Inches(4.2)),
        ("Mandate Timing Anxiety & Bank Penalties",
         "1-day notice creates acute balance anxiety, risking ₹250–₹500 bank penalty bounce fees and reactive churn.",
         "“Groww intimates only 1 day before debit. If they gave 3–4 days advance notice, we could maintain funds in time to avoid bank penalties.”",
         "— Pradhul & Bijoy (Joint Finding on Mandate Timing)",
         Inches(6.8), Inches(4.2))
    ]

    for title_ic, desc_ic, quote_ic, author_ic, left_pos, top_pos in interview_cards:
        add_card(slide3, left_pos, top_pos, Inches(5.733), Inches(2.55))
        tb = slide3.shapes.add_textbox(left_pos + Inches(0.2), top_pos + Inches(0.15), Inches(5.333), Inches(2.25))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = title_ic
        p.font.name = "Arial"
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(2)
        
        p = tf.add_paragraph()
        p.text = desc_ic
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.color.rgb = SLATE_MUT
        p.space_after = Pt(6)
        
        p = tf.add_paragraph()
        p.text = quote_ic
        p.font.name = "Arial"
        p.font.italic = True
        p.font.size = Pt(12)
        p.font.color.rgb = EMERALD
        p.space_after = Pt(4)
        
        p = tf.add_paragraph()
        p.text = author_ic
        p.font.name = "Arial"
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_NAVY

    add_footer(slide3, "[Placeholder: Link to Full Verbatim Interview Transcripts]", 3)

    # ==========================================
    # SLIDE 4: Target Segment & Critical Drop-Off Moment
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Target Segment: Salaried First-Timers Entering the Month 2–6 \"Conviction Cliff\"",
               "Zero Prior Financial Literacy Meets the First Flat or Negative Market Correction Cycle")
    
    # Left Persona Card
    add_card(slide4, Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.2))
    tb_pers = slide4.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(5.0), Inches(4.8))
    tf_pers = tb_pers.text_frame
    tf_pers.word_wrap = True
    tf_pers.margin_left = tf_pers.margin_top = tf_pers.margin_right = tf_pers.margin_bottom = 0
    
    p = tf_pers.paragraphs[0]
    p.text = "👤 TARGET PERSONA: SUSHANT"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = DARK_NAVY
    p.space_after = Pt(8)
    
    persona_points = [
        ("Demographics: ", "27 years old, Salaried Software Engineer, Tier-1 Metro (Bengaluru)."),
        ("Investment Behavior: ", "Monthly SIP of ₹3,000 in Parag Parikh Flexi Cap Fund (Month 3 active)."),
        ("Goal & Motivation: ", "Long-term wealth compounding (5–10 years) inspired by colleagues."),
        ("Financial Literacy: ", "Zero prior stock/mutual fund experience; relies completely on Groww UI for guidance."),
        ("Behavioral Reality: ", "Checks portfolio 3–5 times per month; hyper-sensitive to red returns and macro headlines."),
        ("The Core Dilemma: ", "Experiences acute guilt when seeing paper loss; questions whether mutual funds are a gamble.")
    ]
    for pt_title, pt_desc in persona_points:
        p = tf_pers.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + pt_title
        r1.font.name = "Arial"
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = DARK_NAVY
        r2 = p.add_run()
        r2.text = pt_desc
        r2.font.name = "Arial"
        r2.font.size = Pt(11)
        r2.font.color.rgb = SLATE_BODY
        p.space_after = Pt(4)

    # Right Critical Moment Card
    add_card(slide4, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2))
    tb_crit = slide4.shapes.add_textbox(Inches(6.85), Inches(1.7), Inches(5.433), Inches(4.8))
    tf_crit = tb_crit.text_frame
    tf_crit.word_wrap = True
    tf_crit.margin_left = tf_crit.margin_top = tf_crit.margin_right = tf_crit.margin_bottom = 0
    
    p = tf_crit.paragraphs[0]
    p.text = "⚡ THE CRITICAL DROP-OFF MOMENT (MONTH 3)"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = CORAL_RED
    p.space_after = Pt(6)
    
    p = tf_crit.add_paragraph()
    p.text = "The Trigger Event: Month 3 auto-debit clears ₹3,000. Broader market undergoes a normal 4% dip."
    p.font.name = "Arial"
    p.font.size = Pt(11.5)
    p.font.color.rgb = SLATE_BODY
    p.space_after = Pt(6)

    # Visual Red Box
    p = tf_crit.add_paragraph()
    p.text = "What Groww Displays (Visual Panic Trigger):"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = DARK_NAVY
    p.space_after = Pt(2)
    
    p = tf_crit.add_paragraph()
    p.text = "  Total Invested: ₹9,000   |   Current Value: ₹8,480\n  Total Returns: -₹520.00 (-5.78%)   |   Annualized (XIRR): -14.2%"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = CORAL_RED
    p.space_after = Pt(8)

    breakdown_steps = [
        ("1. Paper Loss Panic: ", "Interprets -₹520 paper loss as capital vanished; fears platform is misleading him."),
        ("2. Jargon Alienation: ", "Sees -14.2% XIRR and assumes he lost 14% of total principal."),
        ("3. YouTube Deflection: ", "Leaves app to seek help; gets overwhelmed by sensationalized finfluencer videos."),
        ("4. Permanent Churn: ", "At the first sign of month-end cash tightness, cancels SIP mandate completely.")
    ]
    for st_title, st_desc in breakdown_steps:
        p = tf_crit.add_paragraph()
        r1 = p.add_run()
        r1.text = st_title
        r1.font.name = "Arial"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = DARK_NAVY
        r2 = p.add_run()
        r2.text = st_desc
        r2.font.name = "Arial"
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = SLATE_BODY
        p.space_after = Pt(3)

    add_footer(slide4, "[Placeholder: Link to User Journey & Friction Mapping]", 4)

    # ==========================================
    # SLIDE 5: Defining the Problem (6-Box Framework)
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Defining the Problem: The NextLeap 6-Box Framework",
               "Framing Root Causes, Target Cohort, Validation Evidence, Business Value, and Strategic Timing")
    
    t_shape5 = slide5.shapes.add_table(2, 3, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.2))
    table5 = t_shape5.table
    table5.columns[0].width = Inches(3.911)
    table5.columns[1].width = Inches(3.911)
    table5.columns[2].width = Inches(3.911)
    table5.rows[0].height = Inches(2.6)
    table5.rows[1].height = Inches(2.6)

    boxes = [
        (0, 0, "1. THE PROBLEM",
         "First-time mutual fund investors on Groww pause or cancel their SIPs within 12 months because the investment dashboard overwhelms them with complex financial terminologies and numbers, offering zero guidance on what to track or how their money is actually growing—leading to cognitive fatigue and a loss of conviction when markets dip or finances tighten."),
        (0, 1, "2. TARGET SEGMENT",
         "First-Time SIP Investors in Months 2–6:\nSalaried retail investors (age 22–30, SIP ₹1k–₹5k/mo) with long-term wealth goals but zero prior financial literacy, who enter Groww with high optimism but encounter their first flat/negative return cycle during a market dip."),
        (0, 2, "3. HOW WE KNOW IT'S REAL",
         "Direct Primary & Secondary Validation:\n• Sushant (27): \"Identifying what to track was very difficult. Made me consider stopping my SIP.\"\n• Pradhul (36): \"No info in layman language... tailor-made for veterans.\"\n• Secondary: 64% of beginner negative reviews cite confusion over red returns."),
        (1, 0, "4. VALUE FOR THE BUSINESS",
         "Plugs the 12-Month SIP Churn Cliff:\nRetaining users past Months 2–6 boosts 12-month active SIP rates (>75% survival post-M6). Retained investors naturally step up SIP amounts, expanding Groww's compounding AUM and Lifetime Value while protecting acquisition CAC."),
        (1, 1, "5. VALUE FOR THE USERS",
         "Replaces Anxiety with Habit Conviction:\nTranslates complex jargon into plain-English progress. Explains that market dips buy cheaper units (Rupee-Cost Averaging), protecting users from panic-stopping wealth creation and helping them achieve 10-year goals."),
        (1, 2, "6. WHY SOLVING MAKES SENSE",
         "Bridging the Product DNA Gap:\nGroww's UI originated from active stock trading (daily P&L, live ticks). Applying trading UI to a 10-year SIP product misaligns first-timers. Contextualizing metrics turns Groww into a trusted wealth partner rather than a transactional broker.")
    ]

    for r_idx, c_idx, b_title, b_desc in boxes:
        cell = table5.cell(r_idx, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BG
        tf = cell.text_frame
        tf.word_wrap = True
        tf.clear()
        
        p = tf.paragraphs[0]
        p.text = b_title
        p.font.name = "Arial"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = EMERALD if "VALUE" in b_title else DARK_NAVY
        p.space_after = Pt(4)
        for r in p.runs:
            r.font.name = "Arial"
            r.font.bold = True
            r.font.color.rgb = EMERALD if "VALUE" in b_title else DARK_NAVY
        
        p2 = tf.add_paragraph()
        p2.text = b_desc
        p2.font.name = "Arial"
        p2.font.size = Pt(10)
        p2.font.color.rgb = SLATE_BODY
        for r in p2.runs:
            r.font.name = "Arial"
            r.font.color.rgb = SLATE_BODY

    add_footer(slide5, "[Placeholder: Link to Problem Definition Working Doc]", 5)

    # ==========================================
    # SLIDE 6: Picking the Solution (Champion + RICE)
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Prioritizing an In-Context AI Companion to Translate Data into Conviction",
               "Evaluating Solution Archetypes via RICE Scoring (Reach, Impact, Confidence, Effort)")
    
    # Top Solution Archetypes
    # Champion
    c_champ = add_card(slide6, Inches(0.8), Inches(1.5), Inches(5.7), Inches(2.5), bg_color=LIGHT_EMR, border_color=EMERALD)
    tb = slide6.shapes.add_textbox(Inches(0.95), Inches(1.6), Inches(5.4), Inches(2.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "👑 SELECTED CHAMPION: GROWW PERSPECTIVE (AI Companion)"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = EMERALD
    p.space_after = Pt(3)
    p = tf.add_paragraph()
    p.text = "• Core Mechanism: Synthesizes raw ledger state into 3-card Monthly Debrief + NAV Simulator + \"Ask About My SIP\" decryptor with SEBI eval-gates.\n• Why It Wins: Dynamically personalizes each user's exact numbers (78.70 discounted units bought), which static text cannot do.\n• Defends Habit: Pairs plain-English education with 1-click non-punitive Skip/Pause flexibility."
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.color.rgb = SLATE_BODY

    # Rejected Alternatives
    c_rej = add_card(slide6, Inches(6.8), Inches(1.5), Inches(5.733), Inches(2.5))
    tb = slide6.shapes.add_textbox(Inches(6.95), Inches(1.6), Inches(5.433), Inches(2.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "❌ EVALUATED & REJECTED ALTERNATIVES"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = CORAL_RED
    p.space_after = Pt(3)
    p = tf.add_paragraph()
    p.text = "1. Groww Clarity View (Beginner Mode Toggle):\n• What it is: A simple toggle switch that hides NAV and XIRR numbers.\n• Why Rejected: Passive hiding does not build financial conviction. Users still panic when total value drops below invested amount during market dips.\n\n2. Static Tooltips & In-App Articles (Groww Academy 2.0):\n• What it is: Infotip popups and educational articles on mutual fund basics.\n• Why Rejected: High cognitive load. Users in financial panic do not read generic 800-word articles. Cannot compute personal unit savings."
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_BODY

    # Bottom RICE Table
    t_shape6 = slide6.shapes.add_table(4, 7, Inches(0.8), Inches(4.2), Inches(11.733), Inches(2.6))
    table6 = t_shape6.table
    r_widths = [Inches(3.733), Inches(1.3), Inches(1.3), Inches(1.4), Inches(1.3), Inches(1.4), Inches(1.3)]
    for i, w in enumerate(r_widths):
        table6.columns[i].width = w

    rice_headers = ["Solution Concept", "Reach (1–10)", "Impact (1–3)", "Confidence (0–1)", "Effort (1–5)", "RICE Score", "Rank"]
    for i, h in enumerate(rice_headers):
        cell = table6.cell(0, i)
        format_cell(cell, h, font_size=11, bold=True, color=DARK_NAVY, align=PP_ALIGN.CENTER, bg_color=LIGHT_HDR)

    rice_rows = [
        ("👑 Groww Perspective (In-Context AI Companion)", "8", "3", "0.90", "3", "7.20", "Rank 1 (Selected)"),
        ("Groww Clarity View (Beginner Mode Toggle)", "7", "2", "0.80", "3", "3.73", "Rank 2"),
        ("Static Tooltips & Nudges (Academy 2.0)", "7", "1", "0.70", "2", "2.45", "Rank 3")
    ]
    for row_idx, r_data in enumerate(rice_rows, start=1):
        for col_idx, val in enumerate(r_data):
            cell = table6.cell(row_idx, col_idx)
            align_c = PP_ALIGN.CENTER if col_idx in [1, 2, 3, 4, 5, 6] else PP_ALIGN.LEFT
            if row_idx == 1:
                col_c = EMERALD if col_idx in [0, 5, 6] else DARK_NAVY
                format_cell(cell, val, font_size=10.5, bold=True, color=col_c, align=align_c, bg_color=LIGHT_EMR)
            else:
                format_cell(cell, val, font_size=10, bold=False, color=DARK_NAVY, align=align_c, bg_color=WHITE)

    add_footer(slide6, "[Placeholder: Link to Full RICE Prioritization Model]", 6)

    # ==========================================
    # SLIDE 7: The Solution in Action (MVP Walkthrough)
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "An Eval-Gated, SEBI-Compliant In-App Companion Built and Deployed",
               "4-Pillar Architecture Translating Ledger Data into Plain-Language Conviction & Flexibility")
    
    screens = [
        ("1. Contextual Anchor", "holdings_dashboard_2_clean.png",
         "Holdings surface reframes -₹520 loss via October Perspective card before panic sets in."),
        ("2. Cognitive Reframing", "story_mode_card2_clean.png",
         "Proves mathematically that market dip bought 78.70 discounted units (+6.55 extra units)."),
        ("3. Plain-English Decryptor", "ask_ai_reassurance_clean.png",
         "Speedometer metaphor for XIRR + Verified Ledger (Score: 100/100) SEBI compliance badge."),
        ("4. Smart Exit Flexibility", "smart_exit_flow_1_clean.png",
         "Non-punitive 1-click Skip 1 Month (zero fee) or 1–6 Month Pause with zero dark patterns.")
    ]

    card_w = Inches(2.75)
    gap = Inches(0.244)
    for idx, (s_title, s_file, s_desc) in enumerate(screens):
        pos_x = Inches(0.8) + idx * (card_w + gap)
        add_card(slide7, pos_x, Inches(1.5), card_w, Inches(5.2))
        
        # Title
        tb = slide7.shapes.add_textbox(pos_x, Inches(1.55), card_w, Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = s_title
        p.font.name = "Arial"
        p.font.bold = True
        p.font.size = Pt(11)
        p.alignment = PP_ALIGN.CENTER
        p.font.color.rgb = DARK_NAVY
        
        # Image
        img_path = os.path.join("./screenshots/clean", s_file)
        if os.path.exists(img_path):
            slide7.shapes.add_picture(img_path, pos_x + Inches(0.15), Inches(2.0), card_w - Inches(0.3), Inches(3.65))
        
        # Description
        tb_desc = slide7.shapes.add_textbox(pos_x + Inches(0.1), Inches(5.7), card_w - Inches(0.2), Inches(0.95))
        tf_d = tb_desc.text_frame
        tf_d.word_wrap = True
        p = tf_d.paragraphs[0]
        p.text = s_desc
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.color.rgb = SLATE_BODY
        p.alignment = PP_ALIGN.CENTER

    add_footer(slide7, "[Placeholder: Link to Live Interactive MVP & Evidence Log]", 7)

    # ==========================================
    # SLIDE 8: User Testing Insights & V2 Roadmap (FIXED TEXT COLORS)
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Prototype Testing Validates Anxiety Reduction; Surfaces Demand for V2 Expansion",
               "Task-Based Usability Protocol with Target First-Time SIP Investors Using Live Production MVP")
    
    # Left Card: Validation Findings
    add_card(slide8, Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.2))
    tb8_l = slide8.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.1), Inches(4.8))
    tf8_l = tb8_l.text_frame
    tf8_l.word_wrap = True
    p = tf8_l.paragraphs[0]
    p.text = "✅ WHAT REAL USERS VALIDATED (CONFIRMED)"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = EMERALD
    p.space_after = Pt(6)

    validations = [
        ("Uncluttered & Focused Mobile UI: ",
         "“Data was not cluttered at all, very easy to focus on each button and metric... pretty self-explanatory.” Validates departure from trading clutter."),
        ("NAV Simulator as Anxiety Diffuser: ",
         "“Gave a very clear explanation... the NAV Simulator will be very helpful for beginners to reduce anxiety.” Validates cognitive reframing hypothesis."),
        ("Layman Jargon Decryption: ",
         "“Very accurate and free of jargon, especially explaining what XIRR is and why it's noisy in Months 1 to 6... understood by any layman.”"),
        ("Habit Defense via Flexibility: ",
         "“If I face a tight month I would definitely use this... can skip 1 month or manually select months to pause with immediate effect.”")
    ]
    for v_title, v_desc in validations:
        p = tf8_l.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + v_title
        r1.font.name = "Arial"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = DARK_NAVY
        r2 = p.add_run()
        r2.text = v_desc
        r2.font.name = "Arial"
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = SLATE_BODY
        p.space_after = Pt(4)

    # Right Card: Prioritized V2 Roadmap Table (100% EXPLICIT DARK TEXT)
    add_card(slide8, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2))
    tb8_r = slide8.shapes.add_textbox(Inches(6.8), Inches(1.7), Inches(5.533), Inches(0.4))
    tf8_r = tb8_r.text_frame
    p = tf8_r.paragraphs[0]
    p.text = "📋 PRIORITIZED V2 ROADMAP (FROM USER TESTING)"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = DARK_NAVY

    t_shape8 = slide8.shapes.add_table(5, 4, Inches(6.8), Inches(2.2), Inches(5.533), Inches(4.3))
    t8 = t_shape8.table
    t8.columns[0].width = Inches(0.9)
    t8.columns[1].width = Inches(2.033)
    t8.columns[2].width = Inches(1.8)
    t8.columns[3].width = Inches(0.8)

    t8_headers = ["Priority", "V2 Enhancement", "Feedback Solved", "Effort"]
    for i, h in enumerate(t8_headers):
        cell = t8.cell(0, i)
        format_cell(cell, h, font_size=11, bold=True, color=DARK_NAVY, align=PP_ALIGN.CENTER, bg_color=LIGHT_HDR)

    v2_rows = [
        ("P0", "Opportunistic Dip Top-Up\n(1-Click Lump Sum in Story)", "Desire to invest extra when units are on discount (Request a).", "Med"),
        ("P0", "Pre-Debit Advance Intimations\n(3 Days Prior + 1-Click Skip)", "Prevents mandate bounce penalties and salary delay panic.", "Low"),
        ("P1", "Groww Wallet Auto-Fallback\nMandate Integration", "Enables funding SIP via wallet when bank balance is low (Request d).", "Med"),
        ("P1", "Goal-Based Exploration &\nFull Redemption Flow", "User request to discover new funds and manage exits (Requests b & c).", "High")
    ]
    for r_idx, r_vals in enumerate(v2_rows, start=1):
        for c_idx, val in enumerate(r_vals):
            cell = t8.cell(r_idx, c_idx)
            align_c = PP_ALIGN.CENTER if c_idx in [0, 3] else PP_ALIGN.LEFT
            bold_c = True if c_idx in [0, 3] else False
            color_c = EMERALD if c_idx == 0 else (DARK_NAVY if c_idx == 3 else SLATE_BODY)
            format_cell(cell, val, font_size=10, bold=bold_c, color=color_c, align=align_c, bg_color=WHITE)

    add_footer(slide8, "[Placeholder: Link to User Testing Transcripts & V2 PRD]", 8)

    # ==========================================
    # SLIDE 9: GTM Strategy & Measuring Success
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "GTM Strategy and Measuring Success",
               "Phased Rollout Plan & Guardrailed Metrics Architecture to Defend 12-Month SIP Retention")
    
    # Left Card: GTM Rollout
    add_card(slide9, Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.2))
    tb9_l = slide9.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.1), Inches(4.8))
    tf9_l = tb9_l.text_frame
    tf9_l.word_wrap = True
    p = tf9_l.paragraphs[0]
    p.text = "🚀 4-PHASE GTM STAGED ROLLOUT STRATEGY"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = DARK_NAVY
    p.space_after = Pt(6)

    gtm_phases = [
        ("Phase 1: Validation & Legal Gate (Weeks 1–2)",
         "Internal dogfooding & compliance review. Benchmark on 20-case Golden Set (100% adherence, zero SEBI advice breaches, deterministic Python math)."),
        ("Phase 2: Canary Beta Launch (Weeks 3–6)",
         "Canary deployment to 10,000 first-time investors entering Month 3. Monitor story completion rates, AI query themes, and support deflection."),
        ("Phase 3: Staged Rollout & A/B Experimentation (Weeks 7–12)",
         "50/50 randomized control trial during next market correction. Measure Net Negative-Market Retention Delta between treatment and control."),
        ("Phase 4: Full Scale & Contextual Adoption (Month 4+)",
         "100% rollout across all first-time mutual fund investors on Groww. Embed contextual entry points: monthly ledger debriefs & 3-day pre-debit alerts.")
    ]
    for ph_title, ph_desc in gtm_phases:
        p = tf9_l.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + ph_title + ": "
        r1.font.name = "Arial"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = DARK_NAVY
        r2 = p.add_run()
        r2.text = ph_desc
        r2.font.name = "Arial"
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = SLATE_BODY
        p.space_after = Pt(4)

    # Right Card: Metrics Architecture
    add_card(slide9, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2))
    tb9_r = slide9.shapes.add_textbox(Inches(6.85), Inches(1.7), Inches(5.433), Inches(4.8))
    tf9_r = tb9_r.text_frame
    tf9_r.word_wrap = True
    p = tf9_r.paragraphs[0]
    p.text = "📊 GUARDRAILED METRICS ARCHITECTURE"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = DARK_NAVY
    p.space_after = Pt(6)

    metrics_arch = [
        ("🌟 North Star Metric: ", "12-Month Active SIP Continuation Rate (% of first-timers with ≥1 successful debit in trailing 30 days at Month 12)."),
        ("⏩ Leading Indicators: ", "• Story Mode Completion Rate (≥65% target)\n• AI Query Resolution Rate (>85% target)\n• Flexibility Adoption Rate (Skip/Pause chosen vs cancel >50%)"),
        ("📈 Lagging Indicators: ", "• Month 2–6 Churn Cliff Survival Rate (>75% survival post-M6)\n• Net Negative-Market Retention Delta (+5% to +8% over control)\n• 12-Month Active SIP Retention Rate (50% ➔ 56% lift)"),
        ("🛡️ Guard Rail Metrics: ", "• SEBI Advice Breaches: Strictly 0% (zero stock/fund tips)\n• Arithmetic Accuracy: 100% deterministic (Python ledger)\n• Cancellation Flow Friction: <15s (zero dark patterns)\n• App Page Load Latency: <200ms via overnight pre-computation")
    ]
    for m_title, m_desc in metrics_arch:
        p = tf9_r.add_paragraph()
        r1 = p.add_run()
        r1.text = m_title
        r1.font.name = "Arial"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = EMERALD if "North Star" in m_title else DARK_NAVY
        r2 = p.add_run()
        r2.text = m_desc
        r2.font.name = "Arial"
        r2.font.size = Pt(10)
        r2.font.color.rgb = SLATE_BODY
        p.space_after = Pt(3)

    add_footer(slide9, "[Placeholder: Link to GTM Experimentation Protocol]", 9)

    # ==========================================
    # SLIDE 10: Measuring the Impact and Risks
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "Measuring the Impact and Risks",
               "Multi-Year Enterprise Financial Impact Sizing & Pre-Mortem Risk Mitigation Strategies")
    
    # Left Card: Impact Sizing
    add_card(slide10, Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.2))
    tb10_l = slide10.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.1), Inches(4.8))
    tf10_l = tb10_l.text_frame
    tf10_l.word_wrap = True
    p = tf10_l.paragraphs[0]
    p.text = "💰 BUSINESS IMPACT SIZING (FINANCIAL MODEL)"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = EMERALD
    p.space_after = Pt(6)

    impact_points = [
        ("Addressable Population: ", "Groww onboards ~500,000 first-time mutual fund investors monthly (~6M annually)."),
        ("The Churn Problem Baseline: ", "Current 12-month retention is ~50% (steepest 40% cliff concentrated in Months 2–6)."),
        ("Target Retention Lift: ", "Conservative +6.0% absolute lift in 12-month active SIP retention (50.0% ➔ 56.0%)."),
        ("Incremental Retained Investors: ", "500,000 × 6% = 30,000 users/month ➔ 360,000 additional active investors/year."),
        ("Direct Net AUM Preserved (Year 1): ", "At avg ₹2,500/mo SIP (₹30k/yr): 360k × ₹30k = ₹1,080 Crores direct AUM preserved."),
        ("Compounding Lifetime AUM (Year 3): ", "With >75% multi-year survival and 10% annual step-up: ₹4,500+ Crores AUM."),
        ("Marketing CAC Efficiency Savings: ", "360k users × ₹1,500 CAC = ₹54 Crores/year saved in otherwise wasted acquisition marketing.")
    ]
    for ip_title, ip_desc in impact_points:
        p = tf10_l.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + ip_title
        r1.font.name = "Arial"
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = DARK_NAVY
        r2 = p.add_run()
        r2.text = ip_desc
        r2.font.name = "Arial"
        r2.font.size = Pt(10)
        r2.font.color.rgb = SLATE_BODY
        p.space_after = Pt(2)

    # Right Card: Risk & Mitigation Strategies
    add_card(slide10, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2))
    tb10_r = slide10.shapes.add_textbox(Inches(6.85), Inches(1.7), Inches(5.433), Inches(4.8))
    tf10_r = tb10_r.text_frame
    tf10_r.word_wrap = True
    p = tf10_r.paragraphs[0]
    p.text = "🛡️ PRE-MORTEM RISK & MITIGATION STRATEGIES"
    p.font.name = "Arial"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = CORAL_RED
    p.space_after = Pt(6)

    risks = [
        ("1. Regulatory & SEBI Advice Risk (Critical):",
         "Risk: AI conversational outputs construed as unregistered investment advice.\nMitigation: Hard-coded Tier 1 Advisory Interceptor immediately detects buy/sell/switch intents and deflects to certified advisors with mandatory disclaimer. Strictly 0% breaches (20/20 Golden Set)."),
        ("2. Arithmetic & Ledger Hallucination Risk:",
         "Risk: Generative token sampling fabricating incorrect returns or XIRR.\nMitigation: Zero runtime LLM math. All ledger metrics pre-computed deterministically in Python (portfolio_data.py). 100% deterministic agreement between ledger and UI."),
        ("3. Operational Churn & Mandate Penalty Risk:",
         "Risk: Salary delays causing debit bounces and ₹250–₹500 bank penalty fees.\nMitigation: 3-day advance pre-debit notifications via WhatsApp with 1-click non-punitive Skip 1 Month or Move Date to 10th (Salary Day). Reduces bounce churn by ≥35%."),
        ("4. App Performance & Page Latency Risk:",
         "Risk: Real-time LLM inference adding 2–4s loading delay to core holdings screen.\nMitigation: Asynchronous overnight batch pre-computation post-market close. Stored in low-latency cache, ensuring <200ms instantaneous native UI render.")
    ]
    for r_title, r_desc in risks:
        p = tf10_r.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + r_title + "\n"
        r1.font.name = "Arial"
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = DARK_NAVY
        r2 = p.add_run()
        r2.text = r_desc
        r2.font.name = "Arial"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = SLATE_BODY
        p.space_after = Pt(3)

    add_footer(slide10, "[Placeholder: Link to Risk & Compliance Register]", 10)

    # Save output
    pptx_path = "NL_Groww.pptx"
    prs.save(pptx_path)
    
    downloads_path = os.path.expanduser("~/Downloads/NL_Groww.pptx")
    shutil.copyfile(pptx_path, downloads_path)
    print(f"Presentation saved successfully at: {os.path.abspath(pptx_path)}")
    print(f"Presentation copied to Downloads: {downloads_path}")

if __name__ == '__main__':
    create_deck()
