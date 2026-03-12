import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Numad.AI — Identity Cloud",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── THEME ──────────────────────────────────────────────────────────────────────
GOLD    = "#D4A843"
TEAL    = "#1BBFA6"
BG      = "#04080F"
SURFACE = "#080E1A"
CARD    = "#0C1424"
BORDER  = "#1A2640"
TEXT    = "#E2D9C8"
MUTED   = "#6B7A99"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    background-color: {BG};
    color: {TEXT};
    font-family: 'DM Sans', sans-serif;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background-color: {SURFACE} !important;
    border-right: 1px solid {BORDER};
}}
section[data-testid="stSidebar"] * {{
    color: {TEXT} !important;
}}

/* Main area */
.main .block-container {{
    background-color: {BG};
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}}

/* Cards */
.numad-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}}
.numad-card-gold {{
    background: {CARD};
    border: 1.5px solid rgba(212,168,67,0.4);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 16px;
    box-shadow: 0 0 24px rgba(212,168,67,0.06);
}}
.numad-card-teal {{
    background: {CARD};
    border: 1.5px solid rgba(27,191,166,0.4);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 16px;
    box-shadow: 0 0 24px rgba(27,191,166,0.06);
}}

/* Typography */
.numad-title {{
    font-family: 'Cinzel', serif;
    color: {TEXT};
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
}}
.numad-subtitle {{
    color: {MUTED};
    font-size: 14px;
    margin-bottom: 32px;
    line-height: 1.6;
}}
.numad-label {{
    color: {GOLD};
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 12px;
}}
.numad-value {{
    font-family: 'Cinzel', serif;
    font-size: 32px;
    font-weight: 700;
    color: {GOLD};
    margin-bottom: 4px;
}}
.numad-value-teal {{
    font-family: 'Cinzel', serif;
    font-size: 32px;
    font-weight: 700;
    color: {TEAL};
    margin-bottom: 4px;
}}

/* Metrics */
.metric-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 22px 24px;
    border-top: 2px solid {GOLD};
    text-align: left;
}}
.metric-label {{
    color: {MUTED};
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
}}
.metric-value {{
    font-family: 'Cinzel', serif;
    font-size: 28px;
    color: {GOLD};
    font-weight: 700;
}}
.metric-sub {{
    color: {MUTED};
    font-size: 11px;
    margin-top: 4px;
}}

/* Tags / badges */
.badge-gold {{
    background: rgba(212,168,67,0.15);
    color: {GOLD};
    border: 1px solid rgba(212,168,67,0.3);
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
}}
.badge-teal {{
    background: rgba(27,191,166,0.15);
    color: {TEAL};
    border: 1px solid rgba(27,191,166,0.3);
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
}}
.badge-neutral {{
    background: rgba(107,122,153,0.15);
    color: {MUTED};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
}}

/* Partner rows */
.partner-row {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 14px;
    cursor: pointer;
    transition: border-color 0.2s;
}}

/* Progress bar */
.progress-wrap {{
    background: {BORDER};
    border-radius: 4px;
    height: 7px;
    margin-bottom: 6px;
    overflow: hidden;
}}

/* Divider */
.numad-divider {{
    border: none;
    border-top: 1px solid {BORDER};
    margin: 24px 0;
}}

/* Step indicator */
.step-active {{
    color: {GOLD};
    font-weight: 700;
}}
.step-done {{
    color: {TEAL};
}}
.step-pending {{
    color: {MUTED};
}}

/* Table */
.numad-table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
}}
.numad-table th {{
    background: {SURFACE};
    color: {MUTED};
    font-weight: 600;
    letter-spacing: 1px;
    font-size: 11px;
    text-transform: uppercase;
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid {BORDER};
}}
.numad-table td {{
    padding: 13px 16px;
    border-bottom: 1px solid {BORDER};
    color: {TEXT};
}}
.numad-table tr:last-child td {{
    border-bottom: none;
}}
code {{
    background: {SURFACE};
    color: {TEAL};
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 12px;
    border: 1px solid {BORDER};
}}

/* Hide streamlit default elements */
#MainMenu, footer, header {{visibility: hidden;}}
.stDeployButton {{display: none;}}
div[data-testid="stToolbar"] {{display: none;}}

/* Button overrides */
.stButton > button {{
    background: linear-gradient(135deg, {GOLD}, #8B6914) !important;
    color: #000 !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    padding: 10px 28px !important;
    font-size: 14px !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
}}
.stButton > button:hover {{
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}}

/* Select box */
.stSelectbox > div > div {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT} !important;
    border-radius: 8px !important;
}}

/* Multiselect */
.stMultiSelect > div > div {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
}}

/* Checkbox */
.stCheckbox > label > span {{
    color: {TEXT} !important;
}}

/* Info/success boxes */
.stAlert {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
}}

