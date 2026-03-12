"""
Numad.AI — Identity Intelligence Cloud
Streamlit in Snowflake app
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Numad.AI — Identity Intelligence Cloud",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Brand colours ─────────────────────────────────────────────────────────────
CYAN    = "#29d4f5"
PURPLE  = "#7c3aed"
PURPLE_LT = "#a855f7"
GREEN   = "#10d9a0"
PINK    = "#f472b6"
GOLD    = "#f0c040"
ORANGE  = "#fb923c"
BG      = "#1a0a3c"
CARD    = "#251050"
MUTED   = "#8b7ab8"

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #1a0a3c;
    color: #e8e0ff;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* Metric cards */
[data-testid="metric-container"] {
    background: #251050;
    border: 1.5px solid #3d1f7a;
    border-radius: 12px;
    padding: 16px;
}
[data-testid="metric-container"] label { color: #8b7ab8 !important; font-size: 12px !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #29d4f5 !important; font-size: 28px !important; font-weight: 800 !important; }
[data-testid="metric-container"] [data-testid="stMetricDelta"] { color: #10d9a0 !important; }

/* Tabs */
[data-testid="stTabs"] button {
    color: #8b7ab8 !important;
    font-weight: 600;
    font-size: 13px;
    border-radius: 0 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #29d4f5 !important;
    border-bottom: 2px solid #29d4f5 !important;
    background: transparent !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #29d4f5);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    font-size: 14px;
    padding: 10px 28px;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #6d28d9, #06b6d4);
    border: none;
    color: white;
}

/* Dataframes */
[data-testid="stDataFrame"] { border-radius: 10px; }

/* Selectbox, multiselect */
[data-testid="stMultiSelect"] > div,
[data-testid="stSelectbox"] > div > div {
    background: #251050 !important;
    border-color: #3d1f7a !important;
    color: #e8e0ff !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #120728;
    border-right: 1px solid #3d1f7a;
}

/* Dividers */
hr { border-color: #3d1f7a; }

/* Code blocks */
code { color: #29d4f5; background: #29d4f520; border-radius: 4px; padding: 2px 6px; }
pre { background: #120728 !important; border: 1px solid #3d1f7a !important; border-radius: 10px !important; }

/* Info / success / warning boxes */
.stAlert { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


# ── Session state defaults ────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "overview",
        "native_sources": [],
        "of_connectors": [],
        "ingest_done": False,
        "graph_run": False,
        "graph_complete": False,
        "activated_partners": [],
        "activation_launched": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── Data ──────────────────────────────────────────────────────────────────────
NATIVE_SOURCES = [
    {"id": "crm",    "tag": "CRM", "label": "Customer Database",   "fields": "Email, Phone, Customer ID"},
    {"id": "app",    "tag": "APP", "label": "Mobile Application",  "fields": "IDFA/GAID, Email, User ID"},
    {"id": "cdp",    "tag": "CDP", "label": "CDP Export",          "fields": "Universal ID, Segment, Score"},
    {"id": "loyalty","tag": "LYL", "label": "Loyalty Programme",   "fields": "Member ID, Email, Mobile"},
    {"id": "pos",    "tag": "POS", "label": "Point of Sale",       "fields": "Transaction ID, Phone, Card Hash"},
    {"id": "ecomm",  "tag": "WEB", "label": "E-commerce Platform", "fields": "Session ID, Email, Device"},
]

SF_OBJECTS = [
    {"name": "BRAND_IDS_EXT",   "type": "EXTERNAL TABLE",  "desc": "Queryable layer over your staged hashed files"},
    {"name": "NUMAD_STAGE",     "type": "INTERNAL STAGE",  "desc": "Landing zone for hashed PII before graph ingest"},
    {"name": "OVERLAP_VIEW",    "type": "SECURE VIEW",     "desc": "Matched IDs only — no access to raw tables"},
    {"name": "MATCH_FN",        "type": "SECURE FUNCTION", "desc": "Identity resolution logic, executes in your VPC"},
    {"name": "OVERLAP_RESULTS", "type": "SECURE VIEW",     "desc": "Aggregated outputs with k≥50 enforced"},
    {"name": "AUDIENCE_SHARE",  "type": "DATA SHARE",      "desc": "Cross-account delivery to activation partners"},
]

OF_CONNECTORS = [
    {"id": "sf",      "name": "Salesforce CRM",         "cat": "CRM",      "ids": "Contact ID, Lead Email, Account ID"},
    {"id": "shopify", "name": "Shopify",                "cat": "Commerce", "ids": "Customer Email, Order ID, Device ID"},
    {"id": "adobe",   "name": "Adobe Experience Cloud", "cat": "CDP",      "ids": "ECID, Email, Segment ID"},
    {"id": "segment", "name": "Segment (Twilio)",        "cat": "CDP",      "ids": "Anonymous ID, User ID, Email"},
    {"id": "braze",   "name": "Braze",                  "cat": "CRM",      "ids": "External ID, Email, Push Token"},
    {"id": "sap",     "name": "SAP Commerce Cloud",     "cat": "Commerce", "ids": "Business Partner, Email, Order Ref"},
    {"id": "mp",      "name": "mParticle",              "cat": "CDP",      "ids": "MPID, Email, IDFA/GAID"},
    {"id": "hs",      "name": "HubSpot (beta)",         "cat": "CRM",      "ids": "Contact ID, Email, Company ID"},
]

SEGMENTS_DF = pd.DataFrame([
    {"Segment": "High-Value Shoppers",   "Before": "22K", "After": "82K",  "Lift": "+273%"},
    {"Segment": "Grocery Loyalists",     "Before": "64K", "After": "210K", "Lift": "+228%"},
    {"Segment": "Electronics Intenders", "Before": "18K", "After": "54K",  "Lift": "+200%"},
    {"Segment": "Ramadan Buyers",        "Before": "90K", "After": "340K", "Lift": "+278%"},
    {"Segment": "Auto In-Market",        "Before": "9K",  "After": "28K",  "Lift": "+211%"},
    {"Segment": "Vision 2030 Consumers", "Before": "38K", "After": "130K", "Lift": "+242%"},
])

RMN_PARTNERS = [
    {"name": "Noon",             "reach": "3.2M users",    "formats": "Sponsored, Display",    "color": "#FFC200"},
    {"name": "Carrefour Arabia", "reach": "1.8M members",  "formats": "In-store + Digital",    "color": "#60a5fa"},
    {"name": "LuLu Hypermarket", "reach": "1.4M customers","formats": "Display, Sponsored",    "color": "#34d399"},
    {"name": "Panda Retail",     "reach": "2.1M members",  "formats": "Offsite + Onsite",      "color": "#f472b6"},
    {"name": "Jarir Bookstore",  "reach": "820K members",  "formats": "Display, Email",        "color": "#fb923c"},
    {"name": "Danube Home",      "reach": "640K shoppers", "formats": "Sponsored, CTV",        "color": "#a78bfa"},
]

DSP_PARTNERS = [
    {"name": "Google DV360",        "reach": "18M+ MENA",    "signal": "Customer Match",  "type": "DSP"},
    {"name": "Meta Business",       "reach": "16M+ MENA",    "signal": "Custom Audience", "type": "Social"},
    {"name": "Snapchat",            "reach": "21M KSA",      "signal": "Snap Audience",   "type": "Social"},
    {"name": "TikTok for Business", "reach": "12M MENA",     "signal": "Custom Audience", "type": "Social"},
    {"name": "Amazon DSP",          "reach": "4M+ KSA",      "signal": "Amazon Audiences","type": "DSP"},
    {"name": "The Trade Desk",      "reach": "Open web",     "signal": "UID 2.0",         "type": "DSP"},
    {"name": "STC Ads",             "reach": "18M KSA subs", "signal": "Mobile Identity", "type": "Telco"},
]

CHANNELS_ROAS = {
    "Channel": ["STC Ads", "Noon RMN", "Snapchat KSA", "Google DV360", "Meta MENA"],
    "ROAS":    [6.1,        5.4,        4.8,            3.9,            3.2],
    "Reach":   ["820K",     "1.1M",     "2.2M",         "3.1M",         "4.4M"],
    "Color":   [PURPLE_LT,  GOLD,       "#FFDD00",      "#4285F4",      "#0668E1"],
}

INCREMENTALITY_DF = pd.DataFrame([
    {"Metric": "Incremental Conversions", "Value": "7,840",     "Note": "81.2% of total"},
    {"Metric": "Incremental Revenue",     "Value": "SAR 2.2M",  "Note": "Attributed to Numad"},
    {"Metric": "True Lift",               "Value": "+18.2%",    "Note": "vs holdout group"},
    {"Metric": "iROAS",                   "Value": "2.9x",      "Note": "Incremental return"},
    {"Metric": "Holdout Group Size",      "Value": "18.8%",     "Note": "of total audience"},
])

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
  connectors: [salesforce, shopify, adobe_ec, segment, braze, sap_commerce, mparticle, hubspot]
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

API_ENDPOINTS = pd.DataFrame([
    {"Method": "POST", "Endpoint": "/v1/ingest/initiate",           "Description": "Stage hashed IDs into Snowflake"},
    {"Method": "POST", "Endpoint": "/v1/ingest/open-flow/connect",  "Description": "Authenticate an Open Flow connector"},
    {"Method": "GET",  "Endpoint": "/v1/ingest/status",             "Description": "Check ingestion job status"},
    {"Method": "POST", "Endpoint": "/v1/graph/run",                 "Description": "Run identity graph matching"},
    {"Method": "GET",  "Endpoint": "/v1/graph/results",             "Description": "Overlap stats and segment expansion"},
    {"Method": "POST", "Endpoint": "/v1/activate",                  "Description": "Push audience to partner destination"},
    {"Method": "GET",  "Endpoint": "/v1/measure/roas",              "Description": "Closed-loop ROAS by channel"},
    {"Method": "GET",  "Endpoint": "/v1/measure/lift",              "Description": "True lift and incrementality report"},
])


# ── Shared UI helpers ─────────────────────────────────────────────────────────
def nav_header():
    """Top navigation bar."""
    col_logo, col_nav, col_right = st.columns([2, 6, 2])

    with col_logo:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;padding:8px 0;">
          <div style="width:38px;height:38px;background:linear-gradient(135deg,#7c3aed,#29d4f5);
               border-radius:10px;display:flex;align-items:center;justify-content:center;
               box-shadow:0 0 18px #29d4f540;">
            <span style="font-size:18px;font-weight:900;color:white;">N</span>
          </div>
          <div>
            <div style="font-size:14px;font-weight:900;color:white;letter-spacing:1.2px;line-height:1.1;">
              NUMAD<span style="color:#29d4f5;">.AI</span>
            </div>
            <div style="font-size:8px;color:#8b7ab8;letter-spacing:1.8px;font-weight:600;margin-top:1px;">
              IDENTITY INTELLIGENCE CLOUD
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_nav:
        pages = [
            ("overview",  "Overview"),
            ("ingest",    "01 · Ingest Data"),
            ("graph",     "02 · Create Graph"),
            ("activate",  "03 · Activate"),
            ("measure",   "04 · Measure"),
            ("techspec",  "Spec"),
        ]
        cols = st.columns(len(pages))
        for col, (pid, label) in zip(cols, pages):
            with col:
                is_active = st.session_state.page == pid
                if st.button(label, key=f"nav_{pid}",
                             type="primary" if is_active else "secondary",
                             use_container_width=True):
                    st.session_state.page = pid
                    st.rerun()

    with col_right:
        st.markdown("""
        <div style="display:flex;align-items:center;justify-content:flex-end;gap:6px;
             padding:8px 0;background:#29B5E812;border:1px solid #29B5E830;
             border-radius:7px;padding:6px 12px;margin-top:4px;">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
            <line x1="12" y1="2" x2="12" y2="22" stroke="#29B5E8" stroke-width="2" stroke-linecap="round"/>
            <line x1="2" y1="12" x2="22" y2="12" stroke="#29B5E8" stroke-width="2" stroke-linecap="round"/>
            <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" stroke="#29B5E8" stroke-width="2" stroke-linecap="round"/>
            <line x1="19.07" y1="4.93" x2="4.93" y2="19.07" stroke="#29B5E8" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span style="font-size:9px;font-weight:800;color:#29B5E8;letter-spacing:0.8px;white-space:nowrap;">
            POWERED BY SNOWFLAKE
          </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0 0 12px 0;border-color:#3d1f7a;'>", unsafe_allow_html=True)


