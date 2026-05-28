import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Payment Analysis Dashboard",
    page_icon="⚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&family=DM+Mono:wght@400;500;600&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* ── Main background ── */
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #f8f9fc 50%, #f0f7f4 100%);
        background-attachment: fixed;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #0f172a !important;
        border-right: none !important;
        box-shadow: 4px 0 24px rgba(0,0,0,0.15);
    }
    [data-testid="stSidebar"] * { color: #94a3b8 !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #f1f5f9 !important; }

    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background: #1e293b !important;
        border: 1.5px solid #334155 !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {
        background: #1d4ed8 !important;
        border-radius: 6px !important;
    }
    [data-testid="stSidebar"] .stTextInput input {
        background: #1e293b !important;
        border: 1.5px solid #334155 !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] ::-webkit-scrollbar { width: 4px; }
    [data-testid="stSidebar"] ::-webkit-scrollbar-track { background: #0f172a; }
    [data-testid="stSidebar"] ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }

    /* ── KPI Cards ── */
    .metric-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 22px 24px 20px 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06), 0 1px 4px rgba(0,0,0,0.04);
        transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.25s ease;
        border: 1px solid rgba(255,255,255,0.9);
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 16px 40px rgba(0,0,0,0.12), 0 4px 12px rgba(0,0,0,0.06);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 5px;
        border-radius: 20px 20px 0 0;
    }
    .metric-card::after {
        content: '';
        position: absolute;
        bottom: -30px; right: -20px;
        width: 110px; height: 110px;
        border-radius: 50%;
        opacity: 0.05;
    }
    .card-blue::before   { background: linear-gradient(90deg, #2563eb, #60a5fa, #38bdf8); }
    .card-blue::after    { background: #2563eb; }
    .card-amber::before  { background: linear-gradient(90deg, #d97706, #fbbf24, #fde68a); }
    .card-amber::after   { background: #d97706; }
    .card-red::before    { background: linear-gradient(90deg, #dc2626, #f87171, #fca5a5); }
    .card-red::after     { background: #dc2626; }
    .card-green::before  { background: linear-gradient(90deg, #059669, #34d399, #6ee7b7); }
    .card-green::after   { background: #059669; }
    .card-violet::before { background: linear-gradient(90deg, #7c3aed, #a78bfa, #c4b5fd); }
    .card-violet::after  { background: #7c3aed; }

    .metric-bg-icon {
        position: absolute;
        right: 16px;
        top: 14px;
        font-size: 36px;
        opacity: 0.12;
        line-height: 1;
    }
    .metric-label {
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 1.6px;
        text-transform: uppercase;
        color: #94a3b8;
        margin-bottom: 10px;
        font-family: 'Outfit', sans-serif;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
        font-family: 'DM Mono', monospace;
        line-height: 1;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    .metric-sub {
        font-size: 11px;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 6px;
    }
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 9px;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 20px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        font-family: 'Outfit', sans-serif;
    }
    .badge-red    { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
    .badge-green  { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
    .badge-blue   { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
    .badge-amber  { background: #fffbeb; color: #d97706; border: 1px solid #fde68a; }
    .badge-violet { background: #f5f3ff; color: #7c3aed; border: 1px solid #ddd6fe; }

    /* ── Section Headers ── */
    .section-header {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #64748b;
        margin: 28px 0 12px 0;
        display: flex;
        align-items: center;
        gap: 12px;
        font-family: 'Outfit', sans-serif;
    }
    .section-header::before {
        content: '';
        width: 4px;
        height: 16px;
        border-radius: 4px;
        background: linear-gradient(180deg, #2563eb, #7c3aed);
        flex-shrink: 0;
    }
    .section-header::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, #e2e8f0 0%, transparent 100%);
    }

    /* ── Page title ── */
    .dash-title {
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.8px;
        font-family: 'Outfit', sans-serif;
        line-height: 1.2;
    }
    .dash-subtitle {
        font-size: 12px;
        color: #64748b;
        margin-top: 5px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .dot-sep {
        width: 3px; height: 3px;
        background: #cbd5e1;
        border-radius: 50%;
        display: inline-block;
    }

    /* ── Chart containers ── */
    .chart-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 8px 8px 0 8px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        border: 1px solid #f1f5f9;
    }

    /* ── Sidebar brand ── */
    .sidebar-brand {
        padding: 24px 0 20px 0;
    }
    .brand-logo {
        font-size: 20px;
        font-weight: 800;
        color: #f1f5f9 !important;
        letter-spacing: -0.5px;
        font-family: 'Outfit', sans-serif;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .brand-tag {
        font-size: 9px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #475569 !important;
        margin-top: 4px;
        font-family: 'Outfit', sans-serif;
    }
    .sidebar-label {
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #475569 !important;
        margin-bottom: 5px;
        margin-top: 16px;
        font-family: 'Outfit', sans-serif;
    }
    .sidebar-divider {
        border: none;
        border-top: 1px solid #1e293b;
        margin: 16px 0;
    }

    /* ── Stat pills in sidebar ── */
    .stat-pill {
        background: #1e293b;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 8px;
        border: 1px solid #334155;
    }
    .stat-pill-label { font-size: 9px; font-weight: 600; color: #64748b !important; letter-spacing: 1px; text-transform: uppercase; }
    .stat-pill-value { font-size: 16px; font-weight: 700; color: #e2e8f0 !important; font-family: 'DM Mono', monospace; margin-top: 2px; }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    }

    /* ── Search input ── */
    .stTextInput input {
        border-radius: 12px !important;
        border: 1.5px solid #e2e8f0 !important;
        padding: 10px 16px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
        background: #ffffff !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stTextInput input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
    }

    /* ── Toolbar & header ── */
    [data-testid="stToolbar"] { display: none !important; }
    header { background: transparent !important; }

    /* ── Sidebar sizing ── */
    [data-testid="stSidebar"] {
        min-width: 252px !important;
        max-width: 252px !important;
        transform: none !important;
        visibility: visible !important;
    }
    [data-testid="stSidebar"] button[kind="header"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="baseButton-headerNoPadding"] {
        display: none !important;
    }

    .block-container { padding-top: 1.8rem; padding-bottom: 1.5rem; }

    /* ── Top filter bar ── */
    .filter-summary-bar {
        background: #ffffff;
        border-radius: 14px;
        padding: 10px 18px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 4px;
    }
    .filter-chip {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 20px;
        padding: 3px 10px;
        font-size: 10px;
        font-weight: 600;
        color: #2563eb;
        letter-spacing: 0.3px;
    }

    /* ── Insights banner ── */
    .insight-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 16px;
        padding: 16px 22px;
        margin: 8px 0 4px 0;
        display: flex;
        align-items: center;
        gap: 18px;
        border: 1px solid #334155;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    .insight-icon {
        font-size: 28px;
        flex-shrink: 0;
    }
    .insight-text {
        font-size: 12px;
        color: #94a3b8;
        line-height: 1.6;
        font-weight: 400;
    }
    .insight-text strong {
        color: #f1f5f9;
        font-weight: 700;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #f8fafc; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 6px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>
""", unsafe_allow_html=True)


# ── Load Data ──────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    file_id = "1VbDVAl9ZQYXe_zpnP_NYMTI7nA2ovUjN"
    try:
        import gdown
        import os
        output_path = "/tmp/Mapped_Output.csv"
        if not os.path.exists(output_path):
            url = f"https://drive.google.com/uc?id={file_id}"
            gdown.download(url, output_path, quiet=False)

        df = pd.read_csv(output_path, low_memory=False)
        df.columns = df.columns.str.strip()

        df['service_date'] = pd.to_datetime(df['service_date'], errors='coerce').dt.strftime('%m/%d/%Y')
        df['Date_Of_Entry'] = pd.to_datetime(df['Date_Of_Entry'], errors='coerce')

        for col in ['Total_Payment', 'InsPayment', 'PatPayment']:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace('[$,]', '', regex=True),
                    errors='coerce'
                ).fillna(0)

        if 'Allowed Contract' in df.columns:
            df['Allowed_Contract_Num'] = pd.to_numeric(
                df['Allowed Contract'].astype(str).str.replace('[$,]', '', regex=True),
                errors='coerce'
            ).fillna(0)
        else:
            df['Allowed_Contract_Num'] = 0

        df['Month_Label'] = df['Date_Of_Entry'].dt.strftime('%b-%y')
        df['Month_Num']   = df['Date_Of_Entry'].dt.month
        df['Year']        = df['Date_Of_Entry'].dt.year

        return df, None
    except Exception as e:
        return None, str(e)


with st.spinner("Loading payment data..."):
    df, error = load_data()


# ── Shared Plotly theme ────────────────────────────────────────────────────
PLOTLY_BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color='#64748b', size=11),
    margin=dict(l=14, r=14, t=42, b=14),
    xaxis=dict(
        gridcolor='#f1f5f9', zeroline=False,
        tickfont=dict(color='#94a3b8', size=10),
        linecolor='#e2e8f0', showline=True
    ),
    yaxis=dict(
        gridcolor='#f1f5f9', zeroline=False,
        tickfont=dict(color='#94a3b8', size=10),
        linecolor='#e2e8f0', showline=False
    ),
)
LEGEND = dict(
    bgcolor='rgba(255,255,255,0.8)',
    font=dict(color='#64748b', size=10),
    borderwidth=1,
    bordercolor='#f1f5f9',
    orientation='h',
    yanchor='bottom', y=1.02,
    xanchor='right', x=1
)
TITLE_FONT = dict(color='#1e293b', size=12, family='Outfit')

PALETTE = ['#2563eb', '#dc2626', '#7c3aed', '#d97706', '#059669', '#db2777', '#0891b2', '#ea580c']
PALETTE_BLUE = ['#1e3a8a', '#1d4ed8', '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe']


# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class='sidebar-brand'>
            <div class='brand-logo'>⚕ Jorie AI</div>
            <div class='brand-tag'>Payment Analytics · ONE AR</div>
        </div>
        <hr class='sidebar-divider'>
    """, unsafe_allow_html=True)

    if df is not None:
        # Dynamic filter options
        year_options     = sorted(df['Year'].dropna().unique().astype(int).tolist(), reverse=True)
        _month_dates     = df['Date_Of_Entry'].dropna().dt.to_period('M').drop_duplicates()
        month_options    = [p.strftime('%b-%y') for p in sorted(_month_dates, reverse=True)]
        carrier_options  = sorted(df['Insurance_Carrier'].dropna().unique().tolist()) if 'Insurance_Carrier' in df.columns else []
        variance_options = sorted(df['Variance'].dropna().unique().tolist())           if 'Variance'          in df.columns else []
        fc_options       = sorted(df['Update_FC'].dropna().unique().tolist())          if 'Update_FC'         in df.columns else []
        cpt_options      = sorted(df['CPT_Category'].dropna().unique().tolist())       if 'CPT_Category'      in df.columns else []
        code_options     = sorted(df['code'].dropna().astype(str).unique().tolist())   if 'code'              in df.columns else []

        st.markdown("<div class='sidebar-label'>📅 Year</div>", unsafe_allow_html=True)
        selected_year = st.multiselect("Year", year_options, default=[], key="year",
                                       placeholder="All years", label_visibility="collapsed")

        st.markdown("<div class='sidebar-label'>🗓 Month</div>", unsafe_allow_html=True)
        selected_month = st.multiselect("Month", month_options, default=[], key="month",
                                        placeholder="All months", label_visibility="collapsed")

        st.markdown("<div class='sidebar-label'>🏥 Insurance Carrier</div>", unsafe_allow_html=True)
        selected_carrier = st.multiselect("Carrier", carrier_options, default=[], key="carrier",
                                          placeholder="All carriers", label_visibility="collapsed")

        st.markdown("<div class='sidebar-label'>⚡ Variance Status</div>", unsafe_allow_html=True)
        selected_variance = st.multiselect("Variance", variance_options, default=[], key="variance",
                                           placeholder="All statuses", label_visibility="collapsed")

        st.markdown("<div class='sidebar-label'>💼 Financial Class</div>", unsafe_allow_html=True)
        selected_fc = st.multiselect("Financial Class", fc_options, default=[], key="fc",
                                     placeholder="All classes", label_visibility="collapsed")

        st.markdown("<div class='sidebar-label'>🏷 CPT Category</div>", unsafe_allow_html=True)
        selected_cpt = st.multiselect("CPT Category", cpt_options, default=[], key="cpt",
                                      placeholder="All categories", label_visibility="collapsed")

        st.markdown("<div class='sidebar-label'>🔢 CPT Code</div>", unsafe_allow_html=True)
        selected_code = st.multiselect("CPT Code", code_options, default=[], key="cpt_code",
                                       placeholder="All codes", label_visibility="collapsed")

    else:
        selected_year = selected_month = selected_carrier = []
        selected_variance = selected_fc = selected_cpt = selected_code = []

    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
    st.markdown("""
        <div style='font-size:9px; color:#334155; text-align:center; padding:4px 0 8px 0;
                    font-weight:600; letter-spacing:1.2px; text-transform:uppercase; font-family:Outfit,sans-serif;'>
            ONE AR · Jorie AI · Contract Intelligence
        </div>
    """, unsafe_allow_html=True)


# ── Error / No Data fallback ───────────────────────────────────────────────
if error or df is None:
    st.error(f"Could not load Mapped_Output.csv: {error}")
    st.info("Make sure you have run the mapping script first and the file exists at the output path.")
    st.stop()


# ── Apply Filters ──────────────────────────────────────────────────────────
filtered = df.copy()
if selected_year:
    filtered = filtered[filtered['Year'].astype(str).isin([str(y) for y in selected_year])]
if selected_month:
    filtered = filtered[filtered['Month_Label'].isin(selected_month)]
if selected_carrier and 'Insurance_Carrier' in filtered.columns:
    filtered = filtered[filtered['Insurance_Carrier'].isin(selected_carrier)]
if selected_variance and 'Variance' in filtered.columns:
    filtered = filtered[filtered['Variance'].isin(selected_variance)]
if selected_fc and 'Update_FC' in filtered.columns:
    filtered = filtered[filtered['Update_FC'].isin(selected_fc)]
if selected_cpt and 'CPT_Category' in filtered.columns:
    filtered = filtered[filtered['CPT_Category'].isin(selected_cpt)]
if selected_code and 'code' in filtered.columns:
    filtered = filtered[filtered['code'].astype(str).isin(selected_code)]


# ── Derived Metrics ────────────────────────────────────────────────────────
total_payment  = filtered['Total_Payment'].sum()
allowed_total  = filtered['Allowed_Contract_Num'].sum()

under_mask = filtered['Total_Payment'] < filtered['Allowed_Contract_Num']
over_mask  = filtered['Total_Payment'] > filtered['Allowed_Contract_Num']
match_mask = filtered['Total_Payment'] == filtered['Allowed_Contract_Num']

total_procedures    = len(filtered)
under_payment_count = int(under_mask.sum())
over_payment_count  = int(over_mask.sum())

# KPI cards — Mapped Contract rows where available, else all filtered rows
mapped_mask = (filtered['Categories'] == 'Mapped Contract') if 'Categories' in filtered.columns else pd.Series([True] * len(filtered), index=filtered.index)
mapped_df   = filtered[mapped_mask] if mapped_mask.sum() > 0 else filtered.copy()

mapped_under   = mapped_df[mapped_df['Total_Payment'] < mapped_df['Allowed_Contract_Num']]
mapped_over    = mapped_df[mapped_df['Total_Payment'] > mapped_df['Allowed_Contract_Num']]
mapped_allowed = mapped_df['Allowed_Contract_Num'].sum()
mapped_actual  = mapped_df['Total_Payment'].sum()

under_payment_amt  = float((mapped_under['Allowed_Contract_Num'] - mapped_under['Total_Payment']).sum())
over_payment_amt   = float((mapped_over['Total_Payment'] - mapped_over['Allowed_Contract_Num']).sum())

pct_under          = (under_payment_count / total_procedures * 100)   if total_procedures > 0 else 0.0
under_pct_of_total = (under_payment_amt  / mapped_allowed   * 100)    if mapped_allowed   > 0 else 0.0
recovery_rate      = (mapped_actual      / mapped_allowed   * 100)    if mapped_allowed   > 0 else 0.0


# ═══════════════════════════════════════════════════════════════════════════
# ── Header
# ═══════════════════════════════════════════════════════════════════════════
col_title, col_logo = st.columns([10, 1])

with col_logo:
    st.markdown("""
        <div style='display:flex; justify-content:flex-end; align-items:flex-start; padding-top:4px;'>
            <a href='https://github.com/kunalvaish49-cpu/VisualCode_UB-04' target='_blank'
               style='text-decoration:none;'>
                <img src='https://raw.githubusercontent.com/kunalvaish49-cpu/VisualCode_UB-04/20be2ac615bd0074353bf7f7b9784af81e6cc040/Jorie%20AI%20Image.webp'
                     style='height:80px; width:auto; border-radius:12px;
                            box-shadow:0 4px 16px rgba(0,0,0,0.14); object-fit:cover;'
                     title='Jorie AI — GitHub'
                />
            </a>
        </div>
    """, unsafe_allow_html=True)

with col_title:
    active_filters = sum([
        len(selected_year)     > 0,
        len(selected_month)    > 0,
        len(selected_carrier)  > 0,
        len(selected_variance) > 0,
        len(selected_fc)       > 0,
        len(selected_cpt)      > 0,
        len(selected_code)     > 0,
    ])

    filter_chips = ""
    if selected_year:
        filter_chips += f"<span class='filter-chip'>📅 {', '.join(str(y) for y in selected_year)}</span> "
    if selected_carrier:
        n = len(selected_carrier)
        filter_chips += f"<span class='filter-chip'>🏥 {selected_carrier[0]}{f' +{n-1}' if n > 1 else ''}</span> "
    if selected_fc:
        n = len(selected_fc)
        filter_chips += f"<span class='filter-chip'>💼 {selected_fc[0]}{f' +{n-1}' if n > 1 else ''}</span> "
    if selected_cpt:
        n = len(selected_cpt)
        filter_chips += f"<span class='filter-chip'>🏷 {selected_cpt[0]}{f' +{n-1}' if n > 1 else ''}</span> "

    filter_badge = (f"<span class='badge badge-blue' style='margin-left:8px;'>"
                    f"{active_filters} filter{'s' if active_filters != 1 else ''} active</span>"
                    if active_filters else "")

    st.markdown(f"""
        <div class='dash-title'>
            Payment Analysis &nbsp;·&nbsp; Under &amp; Over Payment Overview
            {filter_badge}
        </div>
        <div class='dash-subtitle'>
            <span>ONE AR</span>
            <span class='dot-sep'></span>
            <span>Contract Rate Variance Intelligence</span>
            <span class='dot-sep'></span>
            <strong style='color:#0f172a; font-weight:700;'>{total_procedures:,}</strong>
            <span>procedures in view</span>
        </div>
    """, unsafe_allow_html=True)

    if filter_chips:
        st.markdown(f"""
            <div class='filter-summary-bar' style='margin-top:8px;'>
                <span style='font-size:10px; color:#94a3b8; font-weight:600; text-transform:uppercase;
                             letter-spacing:1px; flex-shrink:0;'>Active Filters:</span>
                {filter_chips}
            </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:6px;'></div>", unsafe_allow_html=True)

# ── Smart Insight Banner ─────────────────────────────────────────────────
if total_procedures > 0:
    insight_pct = pct_under
    risk_str = f"${under_payment_amt/1e6:.2f}M" if under_payment_amt >= 1e6 else f"${under_payment_amt/1e3:.0f}K"
    rec_str  = f"{recovery_rate:.1f}%"
    insight_icon = "⚠️" if pct_under > 30 else ("✅" if recovery_rate > 90 else "📊")
    st.markdown(f"""
        <div class='insight-banner'>
            <div class='insight-icon'>{insight_icon}</div>
            <div class='insight-text'>
                <strong>{insight_pct:.1f}%</strong> of procedures ({under_payment_count:,} claims) are under-paid,
                representing <strong>{risk_str}</strong> in revenue at risk.
                Current collection rate is <strong>{rec_str}</strong> of contracted allowable.
                &nbsp;·&nbsp; Over-payment exposure: <strong>${over_payment_amt/1e3:.0f}K</strong>
                across <strong>{len(mapped_over):,}</strong> claims.
            </div>
        </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# ── KPI Cards (5 cards)
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class='metric-card card-blue'>
        <div class='metric-bg-icon'>💰</div>
        <div class='metric-label'>Total Payment Received</div>
        <div class='metric-value'>${total_payment/1e6:.2f}M</div>
        <div class='metric-sub'>{total_procedures:,} total procedures</div>
        <span class='badge badge-blue'>Allowed ${allowed_total/1e6:.2f}M</span>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='metric-card card-amber'>
        <div class='metric-bg-icon'>⚠️</div>
        <div class='metric-label'>% Procedures Under Paid</div>
        <div class='metric-value'>{pct_under:.1f}%</div>
        <div class='metric-sub'>{under_payment_count:,} of {total_procedures:,} claims</div>
        <span class='badge badge-amber'>Under-paid claims</span>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='metric-card card-red'>
        <div class='metric-bg-icon'>📉</div>
        <div class='metric-label'>Under Payment Amount</div>
        <div class='metric-value'>${under_payment_amt/1e6:.2f}M</div>
        <div class='metric-sub'>{under_pct_of_total:.1f}% of contracted allowed</div>
        <span class='badge badge-red'>Revenue at risk</span>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='metric-card card-green'>
        <div class='metric-bg-icon'>📈</div>
        <div class='metric-label'>Over Payment Amount</div>
        <div class='metric-value'>${over_payment_amt/1e6:.2f}M</div>
        <div class='metric-sub'>{len(mapped_over):,} over-paid claims</div>
        <span class='badge badge-green'>Refund exposure</span>
    </div>""", unsafe_allow_html=True)

with c5:
    rate_badge = 'badge-green' if recovery_rate >= 90 else ('badge-amber' if recovery_rate >= 75 else 'badge-red')
    st.markdown(f"""
    <div class='metric-card card-violet'>
        <div class='metric-bg-icon'>🎯</div>
        <div class='metric-label'>Collection Rate</div>
        <div class='metric-value'>{recovery_rate:.1f}%</div>
        <div class='metric-sub'>Actual vs contract allowed</div>
        <span class='badge {rate_badge}'>Contract utilization</span>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# ── Financial Overview
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-header'>Financial Overview</div>", unsafe_allow_html=True)
col_line, col_trend = st.columns([3, 2])

with col_line:
    if 'Update_FC' in filtered.columns:
        if selected_fc and 'Insurance_Carrier' in filtered.columns:
            fc_grp = filtered.groupby('Insurance_Carrier').agg(
                Actual=('Total_Payment', 'sum'),
                Allowed=('Allowed_Contract_Num', 'sum')
            ).reset_index().sort_values('Actual', ascending=False).head(8)
            x_col = 'Insurance_Carrier'
            chart_title = f'Actual vs Allowed — by Carrier ({", ".join(str(s) for s in selected_fc)})'
        else:
            fc_grp = filtered.groupby('Update_FC').agg(
                Actual=('Total_Payment', 'sum'),
                Allowed=('Allowed_Contract_Num', 'sum')
            ).reset_index().sort_values('Actual', ascending=False).head(8)
            x_col = 'Update_FC'
            chart_title = 'Actual vs Allowed — by Financial Class'

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=fc_grp[x_col], y=fc_grp['Actual'] / 1e6,
            mode='lines+markers' if len(fc_grp) > 1 else 'markers',
            name='Actual Payment',
            line=dict(color='#2563eb', width=3),
            marker=dict(size=9, color='#2563eb', line=dict(color='#1e40af', width=2)),
            fill='tozeroy', fillcolor='rgba(37,99,235,0.07)'
        ))
        fig.add_trace(go.Scatter(
            x=fc_grp[x_col], y=fc_grp['Allowed'] / 1e6,
            mode='lines+markers' if len(fc_grp) > 1 else 'markers',
            name='Contract Allowed',
            line=dict(color='#d97706', width=2.5, dash='dot'),
            marker=dict(size=7, color='#d97706', symbol='diamond')
        ))
        fig.update_layout(**PLOTLY_BASE,
            legend=LEGEND,
            title=dict(text=chart_title, font=TITLE_FONT),
            yaxis_tickprefix='$', yaxis_ticksuffix='M', height=300
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col_trend:
    monthly = filtered.groupby('Month_Label').agg(
        Actual=('Total_Payment', 'sum'),
        Allowed=('Allowed_Contract_Num', 'sum')
    ).reset_index()
    monthly['_sort'] = pd.to_datetime(monthly['Month_Label'], format='%b-%y', errors='coerce')
    monthly = monthly.sort_values('_sort').tail(12)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=monthly['Month_Label'], y=monthly['Actual'] / 1e3,
        name='Actual', marker_color='#2563eb', opacity=0.9, marker_line_width=0,
        hovertemplate='<b>%{x}</b><br>Actual: $%{y:,.1f}K<extra></extra>'
    ))
    fig2.add_trace(go.Bar(
        x=monthly['Month_Label'], y=monthly['Allowed'] / 1e3,
        name='Allowed', marker_color='#bfdbfe', opacity=0.9, marker_line_width=0,
        hovertemplate='<b>%{x}</b><br>Allowed: $%{y:,.1f}K<extra></extra>'
    ))
    fig2.update_layout(**PLOTLY_BASE,
        legend=LEGEND,
        title=dict(text='Monthly Payment Trend ($K)', font=TITLE_FONT),
        barmode='group', height=300,
        yaxis_tickprefix='$', yaxis_ticksuffix='K',
        bargap=0.25, bargroupgap=0.08
    )
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})


# ═══════════════════════════════════════════════════════════════════════════
# ── Under Payment: Carriers, Procedures, Providers
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-header'>Under Payment — Carriers · Procedures · Providers</div>", unsafe_allow_html=True)
col_pie, col_proc, col_prov = st.columns(3)

with col_pie:
    if 'Insurance_Carrier' in filtered.columns:
        _uf = filtered[under_mask].copy()
        _uf['_gap'] = _uf['Allowed_Contract_Num'] - _uf['Total_Payment']
        under_carrier = _uf.groupby('Insurance_Carrier').agg(
            Under_Amt=('_gap', 'sum'),
            Claims=('Total_Payment', 'count')
        ).reset_index()
        under_carrier = under_carrier.sort_values('Under_Amt', ascending=False).head(6)
        total_u = _uf['_gap'].sum()

        fig3 = go.Figure(go.Pie(
            labels=under_carrier['Insurance_Carrier'],
            values=under_carrier['Under_Amt'],
            hole=0.60,
            marker=dict(colors=PALETTE, line=dict(color='#ffffff', width=3)),
            textinfo='percent',
            textfont=dict(size=10, family='DM Sans'),
            hovertemplate='<b>%{label}</b><br>Gap: $%{value:,.0f}<br>Share: %{percent}<extra></extra>',
            pull=[0.04, 0, 0, 0, 0, 0]
        ))
        ann_val = f"${total_u/1e6:.2f}M" if total_u >= 1e6 else f"${total_u/1e3:.0f}K"
        fig3.add_annotation(
            text=f'{ann_val}<br><span style="font-size:9px;color:#94a3b8">total gap</span>',
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color='#0f172a', family='DM Mono')
        )
        fig3.update_layout(**PLOTLY_BASE,
            title=dict(text='Under Payment — Top Carriers', font=TITLE_FONT),
            height=320, showlegend=True,
            legend=dict(
                bgcolor='rgba(0,0,0,0)', font=dict(color='#64748b', size=9),
                orientation='v', x=1.01, y=0.5, xanchor='left'
            )
        )
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

with col_proc:
    if 'code' in filtered.columns:
        _pu = filtered[mapped_mask & under_mask].copy() if mapped_mask.sum() > 0 else filtered[under_mask].copy()
        _pu['code'] = _pu['code'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
        _pu = _pu[_pu['code'].notna() & (_pu['code'] != '') & (_pu['code'] != 'nan')]
        _pu['_gap'] = (_pu['Allowed_Contract_Num'] - _pu['Total_Payment']).clip(lower=0)
        proc_under = _pu.groupby('code').agg(Under_Gap=('_gap', 'sum')).reset_index()
        proc_under = proc_under[proc_under['Under_Gap'] > 0]
        proc_under = proc_under.sort_values('Under_Gap', ascending=True).tail(8)

        bar_colors = [f'rgba(37,99,235,{0.4 + 0.6 * i / max(len(proc_under) - 1, 1)})' for i in range(len(proc_under))]

        fig_proc = go.Figure(go.Bar(
            x=proc_under['Under_Gap'] / 1e3,
            y=proc_under['code'].astype(str),
            orientation='h',
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f'${v / 1e3:.1f}K' for v in proc_under['Under_Gap']],
            textposition='outside',
            textfont=dict(color='#64748b', size=10),
            hovertemplate='CPT <b>%{y}</b><br>Gap: $%{x:,.1f}K<extra></extra>'
        ))
        fig_proc.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='DM Sans', color='#64748b', size=11),
            margin=dict(l=14, r=64, t=42, b=14),
            title=dict(text='Under Payment Gap — Top Procedures', font=TITLE_FONT),
            height=320,
            xaxis=dict(
                gridcolor='#f1f5f9', zeroline=False, tickfont=dict(color='#94a3b8', size=10),
                linecolor='#e2e8f0', tickprefix='$', ticksuffix='K', showline=True
            ),
            yaxis=dict(
                gridcolor='#f1f5f9', zeroline=False, tickfont=dict(color='#334155', size=10),
                linecolor='#e2e8f0', type='category', showline=False
            ),
        )
        st.plotly_chart(fig_proc, use_container_width=True, config={'displayModeBar': False})

with col_prov:
    if 'Doctor' in filtered.columns:
        _prov = filtered[mapped_mask & under_mask].copy() if mapped_mask.sum() > 0 else filtered[under_mask].copy()
        _prov['_gap'] = (_prov['Allowed_Contract_Num'] - _prov['Total_Payment']).clip(lower=0)
        prov_under = _prov.groupby('Doctor').agg(Under_Gap=('_gap', 'sum')).reset_index()
        prov_under = prov_under[prov_under['Under_Gap'] > 0]
        prov_under = prov_under.sort_values('Under_Gap', ascending=True).tail(8)
        prov_under['label'] = prov_under['Doctor'].str[:24]

        amber_colors = [f'rgba(217,119,6,{0.35 + 0.65 * i / max(len(prov_under) - 1, 1)})' for i in range(len(prov_under))]

        fig_prov = go.Figure(go.Bar(
            x=prov_under['Under_Gap'] / 1e3,
            y=prov_under['label'],
            orientation='h',
            marker=dict(color=amber_colors, line=dict(width=0)),
            text=[f'${v / 1e3:.1f}K' for v in prov_under['Under_Gap']],
            textposition='outside',
            textfont=dict(color='#64748b', size=10),
            hovertemplate='<b>%{y}</b><br>Gap: $%{x:,.1f}K<extra></extra>'
        ))
        fig_prov.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='DM Sans', color='#64748b', size=11),
            margin=dict(l=14, r=64, t=42, b=14),
            title=dict(text='Under Payment Gap — Top Providers', font=TITLE_FONT),
            height=320,
            xaxis=dict(
                gridcolor='#f1f5f9', zeroline=False, tickfont=dict(color='#94a3b8', size=10),
                linecolor='#e2e8f0', tickprefix='$', ticksuffix='K', showline=True
            ),
            yaxis=dict(
                gridcolor='#f1f5f9', zeroline=False, tickfont=dict(color='#334155', size=10),
                linecolor='#e2e8f0', type='category', showline=False
            ),
        )
        st.plotly_chart(fig_prov, use_container_width=True, config={'displayModeBar': False})


# ═══════════════════════════════════════════════════════════════════════════
# ── Under Payment — Top 5 CPT Categories + Top 10 CPT Actual vs Allowed
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-header'>Under Payment — CPT Category &amp; Procedure Analysis</div>", unsafe_allow_html=True)
col_cat, col_cpt = st.columns([1, 2])

with col_cat:
    if 'CPT_Category' in filtered.columns:
        _cat = filtered[under_mask].copy()
        _cat['_gap'] = _cat['Allowed_Contract_Num'] - _cat['Total_Payment']
        cat_grp = _cat.groupby('CPT_Category').agg(Under_Gap=('_gap', 'sum')).reset_index()
        cat_grp = cat_grp.sort_values('Under_Gap', ascending=True).tail(5)
        cat_grp['label'] = cat_grp['CPT_Category'].str[:24]

        pink_colors = [f'rgba(219,39,119,{0.35 + 0.65 * i / max(len(cat_grp) - 1, 1)})' for i in range(len(cat_grp))]

        fig5 = go.Figure(go.Bar(
            x=cat_grp['Under_Gap'] / 1e3,
            y=cat_grp['label'],
            orientation='h',
            marker=dict(color=pink_colors, line=dict(width=0)),
            text=[f'${v / 1e3:.1f}K' for v in cat_grp['Under_Gap']],
            textposition='outside',
            textfont=dict(color='#64748b', size=10),
            hovertemplate='<b>%{y}</b><br>Gap: $%{x:,.1f}K<extra></extra>'
        ))
        fig5.update_layout(**PLOTLY_BASE,
            title=dict(text='Under Payment — Top 5 CPT Categories', font=TITLE_FONT),
            height=310,
            xaxis_tickprefix='$', xaxis_ticksuffix='K',
            margin=dict(l=14, r=64, t=42, b=14),
        )
        st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})

with col_cpt:
    if 'code' in filtered.columns:
        _cpt_filtered = filtered.copy()
        _cpt_filtered['code'] = _cpt_filtered['code'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
        _cpt_filtered = _cpt_filtered[
            _cpt_filtered['code'].notna() &
            (_cpt_filtered['code'] != '') &
            (_cpt_filtered['code'] != 'nan')
        ]
        cpt_grp = _cpt_filtered.groupby('code').agg(
            Actual=('Total_Payment', 'sum'),
            Allowed=('Allowed_Contract_Num', 'sum')
        ).reset_index().sort_values('Allowed', ascending=False).head(10)
        cpt_labels = cpt_grp['code'].tolist()

        fig_cpt = go.Figure()
        fig_cpt.add_trace(go.Bar(
            name='Actual Payment',
            x=cpt_labels, y=cpt_grp['Actual'] / 1e3,
            marker_color='#2563eb', opacity=0.9, marker_line_width=0,
            hovertemplate='CPT <b>%{x}</b><br>Actual: $%{y:,.1f}K<extra></extra>'
        ))
        fig_cpt.add_trace(go.Bar(
            name='Contract Allowed',
            x=cpt_labels, y=cpt_grp['Allowed'] / 1e3,
            marker_color='#bfdbfe', opacity=0.9, marker_line_width=0,
            hovertemplate='CPT <b>%{x}</b><br>Allowed: $%{y:,.1f}K<extra></extra>'
        ))
        fig_cpt.update_layout(**PLOTLY_BASE,
            legend=LEGEND,
            title=dict(text='Top 10 CPT Codes — Actual vs Contract Allowed ($K)', font=TITLE_FONT),
            barmode='group', height=310,
            yaxis_tickprefix='$', yaxis_ticksuffix='K',
            bargap=0.22, bargroupgap=0.06,
            xaxis_type='category',
            xaxis_tickangle=-35,
        )
        st.plotly_chart(fig_cpt, use_container_width=True, config={'displayModeBar': False})


# ═══════════════════════════════════════════════════════════════════════════
# ── Procedure Contract Rate vs Year (2025 vs 2026)
# ═══════════════════════════════════════════════════════════════════════════
if 'code' in filtered.columns and 'Year' in filtered.columns:
    _code_label = ', '.join(selected_code) if selected_code else 'All'
    _yoy_title = (
        f"CPT {_code_label} — Avg Payment &amp; Contract Rate (2025 vs 2026)"
        if selected_code
        else "Procedure Contract Rate vs Year — Avg Payment &amp; Avg Contract Rate (2025 vs 2026)"
    )
    st.markdown(f"<div class='section-header'>{_yoy_title}</div>", unsafe_allow_html=True)

    mapped_yr = (
        filtered[filtered['Categories'] == 'Mapped Contract']
        if 'Categories' in filtered.columns and (filtered['Categories'] == 'Mapped Contract').sum() > 0
        else filtered.copy()
    )

    if selected_code:
        yr_df = mapped_yr.copy()
        yr_df['code_str'] = yr_df['code'].astype(str)
    else:
        top_codes = (
            mapped_yr.groupby('code')['Total_Payment']
            .sum().nlargest(12).index.tolist()
        )
        yr_df = mapped_yr[mapped_yr['code'].isin(top_codes)].copy()
        yr_df['code_str'] = yr_df['code'].astype(str)

    yr_grp = yr_df.groupby(['code_str', 'Year']).agg(
        Avg_Payment=('Total_Payment', 'mean'),
        Avg_Contract=('Allowed_Contract_Num', 'mean'),
        Count=('Total_Payment', 'count')
    ).reset_index()

    years_present   = sorted(yr_grp['Year'].dropna().unique().astype(int).tolist())
    colors_pay      = {2025: '#60a5fa', 2026: '#1d4ed8'}
    colors_contract = {2025: '#fcd34d', 2026: '#b45309'}

    col_yr1, col_yr2 = st.columns(2)

    with col_yr1:
        fig_yr1 = go.Figure()
        for yr in years_present:
            sub = yr_grp[yr_grp['Year'] == yr].sort_values('code_str')
            if sub.empty:
                continue
            fig_yr1.add_trace(go.Bar(
                name=f'Avg Payment {yr}',
                x=sub['code_str'],
                y=sub['Avg_Payment'],
                marker_color=colors_pay.get(yr, '#60a5fa'),
                opacity=0.9, marker_line_width=0,
                text=[f'${v:,.0f}' for v in sub['Avg_Payment']],
                textposition='outside',
                textfont=dict(size=9, color='#64748b'),
                hovertemplate=f'<b>%{{x}}</b> — {yr}<br>Avg Payment: $%{{y:,.0f}}<extra></extra>'
            ))
        fig_yr1.update_layout(**PLOTLY_BASE,
            legend=LEGEND,
            title=dict(text='Avg Actual Payment per CPT — 2025 vs 2026', font=TITLE_FONT),
            barmode='group', height=340,
            yaxis_tickprefix='$',
            bargap=0.25, bargroupgap=0.08,
            xaxis_type='category', xaxis_tickangle=-35,
        )
        st.plotly_chart(fig_yr1, use_container_width=True, config={'displayModeBar': False})

    with col_yr2:
        fig_yr2 = go.Figure()
        for yr in years_present:
            sub = yr_grp[yr_grp['Year'] == yr].sort_values('code_str')
            if sub.empty:
                continue
            fig_yr2.add_trace(go.Bar(
                name=f'Avg Contract {yr}',
                x=sub['code_str'],
                y=sub['Avg_Contract'],
                marker_color=colors_contract.get(yr, '#fbbf24'),
                opacity=0.9, marker_line_width=0,
                text=[f'${v:,.0f}' for v in sub['Avg_Contract']],
                textposition='outside',
                textfont=dict(size=9, color='#64748b'),
                hovertemplate=f'<b>%{{x}}</b> — {yr}<br>Avg Contract: $%{{y:,.0f}}<extra></extra>'
            ))
        fig_yr2.update_layout(**PLOTLY_BASE,
            legend=LEGEND,
            title=dict(text='Avg Contract Rate per CPT — 2025 vs 2026', font=TITLE_FONT),
            barmode='group', height=340,
            yaxis_tickprefix='$',
            bargap=0.25, bargroupgap=0.08,
            xaxis_type='category', xaxis_tickangle=-35,
        )
        st.plotly_chart(fig_yr2, use_container_width=True, config={'displayModeBar': False})

    # ── YoY summary cards ──────────────────────────────────────────────────
    if 2025 in years_present and 2026 in years_present:
        avg_pay_25 = float(yr_grp[yr_grp['Year'] == 2025]['Avg_Payment'].mean())
        avg_pay_26 = float(yr_grp[yr_grp['Year'] == 2026]['Avg_Payment'].mean())
        avg_con_25 = float(yr_grp[yr_grp['Year'] == 2025]['Avg_Contract'].mean())
        avg_con_26 = float(yr_grp[yr_grp['Year'] == 2026]['Avg_Contract'].mean())

        def yoy_badge(v25, v26):
            if v25 == 0:
                return 0.0, 'badge-blue', '→'
            chg = (v26 - v25) / v25 * 100
            return chg, ('badge-green' if chg >= 0 else 'badge-red'), ('▲' if chg >= 0 else '▼')

        chg_pay, col_pay, arr_pay = yoy_badge(avg_pay_25, avg_pay_26)
        chg_con, col_con, arr_con = yoy_badge(avg_con_25, avg_con_26)

        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.markdown(f"""
<div class='metric-card card-blue' style='padding:18px 20px;'>
    <div class='metric-label'>Avg Payment 2025</div>
    <div class='metric-value' style='font-size:22px;'>${avg_pay_25:,.0f}</div>
    <div class='metric-sub'>Across top CPT codes</div>
</div>""", unsafe_allow_html=True)
        with mc2:
            st.markdown(f"""
<div class='metric-card card-blue' style='padding:18px 20px;'>
    <div class='metric-label'>Avg Payment 2026</div>
    <div class='metric-value' style='font-size:22px;'>${avg_pay_26:,.0f}</div>
    <span class='badge {col_pay}'>{arr_pay} {chg_pay:+.1f}% YoY</span>
</div>""", unsafe_allow_html=True)
        with mc3:
            st.markdown(f"""
<div class='metric-card card-amber' style='padding:18px 20px;'>
    <div class='metric-label'>Avg Contract Rate 2025</div>
    <div class='metric-value' style='font-size:22px;'>${avg_con_25:,.0f}</div>
    <div class='metric-sub'>Across top CPT codes</div>
</div>""", unsafe_allow_html=True)
        with mc4:
            st.markdown(f"""
<div class='metric-card card-amber' style='padding:18px 20px;'>
    <div class='metric-label'>Avg Contract Rate 2026</div>
    <div class='metric-value' style='font-size:22px;'>${avg_con_26:,.0f}</div>
    <span class='badge {col_con}'>{arr_con} {chg_con:+.1f}% YoY</span>
</div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# ── Variance Distribution + Provider Deep-Dive
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-header'>Variance &amp; Contract Analysis</div>", unsafe_allow_html=True)
col_var, col_doc = st.columns([2, 3])

with col_var:
    if 'Variance' in filtered.columns:
        var_counts = filtered['Variance'].value_counts().reset_index()
        var_counts.columns = ['Status', 'Count']
        VAR_COLORS = {
            'Less Than Contract':      '#dc2626',
            'More than Contract':      '#059669',
            'Matched':                 '#2563eb',
            'No Contract vs Payment':  '#94a3b8'
        }
        colors = [VAR_COLORS.get(s, '#94a3b8') for s in var_counts['Status']]
        total_var = var_counts['Count'].sum()

        fig6 = go.Figure(go.Bar(
            x=var_counts['Count'],
            y=var_counts['Status'],
            orientation='h',
            marker_color=colors, marker_line_width=0,
            text=[f'{c:,}  ({c/total_var*100:.1f}%)' for c in var_counts['Count']],
            textposition='outside',
            textfont=dict(color='#64748b', size=10),
            hovertemplate='<b>%{y}</b><br>Count: %{x:,}<extra></extra>'
        ))
        fig6.update_layout(**PLOTLY_BASE,
            title=dict(text='Variance Status Distribution', font=TITLE_FONT),
            height=280,
            margin=dict(l=14, r=100, t=42, b=14),
        )
        st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar': False})

with col_doc:
    if 'Doctor' in filtered.columns:
        doc_grp = filtered.groupby('Doctor').agg(
            Total=('Total_Payment', 'sum'),
            Allowed=('Allowed_Contract_Num', 'sum'),
            Claims=('Total_Payment', 'count')
        ).reset_index()
        doc_grp['Under'] = (doc_grp['Allowed'] - doc_grp['Total']).clip(lower=0)
        doc_grp = doc_grp.sort_values('Under', ascending=False).head(8)

        fig7 = go.Figure()
        fig7.add_trace(go.Bar(
            name='Actual Payment', x=doc_grp['Doctor'], y=doc_grp['Total'] / 1e3,
            marker_color='#2563eb', opacity=0.9, marker_line_width=0,
            hovertemplate='<b>%{x}</b><br>Actual: $%{y:,.1f}K<extra></extra>'
        ))
        fig7.add_trace(go.Bar(
            name='Contract Allowed', x=doc_grp['Doctor'], y=doc_grp['Allowed'] / 1e3,
            marker_color='#fca5a5', opacity=0.9, marker_line_width=0,
            hovertemplate='<b>%{x}</b><br>Allowed: $%{y:,.1f}K<extra></extra>'
        ))
        fig7.update_layout(**PLOTLY_BASE,
            legend=LEGEND,
            title=dict(text='Top 8 Providers — Actual vs Contract Allowed ($K)', font=TITLE_FONT),
            barmode='group', height=280,
            yaxis_tickprefix='$', yaxis_ticksuffix='K',
            bargap=0.25, bargroupgap=0.06
        )
        st.plotly_chart(fig7, use_container_width=True, config={'displayModeBar': False})


# ═══════════════════════════════════════════════════════════════════════════
# ── Detailed Records Table
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-header'>Detailed Records</div>", unsafe_allow_html=True)

show_cols = [c for c in [
    'Ticket_Number', 'service_date', 'Insurance_Carrier', 'Doctor',
    'code', 'Modifier', 'CPT_Category', 'Doctor_Speciality',
    'Total_Payment', 'Allowed Contract', 'Variance', 'Variance Amount'
] if c in filtered.columns]

table_df = filtered[show_cols].copy()

search_col, count_col = st.columns([4, 1])
with search_col:
    search = st.text_input(
        "Search records",
        placeholder="🔍  Search across ticket #, doctor, CPT code, carrier…",
        label_visibility="collapsed",
        key="records_search"
    )
with count_col:
    st.markdown(f"""
        <div style='background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px;
                    padding:9px 14px; text-align:center; margin-top:2px;'>
            <div style='font-size:9px; color:#94a3b8; font-weight:700; letter-spacing:1px;
                        text-transform:uppercase; font-family:Outfit,sans-serif;'>Records</div>
            <div style='font-size:18px; font-weight:800; color:#0f172a;
                        font-family:DM Mono,monospace; line-height:1.2;'>{len(table_df):,}</div>
        </div>
    """, unsafe_allow_html=True)

if search:
    mask_search = table_df.astype(str).apply(
        lambda col: col.str.contains(search, case=False, na=False)
    ).any(axis=1)
    table_df = table_df[mask_search]

st.dataframe(table_df.head(500), use_container_width=True, height=340)

st.markdown(
    f"<div style='font-size:11px; color:#94a3b8; text-align:right; margin-top:6px; "
    f"font-weight:500; font-family:DM Sans,sans-serif;'>"
    f"Showing up to 500 of <strong style='color:#475569;'>{len(table_df):,}</strong> matching rows "
    f"(of <strong style='color:#475569;'>{len(filtered):,}</strong> filtered)</div>",
    unsafe_allow_html=True
)

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown("""
    <div style='margin-top:32px; padding:18px 0 8px 0; border-top:1px solid #e2e8f0;
                display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;'>
        <div style='font-size:11px; color:#94a3b8; font-weight:500;'>
            ⚕ <strong style='color:#475569;'>Jorie AI</strong> &nbsp;·&nbsp;
            ONE AR &nbsp;·&nbsp; Contract Rate Variance Intelligence Platform
        </div>
        <div style='font-size:10px; color:#cbd5e1; font-weight:600; letter-spacing:0.8px;
                    text-transform:uppercase; font-family:Outfit,sans-serif;'>
            Payment Analysis Dashboard
        </div>
    </div>
""", unsafe_allow_html=True)
