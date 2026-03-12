"""
Numad.AI — Identity Intelligence Cloud
Streamlit in Snowflake · v4
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(
    page_title="Numad.AI — Identity Intelligence Cloud",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Colours ───────────────────────────────────────────────────────────────────
CYAN      = "#29d4f5"
PURPLE    = "#7c3aed"
PURPLE_LT = "#a855f7"
GREEN     = "#10d9a0"
PINK      = "#f472b6"
GOLD      = "#f0c040"
ORANGE    = "#fb923c"
BG        = "#1a0a3c"
BG_DEEP   = "#120728"
SURFACE   = "#1e0d42"
CARD      = "#251050"
BORDER    = "#3d1f7a"
MUTED     = "#8b7ab8"
WHITE     = "#ffffff"

SF_SVG = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none"><line x1="12" y1="2" x2="12" y2="22" stroke="#29B5E8" stroke-width="2" stroke-linecap="round"/><line x1="2" y1="12" x2="22" y2="12" stroke="#29B5E8" stroke-width="2" stroke-linecap="round"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07" stroke="#29B5E8" stroke-width="2" stroke-linecap="round"/><line x1="19.07" y1="4.93" x2="4.93" y2="19.07" stroke="#29B5E8" stroke-width="2" stroke-linecap="round"/></svg>'

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif !important;
    background-color: {BG} !important;
    color: #e8e0ff !important;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 0.5rem !important; padding-bottom: 2rem !important; max-width: 1400px; }}

/* Metrics */
[data-testid="metric-container"] {{
    background: {CARD}; border: 1.5px solid {BORDER};
    border-radius: 12px; padding: 16px 18px;
}}
[data-testid="metric-container"] label {{
    color: {MUTED} !important; font-size: 11px !important; font-weight: 600 !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    color: {CYAN} !important; font-size: 26px !important; font-weight: 800 !important;
}}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {{ color: {GREEN} !important; }}

/* Hide ALL default button borders/outlines and reset to transparent */
.stButton > button {{
    border-radius: 9px !important; font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 12px !important;
    transition: opacity 0.15s !important; white-space: nowrap !important;
}}
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, {PURPLE}, {CYAN}) !important;
    color: white !important; border: none !important; padding: 10px 24px !important;
}}
.stButton > button[kind="secondary"] {{
    background: transparent !important; color: {MUTED} !important;
    border: 1px solid {BORDER} !important; padding: 7px 14px !important;
}}
.stButton > button[kind="secondary"]:hover {{
    color: {WHITE} !important; border-color: {CYAN}88 !important;
}}

/* Nav pill buttons — applied via class on the nav container divs */
div[data-nav="active"] .stButton > button {{
    background: {CYAN}18 !important; color: {CYAN} !important;
    border: 1.5px solid {CYAN}60 !important; font-weight: 800 !important;
}}
div[data-nav="inactive"] .stButton > button {{
    background: transparent !important; color: {MUTED} !important;
    border: 1px solid {BORDER} !important;
}}

/* Tabs */
[data-testid="stTabs"] [role="tablist"] {{ border-bottom: 1px solid {BORDER}; }}
[data-testid="stTabs"] button {{
    color: {MUTED} !important; font-weight: 600 !important; font-size: 13px !important;
    border-radius: 0 !important; padding: 8px 20px !important;
    background: transparent !important; border: none !important;
    border-bottom: 2px solid transparent !important; white-space: nowrap !important;
}}
[data-testid="stTabs"] button[aria-selected="true"] {{
    color: {CYAN} !important; border-bottom: 2px solid {CYAN} !important;
}}

/* Multiselect */
[data-testid="stMultiSelect"] > div > div {{
    background: {CARD} !important; border-color: {BORDER} !important;
}}
[data-baseweb="tag"] {{ background: {PURPLE}40 !important; color: {CYAN} !important; }}

/* Dataframe */
[data-testid="stDataFrame"] {{ border-radius: 10px; overflow: hidden; }}
[data-testid="stDataFrame"] th {{
    background: {SURFACE} !important; color: {MUTED} !important;
    font-size: 11px !important; font-weight: 700 !important; letter-spacing: 0.5px;
}}
[data-testid="stDataFrame"] td {{
    background: {CARD} !important; color: #e8e0ff !important; font-size: 12px !important;
}}

/* Progress */
[data-testid="stProgress"] > div > div {{
    background: linear-gradient(90deg, {PURPLE}, {PURPLE_LT}) !important;
}}

hr {{ border-color: {BORDER} !important; margin: 6px 0 !important; }}
code {{ color: {CYAN} !important; background: {CYAN}18 !important; border-radius: 4px; padding: 2px 6px; }}
pre {{ background: {BG_DEEP} !important; border: 1px solid {BORDER} !important; border-radius: 10px !important; padding: 20px !important; }}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
DEFAULTS = dict(
    screen="landing",       # landing | journey | app
    page="overview",
    native_sel=[], of_sel=[],
    ingest_done=False, graph_done=False,
    act_partners=[], act_launched=False,
)
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def goto(screen=None, page=None):
    if screen: st.session_state.screen = screen
    if page:   st.session_state.page   = page
    st.rerun()

# ── Static data ───────────────────────────────────────────────────────────────
NATIVE_SOURCES = [
    ("CRM", "Customer Database",   "Email, Phone, Customer ID"),
    ("APP", "Mobile Application",  "IDFA/GAID, Email, User ID"),
    ("CDP", "CDP Export",          "Universal ID, Segment, Score"),
    ("LYL", "Loyalty Programme",   "Member ID, Email, Mobile"),
    ("POS", "Point of Sale",       "Transaction ID, Phone, Card Hash"),
    ("WEB", "E-commerce Platform", "Session ID, Email, Device"),
]
SF_OBJECTS = [
    ("BRAND_IDS_EXT",   "EXTERNAL TABLE",  "Queryable layer over staged hashed files"),
    ("NUMAD_STAGE",     "INTERNAL STAGE",  "Landing zone for hashed PII before graph ingest"),
    ("OVERLAP_VIEW",    "SECURE VIEW",     "Matched IDs only — no access to raw tables"),
    ("MATCH_FN",        "SECURE FUNCTION", "Identity resolution logic, executes in your VPC"),
    ("OVERLAP_RESULTS", "SECURE VIEW",     "Aggregated outputs with k≥50 enforced"),
    ("AUDIENCE_SHARE",  "DATA SHARE",      "Cross-account delivery to activation partners"),
]
OF_CONNECTORS = [
    ("Salesforce CRM",         "CRM",      "Contact ID, Lead Email, Account ID"),
    ("Shopify",                "Commerce", "Customer Email, Order ID, Device ID"),
    ("Adobe Experience Cloud", "CDP",      "ECID, Email, Segment ID"),
    ("Segment (Twilio)",        "CDP",      "Anonymous ID, User ID, Email"),
    ("Braze",                  "CRM",      "External ID, Email, Push Token"),
    ("SAP Commerce Cloud",     "Commerce", "Business Partner, Email, Order Ref"),
    ("mParticle",              "CDP",      "MPID, Email, IDFA/GAID"),
    ("HubSpot (beta)",         "CRM",      "Contact ID, Email, Company ID"),
]
SEGMENTS = [
    ("High-Value Shoppers",   "22K", "82K",  "+273%"),
    ("Grocery Loyalists",     "64K", "210K", "+228%"),
    ("Electronics Intenders", "18K", "54K",  "+200%"),
    ("Ramadan Buyers",        "90K", "340K", "+278%"),
    ("Auto In-Market",        "9K",  "28K",  "+211%"),
    ("Vision 2030 Consumers", "38K", "130K", "+242%"),
]
RMN_PARTNERS = [
    ("Noon",             "3.2M users",     "Sponsored, Display"),
    ("Carrefour Arabia", "1.8M members",   "In-store + Digital"),
    ("LuLu Hypermarket", "1.4M customers", "Display, Sponsored"),
    ("Panda Retail",     "2.1M members",   "Offsite + Onsite"),
    ("Jarir Bookstore",  "820K members",   "Display, Email"),
    ("Danube Home",      "640K shoppers",  "Sponsored, CTV"),
]
DSP_PARTNERS = [
    ("Google DV360",        "18M+ MENA",    "Customer Match",   "DSP"),
    ("Meta Business",       "16M+ MENA",    "Custom Audience",  "Social"),
    ("Snapchat",            "21M KSA",      "Snap Audience",    "Social"),
    ("TikTok for Business", "12M MENA",     "Custom Audience",  "Social"),
    ("Amazon DSP",          "4M+ KSA",      "Amazon Audiences", "DSP"),
    ("The Trade Desk",      "Open web",     "UID 2.0",          "DSP"),
    ("STC Ads",             "18M KSA subs", "Mobile Identity",  "Telco"),
]
ROAS_CH = [
    ("STC Ads",      6.1, PURPLE_LT),
    ("Noon RMN",     5.4, GOLD),
    ("Snapchat KSA", 4.8, "#FFDD00"),
    ("Google DV360", 3.9, "#4285F4"),
    ("Meta MENA",    3.2, "#0668E1"),
]
GRAPH_TASKS = [
    "SHA-256 hashing all PII fields",
    "Uploading hashed IDs to Snowflake",
    "Matching against Numad identity graph",
    "Cross-device resolution pass",
    "Linking partner clean room signals",
    "Computing overlap and expansion metrics",
]
COLLAB_YAML = """\
# Numad.AI — Snowflake Secure Data Collaboration Spec v2.4
# Region: AWS me-central-1 | Saudi PDPL Compliant