/* Expander */
.streamlit-expanderHeader {{
    background: {CARD} !important;
    color: {TEXT} !important;
    border-radius: 8px !important;
    font-family: 'DM Sans' !important;
}}
</style>
""", unsafe_allow_html=True)


# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Platform Overview"
if "onboard_step" not in st.session_state:
    st.session_state.onboard_step = 0
if "selected_sources" not in st.session_state:
    st.session_state.selected_sources = []
if "active_dests" not in st.session_state:
    st.session_state.active_dests = []
if "ingestion_done" not in st.session_state:
    st.session_state.ingestion_done = False


# ─── DATA ────────────────────────────────────────────────────────────────────
RMN_PARTNERS = [
    {"name": "Noon",              "type": "RMN", "color": "#FFC200", "desc": "UAE/KSA e-commerce leader",   "reach": "12M registered users",  "format": "Sponsored Products, Display"},
    {"name": "Carrefour Arabia",  "type": "RMN", "color": "#004F9F", "desc": "Grocery & general merchandise", "reach": "8M loyalty members",   "format": "In-store + Digital"},
    {"name": "LuLu Hypermarket",  "type": "RMN", "color": "#00843D", "desc": "GCC hypermarket RMN",          "reach": "6.4M customers",        "format": "Display, Sponsored"},
    {"name": "Panda Retail",      "type": "RMN", "color": "#E8453C", "desc": "KSA largest grocery chain",    "reach": "9.1M loyalty holders",  "format": "Offsite + Onsite"},
    {"name": "Jarir Bookstore",   "type": "RMN", "color": "#CC0000", "desc": "Electronics & office RMN",     "reach": "4.2M members",          "format": "Display, Email"},
    {"name": "Danube Home",       "type": "RMN", "color": "#8B4513", "desc": "Premium grocery & home",       "reach": "3.1M shoppers",         "format": "Sponsored, CTV"},
]

ADTECH_PARTNERS = [
    {"name": "Google DV360",      "type": "DSP",     "color": "#4285F4", "desc": "Display & Video 360",    "reach": "40M+ MENA",    "signal": "PPID / Customer Match"},
    {"name": "Meta Business",     "type": "Social",  "color": "#0668E1", "desc": "Facebook & Instagram",   "reach": "35M+ MENA",    "signal": "Custom Audience"},
    {"name": "Snapchat",          "type": "Social",  "color": "#FFDD00", "desc": "No. 1 app in KSA",       "reach": "21M KSA",      "signal": "Snap Audience Match"},
    {"name": "TikTok for Business","type": "Social", "color": "#FF0050", "desc": "Short-form video leader", "reach": "18.4M MENA",   "signal": "Custom Audience"},
    {"name": "Amazon DSP",        "type": "DSP",     "color": "#FF9900", "desc": "Amazon demand-side",      "reach": "10M+ KSA",     "signal": "Amazon Audiences"},
    {"name": "The Trade Desk",    "type": "DSP",     "color": "#17E9E0", "desc": "Open internet DSP",       "reach": "Open web",     "signal": "UID 2.0"},
    {"name": "Criteo Commerce",   "type": "DSP",     "color": "#FF6B2B", "desc": "Commerce media platform", "reach": "KSA + UAE",    "signal": "Commerce Audiences"},
    {"name": "STC Ads",           "type": "Telco",   "color": "#7B2D8B", "desc": "Telecom 1P data network", "reach": "30M KSA subs", "signal": "Mobile Identity"},
]

DATA_SOURCES = [
    {"id": "crm",     "label": "CRM / Customer Database",  "icon": "CRM", "fields": ["Email", "Phone", "Customer ID", "Name"]},
    {"id": "ecomm",   "label": "E-commerce Platform",       "icon": "SHP", "fields": ["Order ID", "Email", "Device ID", "Cart Value"]},
    {"id": "loyalty", "label": "Loyalty Programme",         "icon": "LYL", "fields": ["Member ID", "Email", "Mobile", "Tier"]},
    {"id": "pos",     "label": "Point of Sale (POS)",       "icon": "POS", "fields": ["Transaction ID", "Phone", "Card Hash", "Store ID"]},
    {"id": "app",     "label": "Mobile Application",        "icon": "APP", "fields": ["IDFA / GAID", "Email", "User ID", "Push Token"]},
    {"id": "cdp",     "label": "CDP / DMP Segment Export",  "icon": "CDP", "fields": ["Universal ID", "Segment", "Score", "Frequency"]},
]

SEGMENTS = [
    {"name": "High-Value Shoppers",      "size": "420K",  "iScore": 92, "color": GOLD},
    {"name": "Grocery Loyalists",        "size": "1.1M",  "iScore": 87, "color": TEAL},
    {"name": "Electronics Intenders",    "size": "280K",  "iScore": 81, "color": "#A78BFA"},
    {"name": "Ramadan Buyers",           "size": "890K",  "iScore": 95, "color": "#F472B6"},
    {"name": "Auto In-Market",           "size": "145K",  "iScore": 78, "color": "#60A5FA"},
    {"name": "Pharma & Health",          "size": "330K",  "iScore": 84, "color": "#34D399"},
    {"name": "Vision 2030 Consumers",    "size": "660K",  "iScore": 89, "color": GOLD},
    {"name": "KSA New Residents",        "size": "88K",   "iScore": 91, "color": "#FB923C"},
]


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 20px 0 28px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
            <div style="width:34px;height:34px;background:linear-gradient(135deg,{GOLD},{TEAL});
                        border-radius:8px;display:flex;align-items:center;justify-content:center;
                        font-family:'Cinzel',serif;font-size:16px;font-weight:900;color:#000;">N</div>
            <span style="font-family:'Cinzel',serif;font-size:17px;font-weight:700;
                         color:{TEXT};letter-spacing:1px;">NUMAD<span style="color:{GOLD};">.AI</span></span>
        </div>
        <div style="background:{CARD};border:1px solid {BORDER};border-radius:8px;
                    padding:5px 12px;font-size:10px;color:{MUTED};letter-spacing:2px;
                    font-weight:600;display:inline-block;">IDENTITY CLOUD</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='color:{MUTED};font-size:10px;letter-spacing:2px;font-weight:600;margin-bottom:10px;padding:0 4px;'>NAVIGATION</div>", unsafe_allow_html=True)

    pages = [
        ("Platform Overview",   "01", "Overview"),
        ("Data Onboarding",     "02", "Onboard IDs"),
        ("Identity Graph",      "03", "ID Graph"),
        ("Activation Hub",      "04", "Activate"),
        ("Intelligence",        "05", "Measure"),
        ("Tech Specification",  "06", "Tech Spec"),
    ]

    for page, num, label in pages:
        is_active = st.session_state.page == page
        bg = f"rgba(212,168,67,0.12)" if is_active else "transparent"
        col = GOLD if is_active else MUTED
        border_left = f"3px solid {GOLD}" if is_active else f"3px solid transparent"
        if st.button(f"  {num}  {label}", key=f"nav_{page}", use_container_width=True):
            st.session_state.page = page
            st.rerun()

    st.markdown("<div style='height:1px;background:#1A2640;margin:24px 0 20px'/>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="padding:14px 12px;background:{CARD};border:1px solid {BORDER};border-radius:10px;">
        <div style="font-size:11px;color:{MUTED};font-weight:600;letter-spacing:1px;margin-bottom:12px;">SNOWFLAKE STATUS</div>
        <div style="font-size:12px;color:{TEXT};margin-bottom:6px;">
            <span style="color:{TEAL};margin-right:6px;">&#9679;</span>Clean Room Active
        </div>
        <div style="font-size:12px;color:{TEXT};margin-bottom:6px;">
            <span style="color:{TEAL};margin-right:6px;">&#9679;</span>DCR Spec v2.4
        </div>
        <div style="font-size:12px;color:{TEXT};">
            <span style="color:{GOLD};margin-right:6px;">&#9675;</span>KSA Region: me-central-1
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-top:20px;padding:0 4px;">
        <div style="font-size:11px;color:{MUTED};margin-bottom:4px;">Powered by</div>
        <div style="font-size:12px;color:{TEXT};font-weight:600;">Snowflake Data Clean Rooms</div>
        <div style="font-size:11px;color:{MUTED};">Saudi PDPL Certified</div>
    </div>
    """, unsafe_allow_html=True)