def back_btn(label: str, target: str):
    if st.button(f"← {label}", key=f"back_{target}"):
        st.session_state.page = target
        st.rerun()


def section_header(step_label: str, title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="margin-bottom:20px;">
      <div style="color:#29d4f5;font-size:10px;letter-spacing:3px;font-weight:700;margin-bottom:6px;">
        {step_label}
      </div>
      <div style="font-size:26px;font-weight:900;color:white;margin-bottom:6px;letter-spacing:-0.5px;">
        {title}
      </div>
      <div style="color:#8b7ab8;font-size:13px;line-height:1.65;max-width:750px;">
        {subtitle}
      </div>
    </div>
    """, unsafe_allow_html=True)


def card(content_fn, border_color="#3d1f7a"):
    """Render content inside a styled card."""
    st.markdown(f"""
    <div style="background:#251050;border:1.5px solid {border_color};
         border-radius:14px;padding:20px 22px;margin-bottom:12px;">
    """, unsafe_allow_html=True)
    content_fn()
    st.markdown("</div>", unsafe_allow_html=True)


def roas_chart():
    df = pd.DataFrame(CHANNELS_ROAS)
    fig = go.Figure(go.Bar(
        x=df["ROAS"],
        y=df["Channel"],
        orientation="h",
        marker_color=df["Color"],
        text=[f"{r}x" for r in df["ROAS"]],
        textposition="outside",
        textfont=dict(color="white", size=12),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=10, r=60, t=10, b=10),
        height=240,
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(tickfont=dict(color="#8b7ab8", size=11), gridcolor="#3d1f7a"),
        showlegend=False,
    )
    return fig


def roas_trend_chart():
    weeks = ["Wk 1", "Wk 2", "Wk 3", "Wk 4", "Wk 5", "Wk 6"]
    vals  = [2.4, 2.7, 3.1, 3.4, 3.2, 3.8]
    fig = go.Figure(go.Scatter(
        x=weeks, y=vals,
        mode="lines+markers",
        line=dict(color=CYAN, width=2.5),
        marker=dict(color=CYAN, size=7),
        fill="tozeroy",
        fillcolor=f"rgba(41,212,245,0.12)",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=10, r=10, t=10, b=10),
        height=160,
        xaxis=dict(tickfont=dict(color="#8b7ab8", size=10), gridcolor="#3d1f7a"),
        yaxis=dict(tickfont=dict(color="#8b7ab8", size=10), gridcolor="#3d1f7a"),
        showlegend=False,
    )
    return fig


def venn_chart():
    fig = go.Figure()
    fig.add_shape(type="circle", x0=0.05, y0=0.1, x1=0.65, y1=0.9,
                  fillcolor="rgba(124,58,237,0.25)", line_color=PURPLE_LT, line_width=1.5)
    fig.add_shape(type="circle", x0=0.35, y0=0.1, x1=0.95, y1=0.9,
                  fillcolor="rgba(41,212,245,0.2)", line_color=CYAN, line_width=1.5)
    # intersection highlight
    fig.add_shape(type="circle", x0=0.31, y0=0.15, x1=0.69, y1=0.85,
                  fillcolor="rgba(16,217,160,0.25)", line_color="rgba(0,0,0,0)")
    fig.add_annotation(x=0.22, y=0.72, text="<b>YOUR IDs</b>", showarrow=False,
                       font=dict(color=PURPLE_LT, size=11))
    fig.add_annotation(x=0.22, y=0.60, text="82K", showarrow=False,
                       font=dict(color="#8b7ab8", size=10))
    fig.add_annotation(x=0.78, y=0.72, text="<b>NUMAD<br>GRAPH</b>", showarrow=False,
                       font=dict(color=CYAN, size=11))
    fig.add_annotation(x=0.78, y=0.55, text="820K+", showarrow=False,
                       font=dict(color="#8b7ab8", size=10))
    fig.add_annotation(x=0.50, y=0.62, text="<b>87%</b>", showarrow=False,
                       font=dict(color="white", size=16))
    fig.add_annotation(x=0.50, y=0.50, text="MATCH", showarrow=False,
                       font=dict(color=GREEN, size=11))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=200,
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        showlegend=False,
    )
    return fig


def signal_coverage_chart():
    labels = ["Email coverage", "Mobile coverage", "Cross-device", "Loyalty ID"]
    before = [74, 48, 0, 0]
    after  = [89, 71, 74, 61]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Before", x=before, y=labels, orientation="h",
                         marker_color="rgba(61,31,122,0.6)", width=0.35))
    fig.add_trace(go.Bar(name="After",  x=after,  y=labels, orientation="h",
                         marker_color=CYAN, width=0.35))
    fig.update_layout(
        barmode="overlay",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=10, r=30, t=10, b=10),
        height=200,
        legend=dict(font=dict(size=10, color="#8b7ab8")),
        xaxis=dict(range=[0, 100], ticksuffix="%", tickfont=dict(color="#8b7ab8", size=10),
                   gridcolor="#3d1f7a"),
        yaxis=dict(tickfont=dict(color="#8b7ab8", size=11)),
    )
    return fig


# ── Pages ─────────────────────────────────────────────────────────────────────

def page_overview():
    section_header("IDENTITY INTELLIGENCE CLOUD", "Sovereign Data & AI",
                   "Privacy-preserving identity resolution and audience activation — powered by Snowflake secure data collaboration.")

    # KPI row
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Resolved IDs",       "820K",  "In Numad graph")
    with k2: st.metric("Match Rate",          "87%",   "Deterministic links")
    with k3: st.metric("Avg ROAS",            "3.4x",  "Across KSA RMNs")
    with k4: st.metric("Time to Activation",  "<72h",  "From ingest to live")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Charts row
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**ROAS by Activation Channel**")
        st.plotly_chart(roas_chart(), use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.markdown("**6-Week ROAS Trend**")
        st.plotly_chart(roas_trend_chart(), use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("### Start your journey")

    cols = st.columns(4)
    steps = [
        ("ingest",   "01 · Ingest Data",        CYAN,      "Connect 1P data via native Snowflake objects or Open Flow connectors."),
        ("graph",    "02 · Create Graph",        PURPLE_LT, "Match and enrich IDs against the Numad identity graph."),
        ("activate", "03 · Activate Audiences",  PINK,      "Push enriched audiences to RMNs and DSP partners."),
        ("measure",  "04 · Measure Campaigns",   GREEN,     "Closed-loop attribution inside Snowflake."),
    ]
    for col, (pid, title, color, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div style="background:#251050;border:1.5px solid #3d1f7a;border-top:3px solid {color};
                 border-radius:12px;padding:16px;cursor:pointer;min-height:130px;">
              <div style="font-size:12px;font-weight:800;color:{color};margin-bottom:8px;">{title}</div>
              <div style="font-size:11px;color:#8b7ab8;line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open →", key=f"ov_{pid}", use_container_width=True):
                st.session_state.page = pid
                st.rerun()


def page_ingest():
    back_btn("Back to Overview", "overview")
    section_header("STEP 1 OF 4", "Ingest Data",
                   "Choose how to bring your first-party data into Snowflake. Use native objects for file/export uploads, "
                   "Open Flow connectors for direct platform sync — or both.")

    col_left, col_right = st.columns(2)

    # ── Native Snowflake Objects ──────────────────────────────────────────────
    with col_left:
        st.markdown(f"""
        <div style="background:#251050;border:1.5px solid #3d1f7a;border-radius:14px;
             padding:14px 16px;margin-bottom:4px;">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <line x1="12" y1="2" x2="12" y2="22" stroke="#29B5E8" stroke-width="2" stroke-linecap="round"/>
              <line x1="2" y1="12" x2="22" y2="12" stroke="#29B5E8" stroke-width="2" stroke-linecap="round"/>
              <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" stroke="#29B5E8" stroke-width="2" stroke-linecap="round"/>
              <line x1="19.07" y1="4.93" x2="4.93" y2="19.07" stroke="#29B5E8" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <b style="color:white;font-size:13px;">Native Snowflake Objects</b>
          </div>
          <div style="color:#8b7ab8;font-size:11px;">Upload files or exports — Numad stages and hashes in your account</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Select your data types**")
        native_opts = [f"{s['tag']} — {s['label']}" for s in NATIVE_SOURCES]
        selected_native = st.multiselect("Data types", native_opts,
                                         default=st.session_state.native_sources,
                                         label_visibility="collapsed",
                                         key="native_sel")
        st.session_state.native_sources = selected_native

        st.markdown("**Snowflake objects Numad provisions in your account**")
        sf_df = pd.DataFrame([{"Object": o["name"], "Type": o["type"], "Description": o["desc"]}
                               for o in SF_OBJECTS])
        st.dataframe(sf_df, hide_index=True, use_container_width=True,
                     column_config={
                         "Object": st.column_config.TextColumn(width="medium"),
                         "Type":   st.column_config.TextColumn(width="medium"),
                     })

        st.info("🔐 **SHA-256 + HMAC-SHA256** runs in your environment before upload. Numad never sees raw PII.")

    # ── Open Flow Connectors ─────────────────────────────────────────────────
    with col_right:
        st.markdown(f"""
        <div style="background:#251050;border:1.5px solid #3d1f7a;border-radius:14px;
             padding:14px 16px;margin-bottom:4px;">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
            <span style="font-size:16px;">🔗</span>
            <b style="color:white;font-size:13px;">Open Flow Connectors</b>
          </div>
          <div style="color:#8b7ab8;font-size:11px;">OAuth-authenticated sync — no manual file exports required</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Select connectors to authenticate**")
        of_opts = [c["name"] for c in OF_CONNECTORS]
        selected_of = st.multiselect("Connectors", of_opts,
                                     default=st.session_state.of_connectors,
                                     label_visibility="collapsed",
                                     key="of_sel")
        st.session_state.of_connectors = selected_of

        if selected_of:
            of_df = pd.DataFrame([
                {"Connector": c["name"], "Category": c["cat"], "Identity Fields": c["ids"]}
                for c in OF_CONNECTORS if c["name"] in selected_of
            ])
            st.dataframe(of_df, hide_index=True, use_container_width=True)
            st.success(f"✓ OAuth handshake completes at ingestion — data syncs directly into Snowflake")

        st.markdown("""
        <div style="margin-top:12px;padding:12px;background:rgba(16,217,160,0.06);
             border:1px solid rgba(16,217,160,0.2);border-radius:8px;font-size:11px;color:#10d9a0;">
          🛡️ Saudi PDPL & SDAIA compliant — purpose limitation enforced at the Snowflake object level
          for both ingestion paths
        </div>
        """, unsafe_allow_html=True)

    # ── CTA ─────────────────────────────────────────────────────────────────
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    total = len(selected_native) + len(selected_of)
    if not st.session_state.ingest_done:
        if total > 0:
            if st.button(f"Ingest {total} source{'s' if total > 1 else ''} →", type="primary"):
                st.session_state.ingest_done = True
                st.rerun()
        else:
            st.info("Select at least one data type or connector above to begin ingestion.")
    else:
        st.success(f"✅ Ingestion staged in Snowflake — {len(selected_native)} native source(s) · {len(selected_of)} Open Flow connector(s)")
        if st.button("Create Graph →", type="primary"):
            st.session_state.page = "graph"
            st.rerun()


def page_graph():
    back_btn("Back to Ingest Data", "ingest")
    section_header("STEP 2 OF 4", "Create Graph",
                   "Match your hashed IDs against the Numad identity graph. Matched IDs get enriched with new signals; "
                   "additional reachable profiles are unlocked via household and device graph links.")

    if not st.session_state.graph_complete:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Ready to graph**")
            st.metric("Your ingested IDs", "82K")
            st.metric("Sources selected", str(max(len(st.session_state.native_sources) + len(st.session_state.of_connectors), 1)))
            st.metric("Signal types (before)", "3")

        with col_b:
            st.markdown("**Snowflake objects that will be created**")
            sf_df = pd.DataFrame([{"Object": o["name"], "Type": o["type"]}
                                   for o in SF_OBJECTS[2:]])
            st.dataframe(sf_df, hide_index=True, use_container_width=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("▶  Run Identity Graph", type="primary"):
            with st.spinner("Building your identity graph inside Snowflake — no raw data leaves your environment..."):
                import time
                tasks = [
                    "SHA-256 hashing all PII fields",
                    "Uploading hashed IDs to Snowflake",
                    "Matching against Numad identity graph",
                    "Cross-device resolution pass",
                    "Linking partner clean room signals",
                    "Computing overlap and expansion metrics",
                ]
                prog = st.progress(0)
                status = st.empty()
                for i, task in enumerate(tasks):
                    status.markdown(f"✦ *{task}...*")
                    time.sleep(0.55)
                    prog.progress((i + 1) / len(tasks))
                status.success("✅ Identity graph built successfully")
            st.session_state.graph_complete = True
            st.rerun()
    else:
        # Results banner
        st.success("✅ Graph complete — identity graph built")
        b1, b2, b3 = st.columns(3)
        with b1: st.metric("IDs Matched",    "71K",  "87% of your 82K IDs")
        with b2: st.metric("Match Rate",     "87%",  "Deterministic + probabilistic")
        with b3: st.metric("New Reach",      "66K",  "Via household & device links")

        st.markdown("""
        <div style="background:rgba(16,217,160,0.07);border:1px solid rgba(16,217,160,0.2);
             border-radius:10px;padding:12px 16px;font-size:12px;color:#8b7ab8;margin-bottom:16px;">
          87% of your 82K IDs were matched in the Numad graph. Matched profiles are enriched with new signals,
          and <b style="color:#10d9a0;">66K additional profiles</b> are reachable via household and device links.
          Total addressable: <b style="color:#10d9a0;">137K</b> (+67% vs. input).
        </div>
        """, unsafe_allow_html=True)

        # Charts
        r1, r2 = st.columns(2)
        with r1:
            st.markdown("**Overlap diagram**")
            st.plotly_chart(venn_chart(), use_container_width=True, config={"displayModeBar": False})

            # Stat tiles
            t1, t2, t3 = st.columns(3)
            with t1:
                st.metric("Your IDs",           "82K",  "ingested")
            with t2:
                st.metric("Matched in graph",   "71K",  "87% of yours")
            with t3:
                st.metric("New reach unlocked", "66K",  "via graph links")

            st.markdown(f"""
            <div style="background:rgba(16,217,160,0.07);border:1px solid rgba(16,217,160,0.2);
                 border-radius:8px;padding:10px 14px;display:flex;
                 justify-content:space-between;align-items:center;margin-top:8px;">
              <span style="font-size:12px;color:#8b7ab8;">Total addressable after enrichment</span>
              <span style="font-size:18px;font-weight:900;color:#10d9a0;">137K <span style="font-size:12px;">(+67%)</span></span>
            </div>
            """, unsafe_allow_html=True)

        with r2:
            st.markdown("**Signal coverage** (matched IDs)")
            st.plotly_chart(signal_coverage_chart(), use_container_width=True, config={"displayModeBar": False})

        st.markdown("**Segment expansion**")
        st.dataframe(SEGMENTS_DF, hide_index=True, use_container_width=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("⚡  Activate Audiences →", type="primary"):
            st.session_state.page = "activate"
            st.rerun()


def page_activate():
    back_btn("Back to Create Graph", "graph")
    section_header("STEP 3 OF 4", "Activate Audiences",
                   "Push privacy-safe hashed audiences to your selected partners — all match keys via Snowflake Data Share, "
                   "zero raw data exposure.")

    st.success("✅  137K enriched profiles ready  ·  71K matched + 66K new reach  ·  87% match rate")

    if not st.session_state.activation_launched:
        tab_rmn, tab_dsp = st.tabs(["Retail Media Networks", "DSP & Ad Tech"])

        with tab_rmn:
            rmn_df = pd.DataFrame([
                {"Partner": p["name"], "Reach": p["reach"], "Formats": p["formats"]}
                for p in RMN_PARTNERS
            ])
            st.dataframe(rmn_df, hide_index=True, use_container_width=True)
            rmn_opts = [p["name"] for p in RMN_PARTNERS]
            sel_rmn = st.multiselect("Select RMN partners", rmn_opts,
                                     default=[p for p in st.session_state.activated_partners if p in rmn_opts],
                                     key="rmn_sel")

        with tab_dsp:
            dsp_df = pd.DataFrame([
                {"Partner": p["name"], "Reach": p["reach"], "Signal": p["signal"], "Type": p["type"]}
                for p in DSP_PARTNERS
            ])
            st.dataframe(dsp_df, hide_index=True, use_container_width=True)
            dsp_opts = [p["name"] for p in DSP_PARTNERS]
            sel_dsp = st.multiselect("Select DSP partners", dsp_opts,
                                     default=[p for p in st.session_state.activated_partners if p in dsp_opts],
                                     key="dsp_sel")

        all_sel = sel_rmn + sel_dsp
        st.session_state.activated_partners = all_sel

        if all_sel:
            st.markdown(f"**{len(all_sel)} partner(s) selected:** {', '.join(all_sel)}")
            st.caption("Hashed match keys only — delivered via Snowflake Data Share")
            if st.button(f"⚡  Launch Activation to {len(all_sel)} partner(s)", type="primary"):
                st.session_state.activation_launched = True
                st.rerun()
        else:
            st.info("Select at least one partner to activate.")
    else:
        st.success(f"✅ Activation launched — 137K hashed profiles sent to: **{', '.join(st.session_state.activated_partners)}** via Snowflake.\n\nAudiences available within 2–4 hours.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Add more partners"):
                st.session_state.activation_launched = False
                st.rerun()
        with c2:
            if st.button("📊  Measure Campaigns →", type="primary"):
                st.session_state.page = "measure"
                st.rerun()


def page_measure():
    back_btn("Back to Activate Audiences", "activate")
    section_header("STEP 4 OF 4", "Measure Campaigns",
                   "Closed-loop attribution and true lift measurement — all computed inside Snowflake, "
                   "no raw data shared with any partner.")

    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Total Reach",         "1.4M",     "+11.2% vs prior")
    with k2: st.metric("Matched Conversions", "28K",      "+19.4% vs prior")
    with k3: st.metric("Incremental ROAS",    "3.8x",     "+0.4x vs prior")
    with k4: st.metric("Incremental Revenue", "SAR 2.2M", "Attribution: 81%")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**ROAS by Activation Channel**")
        st.plotly_chart(roas_chart(), use_container_width=True, config={"displayModeBar": False})
        st.markdown("**6-Week ROAS Trend**")
        st.plotly_chart(roas_trend_chart(), use_container_width=True, config={"displayModeBar": False})

    with c2:
        st.markdown("**Incrementality Measurement**")
        st.dataframe(INCREMENTALITY_DF, hide_index=True, use_container_width=True,
                     column_config={
                         "Metric": st.column_config.TextColumn(width="medium"),
                         "Value":  st.column_config.TextColumn(width="small"),
                         "Note":   st.column_config.TextColumn(width="medium"),
                     })
        st.markdown("""
        <div style="margin-top:12px;background:rgba(41,212,245,0.06);border:1px solid rgba(41,212,245,0.2);
             border-radius:8px;padding:12px;font-size:11px;color:#29d4f5;">
          🔒 Computed inside Snowflake. No raw conversion data shared with any partner.
        </div>
        """, unsafe_allow_html=True)


def page_techspec():
    section_header("SNOWFLAKE SECURE DATA COLLABORATION SPEC", "Technical Specification")

    tab_arch, tab_yaml, tab_api = st.tabs(["Architecture", "Collaboration YAML", "API Reference"])

    with tab_arch:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Secure Data Collaboration Config**")
            arch_df = pd.DataFrame([
                {"Property": "Type",        "Value": "Snowflake Secure Data Collaboration"},
                {"Property": "Region",      "Value": "AWS me-central-1 (KSA)"},
                {"Property": "Hashing",     "Value": "SHA-256 + HMAC-SHA256 (client-side)"},
                {"Property": "Privacy",     "Value": "Differential Privacy (ε=1.0)"},
                {"Property": "Threshold",   "Value": "Aggregation k≥50"},
                {"Property": "Compliance",  "Value": "Saudi PDPL / SDAIA"},
                {"Property": "Residency",   "Value": "KSA — no cross-border transfer"},
                {"Property": "Open Flow",   "Value": "OAuth2, incremental sync, 8 connectors"},
            ])
            st.dataframe(arch_df, hide_index=True, use_container_width=True)

        with c2:
            st.markdown("**Identity Namespaces**")
            ns_df = pd.DataFrame([
                {"Namespace": "SHA256_EMAIL",  "Type": "Deterministic",  "Coverage": "74%"},
                {"Namespace": "SHA256_PHONE",  "Type": "Deterministic",  "Coverage": "61%"},
                {"Namespace": "BRAND_NS",      "Type": "Deterministic",  "Coverage": "100%"},
                {"Namespace": "IDFA_GAID",     "Type": "Probabilistic",  "Coverage": "48%"},
                {"Namespace": "LOYALTY_NS",    "Type": "Deterministic",  "Coverage": "38%"},
                {"Namespace": "UID2",          "Type": "Deterministic",  "Coverage": "22%"},
                {"Namespace": "MAID",          "Type": "Probabilistic",  "Coverage": "41%"},
            ])
            st.dataframe(ns_df, hide_index=True, use_container_width=True)

    with tab_yaml:
        st.code(COLLAB_YAML, language="yaml")
        st.download_button("⬇  Download YAML", COLLAB_YAML,
                           file_name="numad_collab_spec.yaml", mime="text/yaml")

    with tab_api:
        st.markdown("**REST API Endpoints**")
        st.dataframe(API_ENDPOINTS, hide_index=True, use_container_width=True,
                     column_config={
                         "Method":      st.column_config.TextColumn(width="small"),
                         "Endpoint":    st.column_config.TextColumn(width="large"),
                         "Description": st.column_config.TextColumn(width="large"),
                     })


# ── Router ────────────────────────────────────────────────────────────────────
nav_header()

pages = {
    "overview": page_overview,
    "ingest":   page_ingest,
    "graph":    page_graph,
    "activate": page_activate,
    "measure":  page_measure,
    "techspec": page_techspec,
}

pages.get(st.session_state.page, page_overview)()