collaboration:
  name: numad_identity_cloud
  version: "2.4"
  region: aws_me_central_1
  compliance: [saudi_pdpl, sdaia_framework]
  data_residency: ksa_only

identity_resolution:
  namespaces:
    - { id: SHA256_EMAIL,  type: deterministic }
    - { id: SHA256_PHONE,  type: deterministic }
    - { id: BRAND_NS,      type: deterministic }
    - { id: IDFA_GAID,     type: probabilistic }
    - { id: LOYALTY_NS,    type: deterministic }
    - { id: UID2,          type: deterministic }

open_flow:
  connectors: [salesforce, shopify, adobe_ec, segment,
               braze, sap_commerce, mparticle, hubspot]
  auth: oauth2
  sync_mode: incremental
  hash_on_ingest: true

privacy_controls:
  differential_privacy:
    enabled: true
    epsilon: 1.0
    mechanism: gaussian_noise
  aggregation_threshold:
    minimum_group_size: 50
  hashing: { algorithm: sha256, salt: hmac_sha256 }
  purpose_limitation:
    allowed_purposes: [ingest, graph, activation, measurement]
    enforce: true

activation:
  transfer_method: hashed_match_keys_only
  raw_data_exposure: false
  audit_log: enabled
"""

ECOSYSTEM = [
    ("Brand / Advertiser",   CYAN,      "Onboard 1P data, activate audiences"),
    ("Retailer / RMN",       PURPLE_LT, "Monetise shopper data with brands"),
    ("Agency",               PINK,      "Unified identity across clients"),
    ("Data Partner",         GOLD,      "Connect ID graph to the ecosystem"),
    ("Measurement Partner",  GREEN,     "Closed-loop attribution in DCR"),
    ("Telco / Gov / Media",  ORANGE,    "Sovereign first-party signals"),
]

JOURNEY_STEPS = [
    ("ingest",   "01", "Ingest Data",        CYAN,
     "Connect your first-party data via native Snowflake objects or Open Flow connectors. PII is hashed before anything enters Snowflake."),
    ("graph",    "02", "Create Graph",        PURPLE_LT,
     "Match and enrich your IDs against the Numad identity graph. Discover overlap, expansion potential, and new signals."),
    ("activate", "03", "Activate Audiences",  PINK,
     "Push enriched, privacy-safe audiences to retail media networks and DSP partners via Snowflake Data Share."),
    ("measure",  "04", "Measure Campaigns",   GREEN,
     "Run closed-loop attribution and true lift studies inside Snowflake. No raw data shared with any partner."),
]

# ── Shared UI ─────────────────────────────────────────────────────────────────

def logo_bar(show_nav=False):
    st.markdown(f"""
    <div style="background:{BG_DEEP};border-bottom:1px solid {BORDER};padding:0 28px;
         display:flex;align-items:center;justify-content:space-between;
         height:54px;position:relative;margin-bottom:0;">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;
           background:linear-gradient(90deg,{PURPLE},{CYAN},{PURPLE});"></div>
      <div style="display:flex;align-items:center;gap:10px;">
        <div style="width:36px;height:36px;background:linear-gradient(135deg,{PURPLE},{CYAN});
             border-radius:10px;display:flex;align-items:center;justify-content:center;
             box-shadow:0 0 18px {CYAN}40;">
          <span style="font-size:16px;font-weight:900;color:white;">N</span>
        </div>
        <div>
          <div style="font-size:14px;font-weight:900;color:white;letter-spacing:1.2px;line-height:1.1;">
            NUMAD<span style="color:{CYAN};">.AI</span></div>
          <div style="font-size:7.5px;color:{MUTED};letter-spacing:1.8px;font-weight:600;margin-top:1px;">
            IDENTITY INTELLIGENCE CLOUD</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:6px;background:#29B5E812;
           border:1px solid #29B5E830;border-radius:7px;padding:5px 12px;">
        {SF_SVG}
        <span style="font-size:9px;font-weight:800;color:#29B5E8;letter-spacing:0.8px;white-space:nowrap;">
          POWERED BY SNOWFLAKE</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