# ─── PAGE: PLATFORM OVERVIEW ──────────────────────────────────────────────────
if st.session_state.page == "Platform Overview":
    st.markdown(f"""
    <div class="numad-label">SNOWFLAKE-NATIVE IDENTITY RESOLUTION</div>
    <div class="numad-title">The Identity Cloud for Saudi Arabia</div>
    <div class="numad-subtitle">
        Onboard, resolve, and activate your customer identities across KSA's fastest-growing retail media ecosystem.<br>
        Privacy-safe. Snowflake-native. Built for Vision 2030.
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    kpi_cols = st.columns(4)
    kpis = [
        ("2.4B+",  "IDs in Numad Graph",      "Across GCC markets"),
        ("94.2%",  "Average Match Rate",       "Industry avg: 68%"),
        ("42",     "Activation Endpoints",     "RMN + DSP networks"),
        ("< 48h",  "Time to First Activation", "From raw data upload"),
    ]
    for col, (val, label, sub) in zip(kpi_cols, kpis):
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{val}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='numad-divider'/>", unsafe_allow_html=True)

    # Pipeline
    st.markdown(f"<div style='color:{TEXT};font-size:14px;font-weight:700;letter-spacing:0.5px;margin-bottom:20px;'>END-TO-END IDENTITY PIPELINE</div>", unsafe_allow_html=True)

    pipeline_cols = st.columns(6)
    steps = [
        ("Ingest",       "Raw ID Onboarding",       GOLD,      "01"),
        ("Normalise",    "Schema Harmonisation",    "#A78BFA",  "02"),
        ("Hash",         "PII Encryption",          "#60A5FA",  "03"),
        ("Graph Build",  "Identity Resolution",     TEAL,       "04"),
        ("Enrich",       "Audience Intelligence",   "#F472B6",  "05"),
        ("Activate",     "Destination Push",        GOLD,       "06"),
    ]
    for col, (label, sub, color, num) in zip(pipeline_cols, steps):
        col.markdown(f"""
        <div style="text-align:center;padding:16px 8px;background:{CARD};border:1px solid {BORDER};
                    border-radius:12px;border-top:2px solid {color};">
            <div style="font-family:'Cinzel',serif;font-size:18px;color:{color};
                        font-weight:700;margin-bottom:8px;">{num}</div>
            <div style="font-size:13px;color:{TEXT};font-weight:700;margin-bottom:4px;">{label}</div>
            <div style="font-size:11px;color:{MUTED};">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='numad-divider'/>", unsafe_allow_html=True)

    # Market context
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="numad-card-gold">
            <div style="color:{GOLD};font-size:11px;letter-spacing:2px;font-weight:700;margin-bottom:16px;">KSA MARKET CONTEXT</div>
            <table class="numad-table">
                <tr><td style="color:{MUTED};">Internet users</td><td style="color:{TEXT};font-weight:600;text-align:right;">36.9M</td></tr>
                <tr><td style="color:{MUTED};">Mobile penetration</td><td style="color:{TEXT};font-weight:600;text-align:right;">98.4%</td></tr>
                <tr><td style="color:{MUTED};">E-commerce GMV (2024)</td><td style="color:{TEXT};font-weight:600;text-align:right;">SAR 42B</td></tr>
                <tr><td style="color:{MUTED};">Retail media ad spend</td><td style="color:{TEXT};font-weight:600;text-align:right;">SAR 1.8B</td></tr>
                <tr><td style="color:{MUTED};">YoY retail media growth</td><td style="color:{TEXT};font-weight:600;text-align:right;">+38%</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="numad-card-teal">
            <div style="color:{TEAL};font-size:11px;letter-spacing:2px;font-weight:700;margin-bottom:16px;">NUMAD ADVANTAGE</div>
            <table class="numad-table">
                <tr><td style="color:{MUTED};">Unique identifier types</td><td style="color:{TEXT};font-weight:600;text-align:right;">11</td></tr>
                <tr><td style="color:{MUTED};">Avg IDs per person</td><td style="color:{TEXT};font-weight:600;text-align:right;">3.7</td></tr>
                <tr><td style="color:{MUTED};">Deterministic match rate</td><td style="color:{TEXT};font-weight:600;text-align:right;">94.2%</td></tr>
                <tr><td style="color:{MUTED};">Saudi PDPL compliance</td><td style="color:{TEXT};font-weight:600;text-align:right;">Certified</td></tr>
                <tr><td style="color:{MUTED};">Data residency</td><td style="color:{TEXT};font-weight:600;text-align:right;">KSA (me-central-1)</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    # CTA row
    st.markdown("<div style='height:8px'/>", unsafe_allow_html=True)
    cta1, cta2, _ = st.columns([1, 1, 2])
    with cta1:
        if st.button("Start Onboarding"):
            st.session_state.page = "Data Onboarding"
            st.rerun()
    with cta2:
        if st.button("View Identity Graph"):
            st.session_state.page = "Identity Graph"
            st.rerun()


# ─── PAGE: ONBOARDING ─────────────────────────────────────────────────────────
elif st.session_state.page == "Data Onboarding":
    st.markdown(f"""
    <div class="numad-label">STEP {st.session_state.onboard_step + 1} OF 4</div>
    <div class="numad-title">Data Onboarding</div>
    <div class="numad-subtitle">Connect your first-party data to the Numad Identity Graph on Snowflake</div>
    """, unsafe_allow_html=True)

    # Progress steps
    step_labels = ["Select Sources", "Map Schema", "Privacy Config", "Ingest & Validate"]
    prog_cols = st.columns(4)
    for i, (col, label) in enumerate(zip(prog_cols, step_labels)):
        if i < st.session_state.onboard_step:
            state_html = f"<span style='color:{TEAL};font-weight:700;'>&#10003;  {label}</span>"
        elif i == st.session_state.onboard_step:
            state_html = f"<span style='color:{GOLD};font-weight:700;'>&#9654;  {label}</span>"
        else:
            state_html = f"<span style='color:{MUTED};'>{i+1}.  {label}</span>"
        col.markdown(f"<div style='padding:12px 0;border-top:2px solid {'#D4A843' if i <= st.session_state.onboard_step else BORDER};font-size:13px;'>{state_html}</div>", unsafe_allow_html=True)

    st.markdown("<div class='numad-divider'/>", unsafe_allow_html=True)

    # Step 0
    if st.session_state.onboard_step == 0:
        st.markdown(f"<div style='color:{TEXT};font-size:15px;font-weight:600;margin-bottom:20px;'>Select your data sources</div>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, src in enumerate(DATA_SOURCES):
            with cols[i % 3]:
                selected = src["id"] in st.session_state.selected_sources
                border_color = GOLD if selected else BORDER
                bg_color = f"rgba(212,168,67,0.07)" if selected else CARD
                st.markdown(f"""
                <div style="background:{bg_color};border:1.5px solid {border_color};
                            border-radius:12px;padding:20px;margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
                        <div style="background:rgba(212,168,67,0.15);border:1px solid rgba(212,168,67,0.3);
                                    border-radius:7px;padding:6px 10px;font-family:'Cinzel',serif;
                                    font-size:11px;color:{GOLD};font-weight:700;">{src["icon"]}</div>
                        {"<div style='color:" + TEAL + ";font-size:16px;font-weight:700;'>&#10003;</div>" if selected else ""}
                    </div>
                    <div style="font-weight:700;color:{TEXT};font-size:14px;margin-bottom:10px;">{src["label"]}</div>
                    <div style="display:flex;flex-wrap:wrap;gap:5px;">
                        {"".join([f'<span class="badge-neutral">{f}</span>' for f in src["fields"]])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                toggle_label = "Selected" if selected else "Select"
                if st.button(toggle_label, key=f"src_{src['id']}"):
                    if selected:
                        st.session_state.selected_sources.remove(src["id"])
                    else:
                        st.session_state.selected_sources.append(src["id"])
                    st.rerun()

        if st.session_state.selected_sources:
            st.markdown(f"<div style='color:{TEAL};font-size:13px;margin-top:8px;'>{len(st.session_state.selected_sources)} source(s) selected</div>", unsafe_allow_html=True)
            if st.button(f"Continue with {len(st.session_state.selected_sources)} source(s)"):
                st.session_state.onboard_step = 1
                st.rerun()

    # Step 1
    elif st.session_state.onboard_step == 1:
        st.markdown(f"<div style='color:{TEXT};font-size:15px;font-weight:600;margin-bottom:20px;'>Map identity fields to Numad Universal Schema</div>", unsafe_allow_html=True)
        mapping_rows = [
            ("customer_email",  "email_hash",    "SHA256_EMAIL",   "Deterministic"),
            ("mobile_number",   "phone_hash",    "SHA256_PHONE",   "Deterministic"),
            ("user_id",         "brand_id",      "BRAND_NS",       "Deterministic"),
            ("device_uuid",     "device_id",     "IDFA_GAID",      "Probabilistic"),
            ("loyalty_card_no", "loyalty_id",    "LOYALTY_NS",     "Deterministic"),
        ]
        header_cols = st.columns([2, 0.5, 2, 2, 1.5])
        for col, h in zip(header_cols, ["Your Field", "", "Numad Field", "ID Namespace", "Link Type"]):
            col.markdown(f"<div style='color:{MUTED};font-size:11px;font-weight:700;letter-spacing:1px;padding-bottom:10px;border-bottom:1px solid {BORDER};'>{h}</div>", unsafe_allow_html=True)
        for your, numad, ns, ltype in mapping_rows:
            row = st.columns([2, 0.5, 2, 2, 1.5])
            row[0].markdown(f"<code>{your}</code>", unsafe_allow_html=True)
            row[1].markdown(f"<div style='color:{GOLD};font-size:20px;text-align:center;padding-top:4px;'>&#8594;</div>", unsafe_allow_html=True)
            row[2].markdown(f"<div style='color:{TEAL};font-weight:600;font-size:13px;padding-top:6px;'>{numad}</div>", unsafe_allow_html=True)
            row[3].markdown(f"<code>{ns}</code>", unsafe_allow_html=True)
            row[4].markdown(f"<span class='{'badge-teal' if ltype == 'Deterministic' else 'badge-neutral'}'>{ltype}</span>", unsafe_allow_html=True)
            st.markdown(f"<div style='height:1px;background:{BORDER};margin:4px 0'/>", unsafe_allow_html=True)

        c1, c2, _ = st.columns([1, 1, 3])
        with c1:
            if st.button("Back"):
                st.session_state.onboard_step = 0
                st.rerun()
        with c2:
            if st.button("Confirm Mapping"):
                st.session_state.onboard_step = 2
                st.rerun()

    # Step 2
    elif st.session_state.onboard_step == 2:
        st.markdown(f"<div style='color:{TEXT};font-size:15px;font-weight:600;margin-bottom:20px;'>Privacy & Compliance Configuration</div>", unsafe_allow_html=True)
        privacy_items = [
            ("Differential Privacy",      "Adds calibrated noise to query results, preventing reverse-engineering of individual records.",         "PDPL Required",   True),
            ("Aggregation Threshold",     "Minimum cohort size (default: 50) before segment data is surfaced to any partner.",                    "Default: 50",     True),
            ("Hashing Protocol",          "SHA-256 with HMAC salt applied to all PII fields before entering the Snowflake clean room.",           "SHA-256 + HMAC",  True),
            ("Saudi PDPL Compliance",     "Full alignment with the Saudi Personal Data Protection Law (PDPL) and SDAIA framework.",               "Certified",       True),
            ("Data Residency — KSA",      "All compute and storage within Saudi Arabia. Snowflake me-central-1 (Riyadh) + AWS me-south-1.",      "KSA Local",       True),
            ("Purpose Limitation",        "Data usage is contractually restricted to the declared activation purposes only.",                      "Enforced",        True),
        ]
        col1, col2 = st.columns(2)
        for i, (title, desc, badge, enabled) in enumerate(privacy_items):
            target = col1 if i % 2 == 0 else col2
            with target:
                st.markdown(f"""
                <div class="numad-card-teal" style="margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                        <div style="font-weight:700;color:{TEXT};font-size:14px;">{title}</div>
                        <span class="badge-teal">{badge}</span>
                    </div>
                    <div style="color:{MUTED};font-size:12px;line-height:1.6;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"<div style='height:8px'/>", unsafe_allow_html=True)
        c1, c2, _ = st.columns([1, 1.5, 3])
        with c1:
            if st.button("Back "):
                st.session_state.onboard_step = 1
                st.rerun()
        with c2:
            if st.button("Start Ingestion"):
                st.session_state.onboard_step = 3
                st.rerun()

    # Step 3 — Ingestion
    elif st.session_state.onboard_step == 3:
        if not st.session_state.ingestion_done:
            st.markdown(f"<div style='text-align:center;padding:20px 0;'>", unsafe_allow_html=True)
            st.markdown(f"<div style='color:{TEXT};font-family:Cinzel,serif;font-size:22px;font-weight:700;text-align:center;margin-bottom:8px;'>Ingesting & Resolving Identities</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='color:{MUTED};font-size:13px;text-align:center;margin-bottom:32px;'>Snowflake native pipeline running inside your clean room</div>", unsafe_allow_html=True)

            pipeline_tasks = [
                "SHA-256 hashing applied to all PII fields",
                "Identity spine building in Snowflake DCR",
                "Cross-device graph stitching",
                "Audience segmentation complete",
                "Graph ready for activation",
            ]
            progress_bar = st.progress(0)
            status_placeholder = st.empty()
            for i, task in enumerate(pipeline_tasks):
                time.sleep(0.5)
                pct = int((i + 1) / len(pipeline_tasks) * 100)
                progress_bar.progress(pct)
                status_placeholder.markdown(f"<div style='color:{TEAL};font-size:13px;text-align:center;'>{task}...</div>", unsafe_allow_html=True)
            st.session_state.ingestion_done = True
            st.rerun()
        else:
            st.markdown(f"""
            <div style="text-align:center;padding:32px 0;">
                <div style="width:72px;height:72px;border-radius:50%;background:rgba(27,191,166,0.15);
                            border:2px solid {TEAL};margin:0 auto 24px;display:flex;align-items:center;
                            justify-content:center;font-size:32px;color:{TEAL};">&#10003;</div>
                <div style="font-family:'Cinzel',serif;color:{TEAL};font-size:24px;font-weight:700;margin-bottom:8px;">Identity Graph Ready</div>
                <div style="color:{MUTED};font-size:14px;max-width:480px;margin:0 auto 32px;">
                    Your data has been ingested, resolved, and graphed inside the Numad clean room on Snowflake.
                </div>
            </div>
            """, unsafe_allow_html=True)

            m1, m2, m3, m4 = st.columns(4)
            for col, (val, label) in zip([m1, m2, m3, m4], [
                ("4.2M", "IDs Onboarded"), ("3.96M", "Resolved IDs"), ("94.2%", "Match Rate"), ("12", "Segments Created")
            ]):
                col.markdown(f"<div class='metric-card' style='text-align:center;'><div class='metric-value'>{val}</div><div class='metric-label'>{label}</div></div>", unsafe_allow_html=True)

            st.markdown("<div style='height:20px'/>", unsafe_allow_html=True)
            c1, c2, _ = st.columns([1.2, 1.2, 2])
            with c1:
                if st.button("View Identity Graph"):
                    st.session_state.page = "Identity Graph"
                    st.rerun()
            with c2:
                if st.button("Activate Audiences"):
                    st.session_state.page = "Activation Hub"
                    st.rerun()


# ─── PAGE: IDENTITY GRAPH ─────────────────────────────────────────────────────
elif st.session_state.page == "Identity Graph":
    st.markdown(f"""
    <div class="numad-label">NUMAD GRAPH ENGINE v3.2 — SNOWFLAKE NATIVE</div>
    <div class="numad-title">Identity Graph</div>
    <div class="numad-subtitle">Cross-device, cross-channel identity resolution for the Saudi market</div>
    """, unsafe_allow_html=True)

    left, right = st.columns([3, 2])

    with left:
        # Network graph with plotly
        node_x = [0.5,  0.15, 0.85, 0.05, 0.30, 0.65, 0.92, 0.5]
        node_y = [0.85, 0.60, 0.60, 0.30, 0.25, 0.25, 0.30, 0.50]
        node_labels = ["Email Hash", "Phone Hash", "Device ID", "CRM ID", "Loyalty ID", "Cookie", "IDFA", "Person"]
        node_colors = [GOLD, GOLD, GOLD, TEAL, TEAL, TEAL, TEAL, "#FFFFFF"]
        node_sizes  = [18, 16, 16, 14, 14, 14, 14, 28]

        edges = [(0,7),(1,7),(2,7),(3,1),(4,1),(5,2),(6,2)]
        edge_x, edge_y = [], []
        for a, b in edges:
            edge_x += [node_x[a], node_x[b], None]
            edge_y += [node_y[a], node_y[b], None]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines",
                                  line=dict(color=f"rgba(27,191,166,0.35)", width=1.5),
                                  hoverinfo="none"))
        fig.add_trace(go.Scatter(x=node_x, y=node_y, mode="markers+text",
                                  marker=dict(size=node_sizes, color=node_colors,
                                              line=dict(color=BORDER, width=1.5)),
                                  text=node_labels,
                                  textposition=["top center"]*7 + ["middle center"],
                                  textfont=dict(color=TEXT, size=11, family="DM Sans"),
                                  hoverinfo="text"))
        fig.update_layout(
            paper_bgcolor=CARD, plot_bgcolor=CARD,
            margin=dict(l=20, r=20, t=20, b=20),
            height=380,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown(f"""
        <div class="numad-card">
            <div style="color:{MUTED};font-size:11px;letter-spacing:2px;font-weight:700;margin-bottom:18px;">GRAPH STATISTICS</div>
            <table class="numad-table">
                <tr><td style="color:{MUTED};">Total Identities</td><td style="color:{GOLD};font-weight:700;font-family:'Cinzel',serif;text-align:right;">4.2M</td></tr>
                <tr><td style="color:{MUTED};">Resolved Persons</td><td style="color:{TEAL};font-weight:700;font-family:'Cinzel',serif;text-align:right;">3.96M</td></tr>
                <tr><td style="color:{MUTED};">Avg IDs / Person</td><td style="color:{TEXT};font-weight:700;text-align:right;">3.7</td></tr>
                <tr><td style="color:{MUTED};">Deterministic Links</td><td style="color:{GOLD};font-weight:700;text-align:right;">94.2%</td></tr>
                <tr><td style="color:{MUTED};">Probabilistic Links</td><td style="color:{MUTED};font-weight:700;text-align:right;">5.8%</td></tr>
                <tr><td style="color:{MUTED};">Cross-Device Match</td><td style="color:{TEXT};font-weight:700;text-align:right;">81.4%</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        # Signal breakdown bar
        signals = [("Email", 78, GOLD), ("Mobile", 64, TEAL), ("Device ID", 52, "#A78BFA"), ("Loyalty Card", 41, "#60A5FA")]
        st.markdown(f"<div style='color:{MUTED};font-size:11px;letter-spacing:2px;font-weight:700;margin:16px 0 12px;'>ID SIGNAL COVERAGE</div>", unsafe_allow_html=True)
        for label, pct, color in signals:
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="font-size:12px;color:{MUTED};">{label}</span>
                    <span style="font-size:12px;color:{color};font-weight:700;">{pct}%</span>
                </div>
                <div class="progress-wrap">
                    <div style="height:100%;width:{pct}%;background:{color};border-radius:4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='numad-divider'/>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:{TEXT};font-size:14px;font-weight:700;letter-spacing:0.5px;margin-bottom:16px;'>RESOLVED AUDIENCE SEGMENTS — Ready for Activation</div>", unsafe_allow_html=True)

    seg_cols = st.columns(4)
    for i, seg in enumerate(SEGMENTS):
        with seg_cols[i % 4]:
            st.markdown(f"""
            <div style="background:{CARD};border:1px solid {BORDER};border-radius:10px;
                        padding:16px;margin-bottom:12px;border-left:3px solid {seg['color']};">
                <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                    <div style="font-size:12px;font-weight:700;color:{TEXT};">{seg['name']}</div>
                    <div style="background:rgba(255,255,255,0.06);border-radius:4px;padding:2px 6px;
                                font-size:10px;color:{seg['color']};font-weight:700;">{seg['iScore']}</div>
                </div>
                <div style="font-family:'Cinzel',serif;font-size:22px;color:{seg['color']};font-weight:700;">{seg['size']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Activate", key=f"act_seg_{i}"):
                st.session_state.page = "Activation Hub"
                st.rerun()


# ─── PAGE: ACTIVATION HUB ─────────────────────────────────────────────────────
elif st.session_state.page == "Activation Hub":
    st.markdown(f"""
    <div class="numad-label">PRIVACY-SAFE AUDIENCE ACTIVATION</div>
    <div class="numad-title">Activation Hub</div>
    <div class="numad-subtitle">Push resolved audiences to retail media networks and ad tech platforms across the Middle East — no raw data leaves the clean room.</div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Retail Media Networks", "DSP & Ad Tech Platforms"])

    with tab1:
        st.markdown(f"<div style='color:{MUTED};font-size:12px;margin-bottom:16px;'>Select RMN partners to activate your matched audiences. All activation via Snowflake DCR — zero raw data exposure.</div>", unsafe_allow_html=True)
        for p in RMN_PARTNERS:
            is_active = p["name"] in st.session_state.active_dests
            bg = f"rgba(212,168,67,0.06)" if is_active else CARD
            border = f"rgba(212,168,67,0.5)" if is_active else BORDER
            cols = st.columns([0.4, 3, 2, 2, 1])
            with cols[0]:
                st.markdown(f"<div style='width:12px;height:12px;border-radius:50%;background:{p['color']};margin-top:14px;margin-left:4px;'></div>", unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"""
                <div style="padding:10px 0;">
                    <div style="font-weight:700;color:{TEXT};font-size:14px;">{p['name']}</div>
                    <div style="color:{MUTED};font-size:12px;">{p['desc']}</div>
                </div>""", unsafe_allow_html=True)
            with cols[2]:
                st.markdown(f"<div style='color:{MUTED};font-size:12px;padding-top:12px;'>{p['reach']}</div>", unsafe_allow_html=True)
            with cols[3]:
                st.markdown(f"<div style='padding-top:12px;'><span class='badge-teal'>DCR-Ready</span> <span class='badge-neutral'>{p['format']}</span></div>", unsafe_allow_html=True)
            with cols[4]:
                label = "Selected" if is_active else "Select"
                if st.button(label, key=f"rmn_{p['name']}"):
                    if is_active:
                        st.session_state.active_dests.remove(p["name"])
                    else:
                        st.session_state.active_dests.append(p["name"])
                    st.rerun()
            st.markdown(f"<div style='height:1px;background:{BORDER};'/>", unsafe_allow_html=True)

    with tab2:
        st.markdown(f"<div style='color:{MUTED};font-size:12px;margin-bottom:16px;'>Activate matched audiences to programmatic and social platforms. Signals transmitted via hashed match keys — no PII transfer.</div>", unsafe_allow_html=True)
        for p in ADTECH_PARTNERS:
            is_active = p["name"] in st.session_state.active_dests
            cols = st.columns([0.4, 3, 2, 2, 1])
            with cols[0]:
                st.markdown(f"<div style='width:12px;height:12px;border-radius:50%;background:{p['color']};margin-top:14px;margin-left:4px;'></div>", unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"""
                <div style="padding:10px 0;">
                    <div style="font-weight:700;color:{TEXT};font-size:14px;">{p['name']}</div>
                    <div style="color:{MUTED};font-size:12px;">{p['desc']}</div>
                </div>""", unsafe_allow_html=True)
            with cols[2]:
                st.markdown(f"<div style='color:{MUTED};font-size:12px;padding-top:12px;'>{p['reach']}</div>", unsafe_allow_html=True)
            with cols[3]:
                st.markdown(f"<div style='padding-top:12px;'><span class='badge-neutral'>{p['type']}</span> <span class='badge-teal'>{p['signal']}</span></div>", unsafe_allow_html=True)
            with cols[4]:
                label = "Selected" if is_active else "Select"
                if st.button(label, key=f"dsp_{p['name']}"):
                    if is_active:
                        st.session_state.active_dests.remove(p["name"])
                    else:
                        st.session_state.active_dests.append(p["name"])
                    st.rerun()
            st.markdown(f"<div style='height:1px;background:{BORDER};'/>", unsafe_allow_html=True)

    if st.session_state.active_dests:
        st.markdown("<div class='numad-divider'/>", unsafe_allow_html=True)
        dest_count = len(st.session_state.active_dests)
        c_left, c_right = st.columns([3, 1])
        with c_left:
            st.markdown(f"""
            <div class="numad-card-gold">
                <div style="font-weight:700;color:{TEXT};font-size:16px;margin-bottom:6px;">
                    {dest_count} destination{"s" if dest_count > 1 else ""} selected for activation
                </div>
                <div style="color:{MUTED};font-size:13px;margin-bottom:16px;">
                    Hashed audiences will be pushed via Snowflake clean room — zero raw data exposure to any partner.
                </div>
                <div style="display:flex;flex-wrap:wrap;gap:8px;">
                    {"".join([f'<span class="badge-gold">{d}</span>' for d in st.session_state.active_dests])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c_right:
            if st.button("Launch Activation"):
                st.success(f"Activation launched to {dest_count} destination(s) via Snowflake DCR.")


# ─── PAGE: INTELLIGENCE ───────────────────────────────────────────────────────
elif st.session_state.page == "Intelligence":
    st.markdown(f"""
    <div class="numad-label">CLOSED-LOOP MEASUREMENT</div>
    <div class="numad-title">Audience Intelligence</div>
    <div class="numad-subtitle">Incrementality reporting and campaign measurement — computed inside Snowflake, no raw data shared with measurement partners.</div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    for col, (val, label, sub, color) in zip([m1,m2,m3,m4], [
        ("8.9M",  "Total Reach",              "+14.2% vs prior",  GOLD),
        ("142K",  "Matched Conversions",      "+28.4% vs prior",  TEAL),
        ("4.8x",  "Incremental ROAS",         "+0.6x vs prior",   "#A78BFA"),
        ("SAR 14.2M", "Incremental Revenue",  "Attribution: 84%", "#F472B6"),
    ]):
        col.markdown(f"""
        <div class="metric-card" style="border-top:2px solid {color};">
            <div class="metric-label">{label}</div>
            <div style="font-family:'Cinzel',serif;font-size:26px;color:{color};font-weight:700;">{val}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='numad-divider'/>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown(f"<div style='color:{TEXT};font-size:14px;font-weight:700;margin-bottom:16px;letter-spacing:0.5px;'>PERFORMANCE BY CHANNEL</div>", unsafe_allow_html=True)
        channel_data = [
            ("STC Ads",          "7.1x", 7.1, "#7B2D8B", "1.2M"),
            ("Noon RMN",         "6.2x", 6.2, "#FFC200", "2.1M"),
            ("Snapchat KSA",     "5.8x", 5.8, "#FFDD00", "3.4M"),
            ("Google DV360",     "4.4x", 4.4, "#4285F4", "4.2M"),
            ("Meta MENA",        "3.9x", 3.9, "#0668E1", "5.1M"),
        ]
        for name, roas_str, roas_num, color, reach in channel_data:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:14px;padding:11px 0;border-bottom:1px solid {BORDER};">
                <div style="width:10px;height:10px;border-radius:50%;background:{color};flex-shrink:0;"></div>
                <div style="flex:1;font-size:13px;color:{TEXT};">{name}</div>
                <div style="font-size:12px;color:{MUTED};">{reach}</div>
                <div style="font-family:'Cinzel',serif;font-size:16px;color:{color};font-weight:700;min-width:44px;text-align:right;">{roas_str}</div>
            </div>
            """, unsafe_allow_html=True)

        # ROAS bar chart
        fig_roas = go.Figure(go.Bar(
            x=[r[1] for r in channel_data],
            y=[r[0] for r in channel_data],
            orientation="h",
            marker=dict(color=[r[3] for r in channel_data], opacity=0.85),
            text=[r[1] for r in channel_data],
            textposition="outside",
            textfont=dict(color=TEXT, size=11),
        ))
        fig_roas.update_layout(
            paper_bgcolor=CARD, plot_bgcolor=CARD,
            margin=dict(l=10, r=40, t=16, b=10),
            height=200,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, color=MUTED),
            yaxis=dict(showgrid=False, zeroline=False, color=TEXT, tickfont=dict(size=11)),
            showlegend=False,
        )
        st.plotly_chart(fig_roas, use_container_width=True)

    with right:
        st.markdown(f"<div style='color:{TEXT};font-size:14px;font-weight:700;margin-bottom:16px;letter-spacing:0.5px;'>INCREMENTALITY MEASUREMENT</div>", unsafe_allow_html=True)
        incr_rows = [
            ("Incremental Conversions", "38,420",    "84.7% of total conversions"),
            ("Incremental Revenue",     "SAR 14.2M", "Attributed to Numad activation"),
            ("True Lift",               "+22.4%",    "vs holdout group"),
            ("Break-even ROAS",         "1.4x",      "vs actual 4.8x"),
            ("iROAS",                   "4.1x",      "Incremental return on ad spend"),
        ]
        for label, value, note in incr_rows:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:flex-start;
                        padding:12px 0;border-bottom:1px solid {BORDER};">
                <div>
                    <div style="font-size:13px;color:{MUTED};">{label}</div>
                    <div style="font-size:11px;color:{BORDER};margin-top:2px;">{note}</div>
                </div>
                <div style="font-family:'Cinzel',serif;font-size:18px;color:{TEAL};font-weight:700;">{value}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:20px;background:rgba(27,191,166,0.08);border:1px solid rgba(27,191,166,0.25);
                    border-radius:10px;padding:14px 18px;font-size:12px;color:{TEAL};line-height:1.6;">
            Measurement computed inside Snowflake Data Clean Room. No raw conversion data is shared with any measurement partner.
            Holdout testing uses randomised control group assignment at the ID level.
        </div>
        """, unsafe_allow_html=True)


# ─── PAGE: TECH SPEC ──────────────────────────────────────────────────────────
elif st.session_state.page == "Tech Specification":
    st.markdown(f"""
    <div class="numad-label">SNOWFLAKE DCR COLLABORATION SPEC</div>
    <div class="numad-title">Technical Specification</div>
    <div class="numad-subtitle">Snowflake Data Clean Room YAML spec and integration architecture for Numad Identity Cloud</div>
    """, unsafe_allow_html=True)

    tab_arch, tab_yaml, tab_api = st.tabs(["Architecture", "DCR Collaboration YAML", "API Reference"])

    with tab_arch:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="numad-card-gold">
                <div style="color:{GOLD};font-size:11px;letter-spacing:2px;font-weight:700;margin-bottom:16px;">DATA LAYER — SNOWFLAKE</div>
                <table class="numad-table">
                    <tr><th>Component</th><th>Detail</th></tr>
                    <tr><td>Clean Room Type</td><td>Snowflake Native DCR</td></tr>
                    <tr><td>Region</td><td>AWS me-central-1 (Riyadh)</td></tr>
                    <tr><td>Hashing</td><td>SHA-256 + HMAC-SHA256</td></tr>
                    <tr><td>Privacy</td><td>Differential Privacy (&#949;=1.0)</td></tr>
                    <tr><td>Threshold</td><td>Aggregation k≥50</td></tr>
                    <tr><td>Compliance</td><td>Saudi PDPL / SDAIA</td></tr>
                    <tr><td>Data Residency</td><td>KSA local, no cross-border</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="numad-card-teal">
                <div style="color:{TEAL};font-size:11px;letter-spacing:2px;font-weight:700;margin-bottom:16px;">IDENTITY NAMESPACES SUPPORTED</div>
                <table class="numad-table">
                    <tr><th>Namespace</th><th>Type</th><th>Coverage</th></tr>
                    <tr><td>SHA256_EMAIL</td><td>Deterministic</td><td>78%</td></tr>
                    <tr><td>SHA256_PHONE</td><td>Deterministic</td><td>64%</td></tr>
                    <tr><td>BRAND_NS</td><td>Deterministic</td><td>100%</td></tr>
                    <tr><td>IDFA_GAID</td><td>Probabilistic</td><td>52%</td></tr>
                    <tr><td>LOYALTY_NS</td><td>Deterministic</td><td>41%</td></tr>
                    <tr><td>UID2</td><td>Deterministic</td><td>35%</td></tr>
                    <tr><td>MAID</td><td>Probabilistic</td><td>48%</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:16px;background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:24px 28px;">
            <div style="color:{TEXT};font-size:14px;font-weight:700;margin-bottom:16px;letter-spacing:0.5px;">END-TO-END DATA FLOW</div>
            <div style="display:flex;align-items:center;gap:0;overflow-x:auto;">
                {"".join([f'''
                <div style="flex:1;text-align:center;padding:14px 8px;background:{SURFACE};border:1px solid {BORDER};
                            border-radius:8px;min-width:110px;">
                    <div style="font-size:11px;color:{GOLD};font-weight:700;margin-bottom:6px;">{num}</div>
                    <div style="font-size:12px;color:{TEXT};font-weight:600;">{step}</div>
                    <div style="font-size:10px;color:{MUTED};margin-top:4px;">{sub}</div>
                </div>
                {"<div style='color:" + GOLD + ";font-size:20px;padding:0 4px;flex-shrink:0;'>&#8594;</div>" if idx < 5 else ""}
                ''' for idx, (num, step, sub) in enumerate([
                    ("01", "Ingest", "Raw 1P data"),
                    ("02", "Normalise", "Schema map"),
                    ("03", "Hash", "SHA-256 PII"),
                    ("04", "Graph", "ID resolution"),
                    ("05", "Enrich", "Segmentation"),
                    ("06", "Activate", "DCR push"),
                ])])}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab_yaml:
        dcr_yaml = """# Numad.AI — Snowflake Data Clean Room Collaboration Spec
# Version: 2.4 | Region: AWS me-central-1 (Riyadh) | PDPL Compliant

collaboration:
  name: numad_identity_cloud_collab
  version: "2.4"
  region: aws_me_central_1
  compliance:
    - saudi_pdpl
    - sdaia_framework
  data_residency: ksa_only

participants:
  provider:
    name: numad_ai
    role: identity_graph_provider
    account: NUMAD_SNOWFLAKE_ACCOUNT
  consumer:
    name: brand_partner
    role: advertiser
    account: "{{ BRAND_SNOWFLAKE_ACCOUNT }}"

identity_resolution:
  namespaces:
    - id: SHA256_EMAIL
      type: deterministic
      match_key: hashed_email
    - id: SHA256_PHONE
      type: deterministic
      match_key: hashed_phone
    - id: BRAND_NS
      type: deterministic
      match_key: brand_customer_id
    - id: IDFA_GAID
      type: probabilistic
      match_key: mobile_advertising_id
    - id: LOYALTY_NS
      type: deterministic
      match_key: loyalty_member_id

privacy_controls:
  differential_privacy:
    enabled: true
    epsilon: 1.0
    delta: 1e-7
    mechanism: gaussian_noise
  aggregation_threshold:
    minimum_group_size: 50
    apply_to: all_queries
  hashing:
    algorithm: sha256
    salt: hmac_sha256
    apply_to:
      - email
      - phone
      - national_id_hash
  purpose_limitation:
    allowed_purposes:
      - audience_matching
      - measurement
      - lookalike_modelling
    enforce: true

templates:
  - name: audience_overlap
    description: Measure overlap between brand CRM and Numad graph
    input_tables:
      brand: brand_hashed_customers
      numad: numad_resolved_persons
    output:
      - overlap_count
      - overlap_pct
      - segment_distribution
    privacy: aggregated_only

  - name: campaign_attribution
    description: Match post-campaign conversions to exposed impressions
    input_tables:
      brand: brand_conversions_hashed
      numad: numad_impression_log
    output:
      - matched_conversions
      - attributed_revenue_sar
      - roas
      - iroas
    privacy: aggregated_only

  - name: incrementality_measurement
    description: Holdout-based true lift measurement
    input_tables:
      brand: brand_purchase_events
      numad: numad_holdout_assignment
    output:
      - treatment_group_cvr
      - control_group_cvr
      - true_lift_pct
      - confidence_interval
    privacy: differential_privacy

  - name: lookalike_expansion
    description: Build lookalike audiences from seed segment
    input_tables:
      brand: brand_seed_segment
      numad: numad_feature_store
    output:
      - lookalike_audience_ids
      - similarity_scores
      - reach_estimate
    privacy: k_anonymity_50

activation:
  endpoints:
    rmn:
      - noon_rmn
      - carrefour_arabia
      - lulu_hypermarket
      - panda_retail
    dsp:
      - google_dv360
      - meta_business
      - snapchat_ksa
      - tiktok_for_business
      - amazon_dsp
      - the_trade_desk
      - stc_ads
  transfer_method: hashed_match_keys_only
  raw_data_exposure: false
  audit_log: enabled
"""
        st.code(dcr_yaml, language="yaml")
        st.download_button(
            label="Download DCR Spec",
            data=dcr_yaml,
            file_name="numad_dcr_collaboration_spec.yaml",
            mime="text/yaml",
        )

    with tab_api:
        st.markdown(f"""
        <div class="numad-card">
            <div style="color:{GOLD};font-size:11px;letter-spacing:2px;font-weight:700;margin-bottom:16px;">REST API ENDPOINTS</div>
            <table class="numad-table">
                <tr><th>Method</th><th>Endpoint</th><th>Description</th></tr>
                <tr><td><span class="badge-teal">POST</span></td><td><code>/v1/onboard/initiate</code></td><td style="color:{MUTED};">Initiate data onboarding job</td></tr>
                <tr><td><span class="badge-teal">POST</span></td><td><code>/v1/onboard/schema-map</code></td><td style="color:{MUTED};">Submit field mapping configuration</td></tr>
                <tr><td><span class="badge-gold">GET</span></td><td><code>/v1/graph/stats</code></td><td style="color:{MUTED};">Retrieve identity graph statistics</td></tr>
                <tr><td><span class="badge-gold">GET</span></td><td><code>/v1/graph/segments</code></td><td style="color:{MUTED};">List resolved audience segments</td></tr>
                <tr><td><span class="badge-teal">POST</span></td><td><code>/v1/activate</code></td><td style="color:{MUTED};">Push audience to destination</td></tr>
                <tr><td><span class="badge-gold">GET</span></td><td><code>/v1/measure/roas</code></td><td style="color:{MUTED};">Retrieve closed-loop ROAS report</td></tr>
                <tr><td><span class="badge-gold">GET</span></td><td><code>/v1/measure/incrementality</code></td><td style="color:{MUTED};">Get incrementality measurement</td></tr>
                <tr><td><span class="badge-teal">POST</span></td><td><code>/v1/dcr/run-template</code></td><td style="color:{MUTED};">Execute a DCR analysis template</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="numad-card" style="margin-top:16px;">
            <div style="color:{TEAL};font-size:11px;letter-spacing:2px;font-weight:700;margin-bottom:12px;">AUTHENTICATION</div>
            <div style="color:{MUTED};font-size:13px;line-height:1.7;">
                All API calls require a Bearer token obtained via <code>/v1/auth/token</code>.<br>
                Snowflake account credentials are passed as a Snowflake OAuth token in the <code>X-Snowflake-Token</code> header.<br>
                IP allowlisting required for production; contact <span style="color:{TEAL};">onboarding@numad.ai</span> to register your IP range.
            </div>
        </div>
        """, unsafe_allow_html=True)
