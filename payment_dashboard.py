import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


# ── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Payment Analysis Dashboard",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* ── Main background ── */
    .stApp {
        background: #f0f4f8;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
        box-shadow: 2px 0 12px rgba(0,0,0,0.06);
    }
    [data-testid="stSidebar"] * { color: #374151 !important; }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: #f8fafc !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 10px !important;
        color: #1e293b !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* ── KPI Cards ── */
    .metric-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 24px 26px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid rgba(255,255,255,0.8);
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 28px rgba(0,0,0,0.12);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        border-radius: 18px 18px 0 0;
    }
    .card-blue::before   { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
    .card-amber::before  { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .card-red::before    { background: linear-gradient(90deg, #ef4444, #f87171); }
    .card-green::before  { background: linear-gradient(90deg, #10b981, #34d399); }
    .card-violet::before { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }

    .metric-bg-icon {
        position: absolute;
        right: 18px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 48px;
        opacity: 0.07;
    }
    .metric-label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        color: #94a3b8;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 30px;
        font-weight: 800;
        color: #0f172a;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1;
        margin-bottom: 6px;
    }
    .metric-sub {
        font-size: 12px;
        color: #64748b;
        font-weight: 500;
    }
    .badge {
        display: inline-block;
        font-size: 10px;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 20px;
        letter-spacing: 0.4px;
        margin-top: 6px;
    }
    .badge-red   { background: #fee2e2; color: #ef4444; }
    .badge-green { background: #d1fae5; color: #10b981; }
    .badge-blue  { background: #dbeafe; color: #3b82f6; }
    .badge-amber { background: #fef3c7; color: #d97706; }

    /* ── Section Headers ── */
    .section-header {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        color: #94a3b8;
        margin: 32px 0 14px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-header::before {
        content: '';
        width: 3px;
        height: 14px;
        border-radius: 2px;
        background: linear-gradient(180deg, #3b82f6, #8b5cf6);
    }
    .section-header::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, #e2e8f0, transparent);
    }

    /* ── Page title ── */
    .dash-title {
        font-size: 24px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.5px;
    }
    .dash-subtitle {
        font-size: 13px;
        color: #64748b;
        margin-top: 3px;
        font-weight: 500;
    }

    /* ── Chart containers ── */
    .chart-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 6px 6px 0 6px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #f1f5f9;
    }

    /* ── Sidebar brand ── */
    .sidebar-brand {
        padding: 20px 0 22px 0;
    }
    .brand-logo {
        font-size: 22px;
        font-weight: 800;
        color: #0f172a !important;
        letter-spacing: -0.5px;
    }
    .brand-tag {
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        color: #94a3b8 !important;
        margin-top: 2px;
    }
    .sidebar-label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: #94a3b8 !important;
        margin-bottom: 4px;
        margin-top: 14px;
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    [data-testid="stToolbar"] { display: none !important; }
    header { background: transparent !important; }

    /* Force sidebar always open, hide the close X inside it */
    [data-testid="stSidebar"] {
        min-width: 244px !important;
        max-width: 244px !important;
        transform: none !important;
        visibility: visible !important;
    }
    [data-testid="stSidebar"] button[kind="header"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="baseButton-headerNoPadding"] {
        display: none !important;
    }
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)


# ── Load Data ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    file2 = r"C:\Users\KunalVaish\OneDrive - Jorie AI\Cartage\Final Reports_Carthage\Carthage_AR_Documents\Contract Rate Mapping\Mapped_Output.csv"
    try:
        
        df = pd.read_csv(file2, low_memory=False, dtype={
            'Ticket_Number': str,
            'cpt DUP': str,
            'Variance Amount': str,
            'Allowed Contract': str,
            '50% Contract': str,
})
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

df, error = load_data()


# ── Shared Plotly theme (LIGHT) ────────────────────────────────────────────
PLOTLY_BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Plus Jakarta Sans', color='#64748b', size=11),
    margin=dict(l=12, r=12, t=38, b=12),
    xaxis=dict(gridcolor='#f1f5f9', zeroline=False, tickfont=dict(color='#94a3b8', size=10), linecolor='#e2e8f0'),
    yaxis=dict(gridcolor='#f1f5f9', zeroline=False, tickfont=dict(color='#94a3b8', size=10), linecolor='#e2e8f0'),
)
LEGEND = dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#64748b', size=11), borderwidth=0)
TITLE_FONT = dict(color='#1e293b', size=13, family='Plus Jakarta Sans')

PALETTE = ['#3b82f6','#ef4444','#8b5cf6','#f59e0b','#10b981','#ec4899','#06b6d4','#f97316']
PALETTE_BLUE = ['#1d4ed8','#2563eb','#3b82f6','#60a5fa','#93c5fd','#bfdbfe','#dbeafe','#eff6ff']


# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class='sidebar-brand'>
            <div class='brand-logo'>⚕ Jorie AI</div>
            <div class='brand-tag'>Payment Analytics</div>
        </div>
        <hr style='border:none; border-top:1.5px solid #f1f5f9; margin-bottom:18px;'>
    """, unsafe_allow_html=True)

    if df is not None:
        # Year options
        year_options = ['All'] + sorted(df['Year'].dropna().unique().astype(int).tolist(), reverse=True)

        # Month options sorted chronologically newest first
        _month_dates  = df['Date_Of_Entry'].dropna().dt.to_period('M').drop_duplicates()
        month_options = ['All'] + [p.strftime('%b-%y') for p in sorted(_month_dates, reverse=True)]

        carrier_options  = ['All'] + sorted(df['Insurance_Carrier'].dropna().unique().tolist()) if 'Insurance_Carrier' in df.columns else ['All']
        variance_options = ['All'] + sorted(df['Variance'].dropna().unique().tolist())           if 'Variance'          in df.columns else ['All']
        fc_options       = ['All'] + sorted(df['Update_FC'].dropna().unique().tolist())          if 'Update_FC'         in df.columns else ['All']
        cpt_options      = ['All'] + sorted(df['CPT_Category'].dropna().unique().tolist())       if 'CPT_Category'      in df.columns else ['All']

        st.markdown("<div class='sidebar-label'>Year</div>", unsafe_allow_html=True)
        selected_year = st.multiselect("Year", year_options[1:], default=[], key="year", placeholder="All", label_visibility="collapsed")

        st.markdown("<div class='sidebar-label'>Month</div>", unsafe_allow_html=True)
        selected_month = st.multiselect("Month", month_options[1:], default=[], key="month", placeholder="All", label_visibility="collapsed")

        st.markdown("<div class='sidebar-label'>Insurance Carrier</div>", unsafe_allow_html=True)
        selected_carrier = st.multiselect("Carrier", carrier_options[1:], default=[], key="carrier", placeholder="All", label_visibility="collapsed")

        st.markdown("<div class='sidebar-label'>Variance Status</div>", unsafe_allow_html=True)
        selected_variance = st.multiselect("Variance", variance_options[1:], default=[], key="variance", placeholder="All", label_visibility="collapsed")

        st.markdown("<div class='sidebar-label'>Financial Class</div>", unsafe_allow_html=True)
        selected_fc = st.multiselect("Financial Class", fc_options[1:], default=[], key="fc", placeholder="All", label_visibility="collapsed")

        st.markdown("<div class='sidebar-label'>CPT Category</div>", unsafe_allow_html=True)
        selected_cpt = st.multiselect("CPT Category", cpt_options[1:], default=[], key="cpt", placeholder="All", label_visibility="collapsed")

        code_options = sorted(df['code'].dropna().astype(str).unique().tolist()) if 'code' in df.columns else []
        st.markdown("<div class='sidebar-label'>CPT Code</div>", unsafe_allow_html=True)
        selected_code = st.multiselect("CPT Code", code_options, default=[], key="cpt_code", placeholder="All", label_visibility="collapsed")

    else:
        selected_year = selected_month = selected_carrier = selected_variance = selected_fc = selected_cpt = selected_code = []

    st.markdown("<hr style='border:none; border-top:1.5px solid #f1f5f9; margin-top:28px;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px; color:#cbd5e1; text-align:center; padding-top:8px; font-weight:600; letter-spacing:0.8px;'>ONE AR · JORIE AI</div>", unsafe_allow_html=True)


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
under_payment_count = under_mask.sum()
over_payment_count  = over_mask.sum()

# KPI cards — Mapped Contract rows where available, else all filtered rows
mapped_mask    = filtered['Categories'] == 'Mapped Contract'
mapped_df      = filtered[mapped_mask] if mapped_mask.sum() > 0 else filtered

mapped_under   = mapped_df[mapped_df['Total_Payment'] < mapped_df['Allowed_Contract_Num']]
mapped_over    = mapped_df[mapped_df['Total_Payment'] > mapped_df['Allowed_Contract_Num']]
mapped_allowed = mapped_df['Allowed_Contract_Num'].sum()
mapped_actual  = mapped_df['Total_Payment'].sum()

under_payment_amt  = (mapped_under['Allowed_Contract_Num'] - mapped_under['Total_Payment']).sum()
over_payment_amt   = (mapped_over['Total_Payment'] - mapped_over['Allowed_Contract_Num']).sum()

pct_under          = (under_payment_amt / mapped_allowed * 100) if mapped_allowed > 0 else 0
under_pct_of_total = (under_payment_amt / mapped_allowed * 100) if mapped_allowed > 0 else 0
recovery_rate      = (mapped_actual / mapped_allowed * 100) if mapped_allowed > 0 else 0


# ═══════════════════════════════════════════════════════════════════════════
# ── Header
# ═══════════════════════════════════════════════════════════════════════════
col_title, col_logo = st.columns([10, 1])
with col_logo:
    st.markdown("""
        <div style='display:flex; justify-content:flex-end; align-items:center; padding-top:6px;'>
            <a href='https://github.com/kunalvaish49-cpu/VisualCode_UB-04' target='_blank' 
               style='text-decoration:none;'>
                <img src='https://raw.githubusercontent.com/kunalvaish49-cpu/VisualCode_UB-04/20be2ac615bd0074353bf7f7b9784af81e6cc040/Jorie%20AI%20Image.webp'
                     style='height:160px; width:auto; border-radius:10px; 
                            box-shadow:0 2px 10px rgba(0,0,0,0.12);'
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
    filter_badge = f"<span class='badge badge-blue'>{active_filters} filter{'s' if active_filters!=1 else ''} active</span>" if active_filters else ""
    st.markdown(f"""
        <div class='dash-title'>Payment Analysis &nbsp;·&nbsp; Under &amp; Over Payment Overview &nbsp;{filter_badge}</div>
        <div class='dash-subtitle'>ONE AR &nbsp;·&nbsp; Contract Rate Variance Intelligence &nbsp;·&nbsp; {total_procedures:,} procedures in view</div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# ── KPI Cards (5 cards)
# ═══════════════════════════════════════════════════════════════════════════
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class='metric-card card-blue'>
        <div class='metric-bg-icon'>💰</div>
        <div class='metric-label'>Total Payment</div>
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
        <div class='metric-label'>Under Payment $</div>
        <div class='metric-value'>${under_payment_amt/1e6:.2f}M</div>
        <div class='metric-sub'>{under_pct_of_total:.1f}% of total payment</div>
        <span class='badge badge-red'>Revenue at risk</span>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='metric-card card-green'>
        <div class='metric-bg-icon'>📈</div>
        <div class='metric-label'>Over Payment $</div>
        <div class='metric-value'>${over_payment_amt/1e6:.2f}M</div>
        <div class='metric-sub'>{len(mapped_over):,} over-paid claims</div>
        <span class='badge badge-green'>Potential refund exposure</span>
    </div>""", unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class='metric-card card-violet'>
        <div class='metric-bg-icon'>🎯</div>
        <div class='metric-label'>Collection Rate</div>
        <div class='metric-value'>{recovery_rate:.1f}%</div>
        <div class='metric-sub'>Actual vs contract allowed</div>
        <span class='badge badge-blue'>Contract utilization</span>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)


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
            chart_title = f"Actual vs Allowed — by Carrier ({', '.join(selected_fc)})"
        else:
            fc_grp = filtered.groupby('Update_FC').agg(
                Actual=('Total_Payment', 'sum'),
                Allowed=('Allowed_Contract_Num', 'sum')
            ).reset_index().sort_values('Actual', ascending=False).head(8)
            x_col = 'Update_FC'
            chart_title = 'Actual vs Allowed — by Financial Class'

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=fc_grp[x_col], y=fc_grp['Actual']/1e6,
            mode='lines+markers' if len(fc_grp) > 1 else 'markers', name='Actual Payment',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=9, color='#3b82f6', line=dict(color='#1d4ed8', width=2)),
            fill='tozeroy', fillcolor='rgba(59,130,246,0.06)'
        ))
        fig.add_trace(go.Scatter(
            x=fc_grp[x_col], y=fc_grp['Allowed']/1e6,
            mode='lines+markers' if len(fc_grp) > 1 else 'markers', name='Contract Allowed',
            line=dict(color='#f59e0b', width=2.5, dash='dot'),
            marker=dict(size=7, color='#f59e0b')
        ))
        fig.update_layout(**PLOTLY_BASE,
            legend=LEGEND,
            title=dict(text=chart_title, font=TITLE_FONT),
            yaxis_tickprefix='$', yaxis_ticksuffix='M', height=290
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
    fig2.add_trace(go.Bar(x=monthly['Month_Label'], y=monthly['Actual']/1e3,  name='Actual',  marker_color='#3b82f6', opacity=0.9, marker_line_width=0))
    fig2.add_trace(go.Bar(x=monthly['Month_Label'], y=monthly['Allowed']/1e3, name='Allowed', marker_color='#bfdbfe', opacity=0.9, marker_line_width=0))
    fig2.update_layout(**PLOTLY_BASE,
        legend=LEGEND,
        title=dict(text='Monthly Payment Trend ($K)', font=TITLE_FONT),
        barmode='group', height=290,
        yaxis_tickprefix='$', yaxis_ticksuffix='K',
        bargap=0.25, bargroupgap=0.08
    )
    st.plotly_chart(fig2, width='stretch', config={'displayModeBar': False})


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
            Under_Amt=('Allowed_Contract_Num', 'sum'),
            Claims=('Total_Payment', 'count'),
            Gap=('_gap', 'sum')
        ).reset_index()
        under_carrier = under_carrier.sort_values('Under_Amt', ascending=False).head(6)
        total_u = (filtered.loc[under_mask, 'Allowed_Contract_Num'] - filtered.loc[under_mask, 'Total_Payment']).sum()

        fig3 = go.Figure(go.Pie(
            labels=under_carrier['Insurance_Carrier'],
            values=under_carrier['Under_Amt'],
            hole=0.58,
            marker=dict(colors=PALETTE, line=dict(color='#ffffff', width=3)),
            textinfo='percent',
            textfont=dict(size=11),
            hovertemplate='<b>%{label}</b><br>Amount: $%{value:,.0f}<br>Share: %{percent}<extra></extra>'
        ))
        fig3.add_annotation(
            text=f'${total_u/1e3:.0f}K<br><span style="font-size:10px;color:#94a3b8">Gap</span>',
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color='#0f172a', family='JetBrains Mono')
        )
        fig3.update_layout(**PLOTLY_BASE,
            title=dict(text='Under Payment — Top Carriers', font=TITLE_FONT),
            height=310, showlegend=True,
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#64748b', size=10), orientation='v', x=1, y=0.5)
        )
        st.plotly_chart(fig3, width='stretch', config={'displayModeBar': False})

with col_proc:
    if 'code' in filtered.columns:
        _pu = filtered[mapped_mask & under_mask].copy() if mapped_mask.sum() > 0 else filtered[under_mask].copy()
        _pu['code'] = _pu['code'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
        _pu = _pu[_pu['code'].notna() & (_pu['code'] != '') & (_pu['code'] != 'nan')]
        _pu['_gap'] = (_pu['Allowed_Contract_Num'] - _pu['Total_Payment']).clip(lower=0)
        proc_under = _pu.groupby('code').agg(Under_Gap=('_gap', 'sum')).reset_index()
        proc_under = proc_under[proc_under['Under_Gap'] > 0]
        proc_under = proc_under.sort_values('Under_Gap', ascending=True).tail(8)

        fig_proc = go.Figure(go.Bar(
            x=proc_under['Under_Gap']/1e3,
            y=proc_under['code'].astype(str),
            orientation='h',
            marker=dict(
                color=proc_under['Under_Gap'],
                colorscale=[[0,'#dbeafe'],[0.5,'#60a5fa'],[1,'#1d4ed8']],
                showscale=False,
                line=dict(width=0)
            ),
            text=[f'${v/1e3:.1f}K' for v in proc_under['Under_Gap']],
            textposition='outside',
            textfont=dict(color='#64748b', size=10)
        ))
        fig_proc.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Plus Jakarta Sans', color='#64748b', size=11),
            margin=dict(l=12, r=60, t=38, b=12),
            title=dict(text='Under Payment Gap — Top Procedures', font=TITLE_FONT),
            height=310,
            xaxis=dict(
                gridcolor='#f1f5f9', zeroline=False,
                tickfont=dict(color='#94a3b8', size=10),
                linecolor='#e2e8f0',
                tickprefix='$', ticksuffix='K'
            ),
            yaxis=dict(
                gridcolor='#f1f5f9', zeroline=False,
                tickfont=dict(color='#94a3b8', size=10),
                linecolor='#e2e8f0',
                type='category'
            ),
        )
        st.plotly_chart(fig_proc, width='stretch', config={'displayModeBar': False})

with col_prov:
    if 'Doctor' in filtered.columns:
        # Use only Mapped Contract rows — same as KPIs
        _prov = filtered[mapped_mask & under_mask].copy() if mapped_mask.sum() > 0 else filtered[under_mask].copy()
        _prov['_gap'] = (_prov['Allowed_Contract_Num'] - _prov['Total_Payment']).clip(lower=0)
        prov_under = _prov.groupby('Doctor').agg(Under_Gap=('_gap', 'sum')).reset_index()
        prov_under = prov_under[prov_under['Under_Gap'] > 0]
        prov_under = prov_under.sort_values('Under_Gap', ascending=True).tail(8)
        prov_under['label'] = prov_under['Doctor'].str[:22]

        fig_prov = go.Figure(go.Bar(
            x=prov_under['Under_Gap']/1e3,
            y=prov_under['label'],
            orientation='h',
            marker=dict(
                color=prov_under['Under_Gap'],
                colorscale=[[0,'#fef3c7'],[0.5,'#fbbf24'],[1,'#d97706']],
                showscale=False,
                line=dict(width=0)
            ),
            text=[f'${v/1e3:.1f}K' for v in prov_under['Under_Gap']],
            textposition='outside',
            textfont=dict(color='#64748b', size=10)
        ))
        fig_prov.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Plus Jakarta Sans', color='#64748b', size=11),
            margin=dict(l=12, r=60, t=38, b=12),
            title=dict(text='Under Payment Gap — Top Providers', font=TITLE_FONT),
            height=310,
            xaxis=dict(
                gridcolor='#f1f5f9', zeroline=False,
                tickfont=dict(color='#94a3b8', size=10),
                linecolor='#e2e8f0',
                tickprefix='$', ticksuffix='K'
            ),
            yaxis=dict(
                gridcolor='#f1f5f9', zeroline=False,
                tickfont=dict(color='#94a3b8', size=10),
                linecolor='#e2e8f0',
                type='category'
            ),
        )
        st.plotly_chart(fig_prov, width='stretch', config={'displayModeBar': False})


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
        cat_grp['label'] = cat_grp['CPT_Category'].str[:22]

        fig5 = go.Figure(go.Bar(
            x=cat_grp['Under_Gap']/1e3,
            y=cat_grp['label'],
            orientation='h',
            marker=dict(
                color=cat_grp['Under_Gap'],
                colorscale=[[0,'#fce7f3'],[0.5,'#f472b6'],[1,'#db2777']],
                showscale=False,
                line=dict(width=0)
            ),
            text=[f'${v/1e3:.1f}K' for v in cat_grp['Under_Gap']],
            textposition='outside',
            textfont=dict(color='#64748b', size=10)
        ))
        fig5.update_layout(**PLOTLY_BASE,
            title=dict(text='Under Payment — Top 5 CPT Categories', font=TITLE_FONT),
            height=300,
            xaxis_tickprefix='$', xaxis_ticksuffix='K',
        )
        st.plotly_chart(fig5, width='stretch', config={'displayModeBar': False})

with col_cpt:
    if 'code' in filtered.columns:
        _cpt_filtered = filtered.copy()
        _cpt_filtered['code'] = _cpt_filtered['code'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
        _cpt_filtered = _cpt_filtered[_cpt_filtered['code'].notna() & (_cpt_filtered['code'] != '') & (_cpt_filtered['code'] != 'nan')]
        cpt_grp = _cpt_filtered.groupby('code').agg(
            Actual=('Total_Payment', 'sum'),
            Allowed=('Allowed_Contract_Num', 'sum')
        ).reset_index().sort_values('Allowed', ascending=False).head(10)
        cpt_grp['code_str'] = cpt_grp['code']
        cpt_grp['Gap']      = (cpt_grp['Allowed'] - cpt_grp['Actual']).clip(lower=0)

        cpt_labels = cpt_grp['code_str'].tolist()

        fig_cpt = go.Figure()
        fig_cpt.add_trace(go.Bar(
            name='Actual Payment',
            x=cpt_labels, y=cpt_grp['Actual']/1e3,
            marker_color='#3b82f6', opacity=0.9, marker_line_width=0
        ))
        fig_cpt.add_trace(go.Bar(
            name='Contract Allowed',
            x=cpt_labels, y=cpt_grp['Allowed']/1e3,
            marker_color='#bfdbfe', opacity=0.9, marker_line_width=0
        ))
        fig_cpt.update_layout(**PLOTLY_BASE,
            legend=LEGEND,
            title=dict(text='Top 10 CPT Codes — Actual vs Contract Allowed ($K)', font=TITLE_FONT),
            barmode='group', height=300,
            yaxis_tickprefix='$', yaxis_ticksuffix='K',
            bargap=0.22, bargroupgap=0.06,
            xaxis_type='category',
            xaxis_tickangle=-35,
        )
        st.plotly_chart(fig_cpt, width='stretch', config={'displayModeBar': False})

# ═══════════════════════════════════════════════════════════════════════════
# ── Procedure Contract Rate vs Year (2025 vs 2026) — Avg Payment & Contract
# ═══════════════════════════════════════════════════════════════════════════
if 'code' in filtered.columns and 'Year' in filtered.columns:
    _code_label = ', '.join(selected_code) if selected_code else 'All'
    _yoy_title = f"CPT {_code_label} — Avg Payment &amp; Contract Rate (2025 vs 2026)" if selected_code else "Procedure Contract Rate vs Year — Avg Payment &amp; Avg Contract Rate (2025 vs 2026)"
    st.markdown(f"<div class='section-header'>{_yoy_title}</div>", unsafe_allow_html=True)

    mapped_yr = filtered[filtered['Categories'] == 'Mapped Contract'] if 'Categories' in filtered.columns and (filtered['Categories'] == 'Mapped Contract').sum() > 0 else filtered

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
        Avg_Payment=('Total_Payment',        'mean'),
        Avg_Contract=('Allowed_Contract_Num','mean'),
        Count=('Total_Payment',              'count')
    ).reset_index()

    years_present   = sorted(yr_grp['Year'].dropna().unique().astype(int).tolist())
    colors_pay      = {2025: '#3b82f6', 2026: '#1d4ed8'}
    colors_contract = {2025: '#fbbf24', 2026: '#d97706'}

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
            ))
        fig_yr1.update_layout(**PLOTLY_BASE,
            legend=LEGEND,
            title=dict(text='Avg Actual Payment per CPT \u2014 2025 vs 2026', font=TITLE_FONT),
            barmode='group', height=340,
            yaxis_tickprefix='$',
            bargap=0.25, bargroupgap=0.08,
            xaxis_type='category', xaxis_tickangle=-35,
        )
        st.plotly_chart(fig_yr1, width='stretch', config={'displayModeBar': False})

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
            ))
        fig_yr2.update_layout(**PLOTLY_BASE,
            legend=LEGEND,
            title=dict(text='Avg Contract Rate per CPT \u2014 2025 vs 2026', font=TITLE_FONT),
            barmode='group', height=340,
            yaxis_tickprefix='$',
            bargap=0.25, bargroupgap=0.08,
            xaxis_type='category', xaxis_tickangle=-35,
        )
        st.plotly_chart(fig_yr2, width='stretch', config={'displayModeBar': False})

    if 2025 in years_present and 2026 in years_present:
        avg_pay_25 = yr_grp[yr_grp['Year'] == 2025]['Avg_Payment'].mean()
        avg_pay_26 = yr_grp[yr_grp['Year'] == 2026]['Avg_Payment'].mean()
        avg_con_25 = yr_grp[yr_grp['Year'] == 2025]['Avg_Contract'].mean()
        avg_con_26 = yr_grp[yr_grp['Year'] == 2026]['Avg_Contract'].mean()

        def yoy_badge(v25, v26):
            if v25 == 0:
                return 0.0, 'badge-blue', '\u2192'
            chg = (v26 - v25) / v25 * 100
            return chg, ('badge-green' if chg >= 0 else 'badge-red'), ('\u25b2' if chg >= 0 else '\u25bc')

        chg_pay, col_pay, arr_pay = yoy_badge(avg_pay_25, avg_pay_26)
        chg_con, col_con, arr_con = yoy_badge(avg_con_25, avg_con_26)

        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.markdown(f"""
<div class='metric-card card-blue' style='padding:18px 22px;'>
    <div class='metric-label'>Avg Payment 2025</div>
    <div class='metric-value' style='font-size:22px;'>${avg_pay_25:,.0f}</div>
    <div class='metric-sub'>Across top CPT codes</div>
</div>""", unsafe_allow_html=True)
        with mc2:
            st.markdown(f"""
<div class='metric-card card-blue' style='padding:18px 22px;'>
    <div class='metric-label'>Avg Payment 2026</div>
    <div class='metric-value' style='font-size:22px;'>${avg_pay_26:,.0f}</div>
    <span class='badge {col_pay}'>{arr_pay} {chg_pay:+.1f}% YoY</span>
</div>""", unsafe_allow_html=True)
        with mc3:
            st.markdown(f"""
<div class='metric-card card-amber' style='padding:18px 22px;'>
    <div class='metric-label'>Avg Contract Rate 2025</div>
    <div class='metric-value' style='font-size:22px;'>${avg_con_25:,.0f}</div>
    <div class='metric-sub'>Across top CPT codes</div>
</div>""", unsafe_allow_html=True)
        with mc4:
            st.markdown(f"""
<div class='metric-card card-amber' style='padding:18px 22px;'>
    <div class='metric-label'>Avg Contract Rate 2026</div>
    <div class='metric-value' style='font-size:22px;'>${avg_con_26:,.0f}</div>
    <span class='badge {col_con}'>{arr_con} {chg_con:+.1f}% YoY</span>
</div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)



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
            'Less Than Contract':      '#ef4444',
            'More than Contract':      '#10b981',
            'Matched':                 '#3b82f6',
            'No Contract vs Payment':  '#94a3b8'
        }
        colors = [VAR_COLORS.get(s, '#94a3b8') for s in var_counts['Status']]
        fig6 = go.Figure(go.Bar(
            x=var_counts['Count'],
            y=var_counts['Status'],
            orientation='h',
            marker_color=colors,
            marker_line_width=0,
            text=var_counts['Count'].apply(lambda x: f'{x:,}'),
            textposition='outside',
            textfont=dict(color='#64748b', size=11)
        ))
        fig6.update_layout(**PLOTLY_BASE,
            title=dict(text='Variance Status Distribution', font=TITLE_FONT),
            height=270,
        )
        st.plotly_chart(fig6, width='stretch', config={'displayModeBar': False})

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
        fig7.add_trace(go.Bar(name='Actual Payment', x=doc_grp['Doctor'], y=doc_grp['Total']/1e3,   marker_color='#3b82f6', opacity=0.9, marker_line_width=0))
        fig7.add_trace(go.Bar(name='Contract Allowed', x=doc_grp['Doctor'], y=doc_grp['Allowed']/1e3, marker_color='#fca5a5', opacity=0.9, marker_line_width=0))
        fig7.update_layout(**PLOTLY_BASE,
            legend=LEGEND,
            title=dict(text='Top 8 Providers — Actual vs Contract Allowed ($K)', font=TITLE_FONT),
            barmode='group', height=270,
            yaxis_tickprefix='$', yaxis_ticksuffix='K',
            bargap=0.25, bargroupgap=0.06
        )
        st.plotly_chart(fig7, width='stretch', config={'displayModeBar': False})


# ═══════════════════════════════════════════════════════════════════════════
# ── Detailed Records Table
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-header'>Detailed Records</div>", unsafe_allow_html=True)

show_cols = [c for c in [
    'Ticket_Number', 'service_date', 'carrier', 
    'code', 'Modifier', 'CPT_Category', 'Doctor_Speciality',
    'Total_Payment', 'Allowed Contract', 'Variance Amount', 'Variance','Doctor'
] if c in filtered.columns]

table_df = filtered[show_cols].copy()

search = st.text_input(
    "Search records",
    placeholder="Type to search across all columns (ticket #, doctor, CPT, carrier…)",
    label_visibility="collapsed",
    key="records_search"
)

if search:
    mask = table_df.astype(str).apply(
        lambda col: col.str.contains(search, case=False, na=False)
    ).any(axis=1)
    table_df = table_df[mask]

st.dataframe(table_df.head(500), use_container_width=True, height=330)

st.markdown(
    f"<div style='font-size:11px; color:#94a3b8; text-align:right; margin-top:6px; font-weight:500;'>"
    f"Showing up to 500 of <b>{len(table_df):,}</b> matching rows "
    f"(of {len(filtered):,} filtered)</div>",
    unsafe_allow_html=True
)