def nav_bar():
    """Horizontal nav using st.columns + buttons. Active page gets cyan border."""
    NAV = [
        ("overview",  "Overview"),
        ("ingest",    "01 · Ingest"),
        ("graph",     "02 · Graph"),
        ("activate",  "03 · Activate"),
        ("measure",   "04 · Measure"),
        ("techspec",  "Spec"),
    ]
    cols = st.columns(len(NAV))
    for col, (pid, label) in zip(cols, NAV):
        with col:
            active = st.session_state.page == pid
            # Inject per-button style via markdown trick
            if active:
                st.markdown(f"""
                <style>
                div[data-testid="column"]:has(button[kind]) button[aria-label="{label}"] {{
                    background: {CYAN}18 !important;
                    color: {CYAN} !important;
                    border: 1.5px solid {CYAN}80 !important;
                }}
                </style>
                """, unsafe_allow_html=True)
            btn_type = "primary" if active else "secondary"
            if st.button(label, key=f"nav_{pid}", type=btn_type, use_container_width=True):
                st.session_state.page = pid
                st.rerun()
    st.markdown("<hr>", unsafe_allow_html=True)


def back_btn(label, target):
    if st.button(f"← {label}", key=f"back_{target}_{st.session_state.page}", type="secondary"):
        st.session_state.page = target
        st.rerun()


def step_header(step, title, sub=""):
    st.markdown(f"""
    <div style="margin-bottom:20px;">
      <div style="color:{CYAN};font-size:10px;letter-spacing:3px;font-weight:700;margin-bottom:6px;">{step}</div>
      <div style="font-size:26px;font-weight:900;color:{WHITE};margin-bottom:6px;letter-spacing:-0.5px;">{title}</div>
      {"<div style='color:"+MUTED+";font-size:12px;line-height:1.65;max-width:760px;'>"+sub+"</div>" if sub else ""}
    </div>
    """, unsafe_allow_html=True)


def callout(text, color=GREEN, icon="🛡️"):
    st.markdown(f"""
    <div style="background:{color}10;border:1px solid {color}30;border-radius:9px;
         padding:10px 14px;margin:10px 0;font-size:11px;color:{color};
         display:flex;gap:8px;">
      {"<span>"+icon+"</span>" if icon else ""}<span>{text}</span>
    </div>
    """, unsafe_allow_html=True)


def stat_tile_row(tiles):
    cols = st.columns(len(tiles))
    for col, (v, l, n, c) in zip(cols, tiles):
        with col:
            st.markdown(f"""
            <div style="background:{SURFACE};border-radius:9px;padding:12px 10px;text-align:center;margin-top:10px;">
              <div style="font-size:20px;font-weight:900;color:{c};line-height:1;">{v}</div>
              <div style="font-size:10px;color:{MUTED};margin-top:4px;">{l}</div>
              {"<div style='font-size:9px;color:"+BORDER+";margin-top:2px;'>"+n+"</div>" if n else ""}
            </div>
            """, unsafe_allow_html=True)


def label(text, color=MUTED):
    st.markdown(f"<div style='color:{color};font-size:9px;letter-spacing:2px;font-weight:700;margin-bottom:6px;'>{text}</div>", unsafe_allow_html=True)


# ── Charts ────────────────────────────────────────────────────────────────────

def chart_roas_bars(height=220):
    fig = go.Figure(go.Bar(
        x=[r[1] for r in ROAS_CH], y=[r[0] for r in ROAS_CH], orientation="h",
        marker_color=[r[2] for r in ROAS_CH],
        text=[f"{r[1]}x" for r in ROAS_CH], textposition="outside",
        textfont=dict(color=WHITE, size=12),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color=WHITE, margin=dict(l=10, r=60, t=10, b=10), height=height,
        xaxis=dict(visible=False), yaxis=dict(tickfont=dict(color=MUTED, size=11)),
        showlegend=False,
    )
    return fig


def chart_roas_trend(height=160):
    fig = go.Figure(go.Scatter(
        x=["Wk 1","Wk 2","Wk 3","Wk 4","Wk 5","Wk 6"],
        y=[2.4, 2.7, 3.1, 3.4, 3.2, 3.8],
        mode="lines+markers",
        line=dict(color=CYAN, width=2.5), marker=dict(color=CYAN, size=7),
        fill="tozeroy", fillcolor="rgba(41,212,245,0.1)",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color=WHITE, margin=dict(l=10, r=10, t=10, b=10), height=height,
        xaxis=dict(tickfont=dict(color=MUTED, size=10), gridcolor=BORDER),
        yaxis=dict(tickfont=dict(color=MUTED, size=10), gridcolor=BORDER),
        showlegend=False,
    )
    return fig


def chart_venn():
    fig = go.Figure()
    fig.add_shape(type="circle", x0=0.04, y0=0.08, x1=0.64, y1=0.92,
                  fillcolor="rgba(124,58,237,0.22)", line_color=PURPLE_LT, line_width=1.5, line_dash="dot")
    fig.add_shape(type="circle", x0=0.36, y0=0.08, x1=0.96, y1=0.92,
                  fillcolor="rgba(41,212,245,0.18)", line_color=CYAN, line_width=1.5)
    fig.add_shape(type="circle", x0=0.32, y0=0.14, x1=0.68, y1=0.86,
                  fillcolor="rgba(16,217,160,0.22)", line_color="rgba(0,0,0,0)")
    for x, y, txt, color, size in [
        (0.22, 0.72, "<b>YOUR IDs</b>",    PURPLE_LT, 11),
        (0.22, 0.59, "82K",                MUTED,     10),
        (0.78, 0.72, "<b>NUMAD GRAPH</b>", CYAN,      11),
        (0.78, 0.57, "820K+",              MUTED,     10),
        (0.50, 0.65, "<b>87%</b>",         WHITE,     15),
        (0.50, 0.50, "MATCH",              GREEN,     11),
    ]:
        fig.add_annotation(x=x, y=y, text=txt, showarrow=False, font=dict(color=color, size=size))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10), height=200,
        xaxis=dict(visible=False, range=[0,1]), yaxis=dict(visible=False, range=[0,1]),
        showlegend=False,
    )
    return fig


def chart_signals():
    labels = ["Email coverage", "Mobile coverage", "Cross-device", "Loyalty ID"]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Before", x=[74,48,0,0], y=labels, orientation="h",
                         marker_color="rgba(61,31,122,0.55)", width=0.38))
    fig.add_trace(go.Bar(name="After",  x=[89,71,74,61], y=labels, orientation="h",
                         marker_color=CYAN, width=0.38))
    fig.update_layout(
        barmode="overlay",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color=WHITE, margin=dict(l=10, r=30, t=10, b=10), height=210,
        legend=dict(font=dict(size=10, color=MUTED), orientation="h", y=-0.2),
        xaxis=dict(range=[0,105], ticksuffix="%", tickfont=dict(color=MUTED, size=10), gridcolor=BORDER),
        yaxis=dict(tickfont=dict(color=MUTED, size=11)),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# SCREENS
# ══════════════════════════════════════════════════════════════════════════════

def screen_landing():
    logo_bar()
    st.markdown(f"""
    <div style="background:radial-gradient(ellipse at 50% 60%,{PURPLE}35,transparent 70%),
                {BG_DEEP};padding:72px 0 56px;text-align:center;margin-bottom:0;">
      <div style="color:{CYAN};font-size:10px;letter-spacing:5px;font-weight:700;margin-bottom:20px;">
        // POWERING MENA'S DATA ECONOMY
      </div>
      <div style="font-size:58px;font-weight:900;line-height:0.93;margin-bottom:20px;letter-spacing:-2px;">
        <div style="color:{WHITE};">SOVEREIGN</div>
        <div style="background:linear-gradient(90deg,{CYAN},#7de8ff);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;">DATA &amp; AI</div>
      </div>
      <div style="color:{MUTED};font-size:14px;line-height:1.8;max-width:480px;margin:0 auto 36px;">
        Secure data collaboration connecting brands, retailers, agencies, and telcos —
        without exposing raw data.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # GET STARTED button centred
    col = st.columns([3, 2, 3])[1]
    with col:
        if st.button("▶  GET STARTED", type="primary", use_container_width=True):
            goto("journey")

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center;margin-bottom:20px;">
      <div style="color:{CYAN};font-size:10px;letter-spacing:4px;font-weight:700;margin-bottom:8px;">
        BUILT FOR EVERY PLAYER IN THE ECOSYSTEM
      </div>
      <div style="color:{MUTED};font-size:13px;">
        One secure data collaboration infrastructure — every party keeps their raw data.
      </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, (label_txt, color, note) in enumerate(ECOSYSTEM):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:{CARD};border:1.5px solid {BORDER};border-top:2px solid {color}80;
                 border-radius:14px;padding:18px 20px;margin-bottom:12px;position:relative;overflow:hidden;">
              <div style="font-size:12px;font-weight:800;color:{color};margin-bottom:6px;">{label_txt}</div>
              <div style="font-size:11px;color:{MUTED};line-height:1.6;">{note}</div>
            </div>
            """, unsafe_allow_html=True)


def screen_journey():
    logo_bar()
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Back to home
    if st.button("← Back to home", type="secondary"):
        goto("landing")

    st.markdown(f"""
    <div style="text-align:center;margin:20px 0 36px;">
      <div style="color:{CYAN};font-size:10px;letter-spacing:4px;font-weight:700;margin-bottom:10px;">
        YOUR DATA COLLABORATION JOURNEY
      </div>
      <div style="font-size:32px;font-weight:900;color:{WHITE};letter-spacing:-0.8px;margin-bottom:10px;">
        Four steps to campaign measurement
      </div>
      <div style="color:{MUTED};font-size:13px;max-width:520px;margin:0 auto;line-height:1.7;">
        Ingest your data, build your identity graph, activate enriched audiences,
        and measure true campaign lift — all inside Snowflake.
      </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    for col, (pid, num, title, color, desc) in zip(cols, JOURNEY_STEPS):
        with col:
            st.markdown(f"""
            <div style="background:{CARD};border:1.5px solid {BORDER};border-top:3px solid {color};
                 border-radius:16px;padding:22px 18px;min-height:210px;">
              <div style="font-size:10px;color:{color}80;font-weight:900;letter-spacing:2px;margin-bottom:10px;">{num}</div>
              <div style="font-size:15px;font-weight:900;color:{WHITE};margin-bottom:8px;">{title}</div>
              <div style="font-size:11px;color:{MUTED};line-height:1.65;margin-bottom:16px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Begin →", key=f"journey_{pid}", type="primary", use_container_width=True):
                st.session_state.page = pid
                goto("app")


# ══════════════════════════════════════════════════════════════════════════════
# APP PAGES
# ══════════════════════════════════════════════════════════════════════════════

def page_overview():
    step_header(
        "IDENTITY INTELLIGENCE CLOUD", "Sovereign Data & AI",
        "Privacy-preserving identity resolution and audience activation — powered by Snowflake secure data collaboration.",
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Resolved IDs",      "820K", "In Numad graph")
    with c2: st.metric("Match Rate",         "87%",  "Deterministic links")
    with c3: st.metric("Avg ROAS",           "3.4x", "Across KSA RMNs")
    with c4: st.metric("Time to Activation", "<72h", "From ingest to live")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    lc, rc = st.columns(2)
    with lc:
        label("ROAS BY CHANNEL")
        st.plotly_chart(chart_roas_bars(), use_container_width=True, config={"displayModeBar":False})
    with rc:
        label("6-WEEK ROAS TREND")
        st.plotly_chart(chart_roas_trend(), use_container_width=True, config={"displayModeBar":False})

    st.markdown(f"<div style='font-size:16px;font-weight:800;color:{WHITE};margin:8px 0 12px;'>Start your journey</div>", unsafe_allow_html=True)
    steps = [
        ("ingest",   "01 · Ingest Data",       CYAN,      "Connect 1P data via native Snowflake objects or Open Flow connectors."),
        ("graph",    "02 · Create Graph",       PURPLE_LT, "Match and enrich IDs against the Numad identity graph."),
        ("activate", "03 · Activate",           PINK,      "Push enriched audiences to RMNs and DSP partners."),
        ("measure",  "04 · Measure",            GREEN,     "Closed-loop attribution inside Snowflake. No raw data shared."),
    ]
    cols = st.columns(4)
    for col, (pid, title, color, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div style="background:{CARD};border:1.5px solid {BORDER};border-top:3px solid {color};
                 border-radius:12px;padding:16px 14px;min-height:120px;margin-bottom:8px;">
              <div style="font-size:12px;font-weight:800;color:{color};margin-bottom:8px;">{title}</div>
              <div style="font-size:11px;color:{MUTED};line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open →", key=f"ov_{pid}", use_container_width=True, type="secondary"):
                st.session_state.page = pid
                st.rerun()


def page_ingest():
    back_btn("Back to Overview", "overview")
    step_header("STEP 1 OF 4", "Ingest Data",
        "Choose how to bring your first-party data into Snowflake. Use native objects for file/export uploads, "
        "Open Flow connectors for direct platform sync — or both.")

    left, right = st.columns(2)
    with left:
        st.markdown(f"""
        <div style="background:{CARD};border:1.5px solid {BORDER};border-radius:14px;
             padding:14px 16px;margin-bottom:10px;">
          <div style="display:flex;align-items:center;gap:9px;margin-bottom:4px;">
            <div style="width:28px;height:28px;background:#29B5E818;border:1px solid #29B5E835;
                 border-radius:8px;display:flex;align-items:center;justify-content:center;
                 flex-shrink:0;">{SF_SVG}</div>
            <b style="color:{WHITE};font-size:13px;">Native Snowflake Objects</b>
          </div>
          <div style="color:{MUTED};font-size:11px;">Upload files or exports — Numad stages and hashes in your account</div>
        </div>
        """, unsafe_allow_html=True)

        label("SELECT YOUR DATA TYPES")
        native_opts = [f"{tag} — {lbl}" for tag, lbl, _ in NATIVE_SOURCES]
        sel_native = st.multiselect("Data types", native_opts,
                                    default=st.session_state.native_sel,
                                    label_visibility="collapsed", key="ms_native")
        st.session_state.native_sel = sel_native
        if sel_native:
            matched = [s for s in NATIVE_SOURCES if f"{s[0]} — {s[1]}" in sel_native]
            st.dataframe(pd.DataFrame([{"Tag":s[0],"Source":s[1],"Fields":s[2]} for s in matched]),
                         hide_index=True, use_container_width=True)

        label("SNOWFLAKE OBJECTS IN YOUR ACCOUNT", MUTED)
        st.dataframe(pd.DataFrame([{"Object":n,"Type":t,"Description":d} for n,t,d in SF_OBJECTS]),
                     hide_index=True, use_container_width=True)
        callout("<b style='color:#f0c040;'>SHA-256 + HMAC-SHA256</b> runs in your environment before upload. Numad never sees raw PII.", GOLD, "🔐")

    with right:
        st.markdown(f"""
        <div style="background:{CARD};border:1.5px solid {PURPLE_LT}40;border-radius:14px;
             padding:14px 16px;margin-bottom:10px;">
          <div style="display:flex;align-items:center;gap:9px;margin-bottom:4px;">
            <div style="width:28px;height:28px;background:{PURPLE_LT}18;
                 border:1px solid {PURPLE_LT}35;border-radius:8px;
                 display:flex;align-items:center;justify-content:center;
                 flex-shrink:0;font-size:14px;">🔗</div>
            <b style="color:{WHITE};font-size:13px;">Open Flow Connectors</b>
          </div>
          <div style="color:{MUTED};font-size:11px;">OAuth-authenticated sync — no manual exports required</div>
        </div>
        """, unsafe_allow_html=True)

        label("SELECT CONNECTORS TO AUTHENTICATE")
        of_opts = [n for n,_,_ in OF_CONNECTORS]
        sel_of = st.multiselect("Connectors", of_opts,
                                default=st.session_state.of_sel,
                                label_visibility="collapsed", key="ms_of")
        st.session_state.of_sel = sel_of
        if sel_of:
            matched_of = [(n,cat,ids) for n,cat,ids in OF_CONNECTORS if n in sel_of]
            st.dataframe(pd.DataFrame([{"Connector":n,"Category":cat,"Identity Fields":ids}
                                        for n,cat,ids in matched_of]),
                         hide_index=True, use_container_width=True)
            callout("✓ OAuth handshake completes at ingestion — syncs directly into Snowflake", PURPLE_LT, "")
        callout("Saudi PDPL & SDAIA compliant — purpose limitation enforced at the Snowflake object level for both paths", GREEN, "🛡️")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    total = len(sel_native) + len(sel_of)
    if not st.session_state.ingest_done:
        if total > 0:
            if st.button(f"Ingest {total} source{'s' if total>1 else ''} →", type="primary"):
                st.session_state.ingest_done = True
                st.rerun()
        else:
            st.info("Select at least one data type or connector above to begin.")
    else:
        parts = []
        if sel_native: parts.append(f"{len(sel_native)} native source{'s' if len(sel_native)>1 else ''}")
        if sel_of:     parts.append(f"{len(sel_of)} connector{'s' if len(sel_of)>1 else ''}")
        st.success(f"✅ Ingestion staged — {' · '.join(parts)}")
        if st.button("Create Graph →", type="primary"):
            st.session_state.page = "graph"; st.rerun()


def page_graph():
    back_btn("Back to Ingest Data", "ingest")
    step_header("STEP 2 OF 4", "Create Graph",
        "Match your hashed IDs against the Numad identity graph. "
        "Matched IDs get enriched with new signals; additional reachable profiles are unlocked "
        "via household and device graph links.")

    if not st.session_state.graph_done:
        c1, c2 = st.columns(2)
        with c1:
            label("READY TO GRAPH", CYAN)
            n_src = max(len(st.session_state.native_sel)+len(st.session_state.of_sel), 1)
            for val, lbl in [("82K","Your ingested IDs"),(str(n_src),"Sources selected"),("3","Signal types (before)")]:
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid {BORDER};">
                  <span style="font-size:12px;color:{MUTED};">{lbl}</span>
                  <span style="font-size:14px;color:{CYAN};font-weight:800;">{val}</span>
                </div>
                """, unsafe_allow_html=True)
        with c2:
            label("GRAPH OBJECTS TO BE CREATED")
            st.dataframe(pd.DataFrame([{"Object":n,"Type":t,"Description":d} for n,t,d in SF_OBJECTS[2:]]),
                         hide_index=True, use_container_width=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("▶  Run Identity Graph", type="primary"):
            prog = st.progress(0, text="Starting...")
            for i, task in enumerate(GRAPH_TASKS):
                time.sleep(0.5)
                prog.progress((i+1)/len(GRAPH_TASKS), text=f"✦ {task}")
            time.sleep(0.3); prog.empty()
            st.session_state.graph_done = True; st.rerun()
    else:
        st.success("✅ Graph complete — identity graph built")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("IDs Matched", "71K", "87% of your 82K IDs")
        with c2: st.metric("Match Rate",  "87%", "Deterministic + probabilistic")
        with c3: st.metric("New Reach",   "66K", "Via household & device links")

        callout("87% of your 82K IDs were matched. Matched profiles enriched with new signals. "
                "<b>66K additional profiles</b> reachable via household and device links. "
                "Total addressable: <b>137K</b> (+67%).", GREEN, "")

        r1, r2 = st.columns(2)
        with r1:
            label("OVERLAP DIAGRAM")
            st.plotly_chart(chart_venn(), use_container_width=True, config={"displayModeBar":False})
            stat_tile_row([
                ("82K","Your IDs","ingested",PURPLE_LT),
                ("71K","Matched in graph","87% of yours",GREEN),
                ("66K","New reach","via graph links",CYAN),
            ])
            st.markdown(f"""
            <div style="background:{GREEN}08;border:1px solid {GREEN}22;border-radius:8px;
                 padding:10px 14px;display:flex;justify-content:space-between;align-items:center;margin-top:10px;">
              <span style="font-size:12px;color:{MUTED};">Total addressable after enrichment</span>
              <span style="font-size:18px;font-weight:900;color:{GREEN};">137K
                <span style="font-size:11px;font-weight:600;">(+67%)</span></span>
            </div>
            """, unsafe_allow_html=True)
        with r2:
            label("SIGNAL COVERAGE (matched IDs)")
            st.plotly_chart(chart_signals(), use_container_width=True, config={"displayModeBar":False})

        label("SEGMENT EXPANSION")
        st.dataframe(pd.DataFrame([{"Segment":n,"Before":b,"After (enriched)":a,"Lift":lift}
                                    for n,b,a,lift in SEGMENTS]),
                     hide_index=True, use_container_width=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("⚡  Activate Audiences →", type="primary"):
            st.session_state.page = "activate"; st.rerun()


def page_activate():
    back_btn("Back to Create Graph", "graph")
    step_header("STEP 3 OF 4", "Activate Audiences",
        "Push privacy-safe hashed audiences to your selected partners — all match keys via Snowflake Data Share, "
        "zero raw data exposure.")
    callout("✅  137K enriched profiles ready  ·  71K matched + 66K new reach  ·  87% match rate", CYAN, "")

    if not st.session_state.act_launched:
        tab_rmn, tab_dsp = st.tabs(["Retail Media Networks", "DSP & Ad Tech"])
        with tab_rmn:
            st.dataframe(pd.DataFrame([{"Partner":n,"Reach":r,"Formats":fmt} for n,r,fmt in RMN_PARTNERS]),
                         hide_index=True, use_container_width=True)
            rmn_opts = [n for n,_,_ in RMN_PARTNERS]
            sel_rmn = st.multiselect("Select RMN partners", rmn_opts,
                                     default=[p for p in st.session_state.act_partners if p in rmn_opts],
                                     key="ms_rmn")
        with tab_dsp:
            st.dataframe(pd.DataFrame([{"Partner":n,"Reach":r,"Signal":sig,"Type":t}
                                        for n,r,sig,t in DSP_PARTNERS]),
                         hide_index=True, use_container_width=True)
            dsp_opts = [n for n,_,_,_ in DSP_PARTNERS]
            sel_dsp = st.multiselect("Select DSP partners", dsp_opts,
                                     default=[p for p in st.session_state.act_partners if p in dsp_opts],
                                     key="ms_dsp")

        all_sel = sel_rmn + sel_dsp
        st.session_state.act_partners = all_sel
        if all_sel:
            st.markdown(f"<div style='margin:8px 0;font-size:12px;color:{WHITE};font-weight:600;'>{len(all_sel)} partner(s) selected: {', '.join(all_sel)}</div>", unsafe_allow_html=True)
            st.caption("Hashed match keys only — delivered via Snowflake Data Share")
            if st.button(f"⚡  Launch Activation to {len(all_sel)} partner(s)", type="primary"):
                st.session_state.act_launched = True; st.rerun()
        else:
            st.info("Select at least one partner above to activate.")
    else:
        st.success(f"✅ Activation launched — 137K hashed profiles sent to **{', '.join(st.session_state.act_partners)}** via Snowflake.\n\nAudiences available within 2–4 hours.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Add more partners", type="secondary"):
                st.session_state.act_launched = False; st.rerun()
        with c2:
            if st.button("📊  Measure Campaigns →", type="primary"):
                st.session_state.page = "measure"; st.rerun()


def page_measure():
    back_btn("Back to Activate Audiences", "activate")
    step_header("STEP 4 OF 4", "Measure Campaigns",
        "Closed-loop attribution and true lift measurement — all computed inside Snowflake, "
        "no raw data shared with any partner.")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Total Reach",         "1.4M",     "+11.2% vs prior")
    with c2: st.metric("Matched Conversions", "28K",      "+19.4% vs prior")
    with c3: st.metric("Incremental ROAS",    "3.8x",     "+0.4x vs prior")
    with c4: st.metric("Incremental Revenue", "SAR 2.2M", "Attribution: 81%")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    lc, rc = st.columns(2)
    with lc:
        label("ROAS BY ACTIVATION CHANNEL")
        st.plotly_chart(chart_roas_bars(), use_container_width=True, config={"displayModeBar":False})
        label("6-WEEK ROAS TREND")
        st.plotly_chart(chart_roas_trend(), use_container_width=True, config={"displayModeBar":False})
    with rc:
        label("INCREMENTALITY MEASUREMENT")
        st.dataframe(pd.DataFrame([
            ("Incremental Conversions","7,840",   "81.2% of total"),
            ("Incremental Revenue",   "SAR 2.2M","Attributed to Numad"),
            ("True Lift",             "+18.2%",  "vs holdout group"),
            ("iROAS",                 "2.9x",    "Incremental return"),
            ("Holdout Group Size",     "18.8%",   "of total audience"),
        ], columns=["Metric","Value","Note"]), hide_index=True, use_container_width=True)
        callout("🔒 Computed inside Snowflake. No raw conversion data shared with any partner.", CYAN, "")


def page_techspec():
    step_header("SNOWFLAKE SECURE DATA COLLABORATION SPEC", "Technical Specification")
    tab_arch, tab_yaml, tab_api = st.tabs(["Architecture","Collaboration YAML","API Reference"])
    with tab_arch:
        c1, c2 = st.columns(2)
        with c1:
            label("SECURE DATA COLLABORATION CONFIG", CYAN)
            st.dataframe(pd.DataFrame([
                ("Type",      "Snowflake Secure Data Collaboration"),
                ("Region",    "AWS me-central-1 (KSA)"),
                ("Hashing",   "SHA-256 + HMAC-SHA256 (client-side)"),
                ("Privacy",   "Differential Privacy (ε=1.0)"),
                ("Threshold", "Aggregation k≥50"),
                ("Compliance","Saudi PDPL / SDAIA"),
                ("Residency", "KSA — no cross-border transfer"),
                ("Open Flow", "OAuth2, incremental sync, 8 connectors"),
            ], columns=["Property","Value"]), hide_index=True, use_container_width=True)
        with c2:
            label("IDENTITY NAMESPACES", PURPLE_LT)
            st.dataframe(pd.DataFrame([
                ("SHA256_EMAIL","Deterministic","74%"),
                ("SHA256_PHONE","Deterministic","61%"),
                ("BRAND_NS",   "Deterministic","100%"),
                ("IDFA_GAID",  "Probabilistic","48%"),
                ("LOYALTY_NS", "Deterministic","38%"),
                ("UID2",       "Deterministic","22%"),
                ("MAID",       "Probabilistic","41%"),
            ], columns=["Namespace","Type","Coverage"]), hide_index=True, use_container_width=True)
    with tab_yaml:
        st.code(COLLAB_YAML, language="yaml")
        st.download_button("⬇  Download YAML", COLLAB_YAML,
                           file_name="numad_collab_spec.yaml", mime="text/yaml")
    with tab_api:
        st.dataframe(pd.DataFrame([
            ("POST","/v1/ingest/initiate",         "Stage hashed IDs into Snowflake"),
            ("POST","/v1/ingest/open-flow/connect","Authenticate an Open Flow connector"),
            ("GET", "/v1/ingest/status",           "Check ingestion job status"),
            ("POST","/v1/graph/run",               "Run identity graph matching"),
            ("GET", "/v1/graph/results",           "Overlap stats and segment expansion"),
            ("POST","/v1/activate",                "Push audience to partner destination"),
            ("GET", "/v1/measure/roas",            "Closed-loop ROAS by channel"),
            ("GET", "/v1/measure/lift",            "True lift and incrementality report"),
        ], columns=["Method","Endpoint","Description"]), hide_index=True, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════

screen = st.session_state.screen

if screen == "landing":
    screen_landing()

elif screen == "journey":
    screen_journey()

else:  # "app"
    logo_bar()
    # Home button inline with nav
    hcol, ncol = st.columns([1, 8])
    with hcol:
        if st.button("⌂ Home", type="secondary", use_container_width=True):
            goto("landing")
    with ncol:
        NAV = [
            ("overview",  "Overview"),
            ("ingest",    "01 · Ingest"),
            ("graph",     "02 · Graph"),
            ("activate",  "03 · Activate"),
            ("measure",   "04 · Measure"),
            ("techspec",  "Spec"),
        ]
        cols = st.columns(len(NAV))
        for col, (pid, lbl) in zip(cols, NAV):
            with col:
                t = "primary" if st.session_state.page == pid else "secondary"
                if st.button(lbl, key=f"nav_{pid}", type=t, use_container_width=True):
                    st.session_state.page = pid
                    st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    {
        "overview": page_overview,
        "ingest":   page_ingest,
        "graph":    page_graph,
        "activate": page_activate,
        "measure":  page_measure,
        "techspec": page_techspec,
    }.get(st.session_state.page, page_overview)()
