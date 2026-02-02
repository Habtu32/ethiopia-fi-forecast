import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'reports' / 'analysis_outputs'

st.set_page_config(page_title='Ethiopia FI Dashboard', layout='wide')

@st.cache_data
def load_forecast():
    fp = DATA_DIR / 'forecast_2025_2027_scenarios.csv'
    if not fp.exists():
        return pd.DataFrame()
    return pd.read_csv(fp)

@st.cache_data
def load_enriched():
    fp = ROOT / 'data' / 'processed' / 'ethiopia_fi_enriched_data.csv'
    if not fp.exists():
        return pd.DataFrame()
    return pd.read_csv(fp)

forecasts = load_forecast()
enriched = load_enriched()

st.title('Ethiopia Financial Inclusion — Dashboard')

# Sidebar controls
st.sidebar.header('Controls')
scenario = st.sidebar.selectbox('Scenario', options=sorted(forecasts['scenario'].unique()) if not forecasts.empty else ['base'], index=1 if ('base' in forecasts['scenario'].unique() if not forecasts.empty else False) else 0)
model_choice = st.sidebar.selectbox('Model for trend', ['Linear (default)'])
download_data = st.sidebar.checkbox('Show raw data download')

def _format_latest(df, indicator):
    if df.empty:
        return 'n/a'
    s = df[(df['indicator_code']==indicator) & (df['record_type']=='observation')]
    if s.empty:
        return 'n/a'
    v = pd.to_numeric(s['value_numeric'], errors='coerce').dropna()
    if v.empty:
        return 'n/a'
    return f"{v.iloc[-1]:.1f}%"

def _get_annual_mean(df, code):
    sub = df[(df['indicator_code']==code)&(df['record_type']=='observation')].copy()
    if sub.empty:
        return pd.Series()
    sub['observation_date'] = pd.to_datetime(sub['observation_date'], errors='coerce')
    sub['year'] = sub['observation_date'].dt.year.fillna(sub['fiscal_year']).astype('Int64')
    s = sub.groupby('year')['value_numeric'].mean()
    s.index = s.index.astype(int)
    return s

def _format_latest_usage(df):
    if df.empty:
        return 'n/a'
    try:
        acc = _get_annual_mean(df, 'ACC_MM_ACCOUNT')
        act = _get_annual_mean(df, 'USG_ACTIVE_RATE')
        if acc.empty or act.empty:
            return 'n/a'
        last_year = sorted(set(acc.index)&set(act.index))[-1]
        val = acc.loc[last_year] * act.loc[last_year] / 100.0
        return f"{val:.2f}%"
    except Exception:
        return 'n/a'

def _compute_p2p_atm_ratio(df):
    if df.empty:
        return 'n/a'
    p2p = _get_annual_mean(df, 'USG_P2P_COUNT')
    atm = _get_annual_mean(df, 'USG_ATM_COUNT')
    if atm.empty or p2p.empty:
        return 'n/a'
    y = sorted(set(p2p.index)&set(atm.index))[-1]
    if atm.loc[y]==0:
        return 'n/a'
    return f"{(p2p.loc[y]/atm.loc[y]):.2f}"

col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Latest Account Ownership (obs)', value=_format_latest(enriched, 'ACC_OWNERSHIP'))
with col2:
    st.metric('Latest Digital Usage (proxy)', value=_format_latest_usage(enriched))
with col3:
    st.metric('P2P/ATM Ratio', value=_compute_p2p_atm_ratio(enriched))

st.markdown('---')

with st.expander('Trends'):
    st.header('Time Series Explorer')
    years = st.slider('Select year range', 2010, 2030, (2014, 2027))
    indicator = st.selectbox('Indicator', ['ACC_OWNERSHIP','ACC_MM_ACCOUNT','USG_ACTIVE_RATE','USG_P2P_COUNT','USG_ATM_COUNT'])
    ts = _get_annual_mean(enriched, indicator)
    if not ts.empty:
        ts = ts[(ts.index>=years[0])&(ts.index<=years[1])]
        st.line_chart(ts)

with st.expander('Forecasts'):
    st.header('Forecast scenarios (2025–2027)')
    if forecasts.empty:
        st.info('No forecast file found.')
    else:
        sub = forecasts[forecasts['scenario']==scenario].set_index('year')
        st.line_chart(sub['acc_pred_mean'], use_container_width=True)
        st.line_chart(sub['usage_pred_mean'], use_container_width=True)
        st.download_button('Download forecast CSV', data=forecasts.to_csv(index=False), file_name='forecast_2025_2027_scenarios.csv')

with st.expander('Inclusion Projections'):
    st.header('Progress toward 60% account ownership target')
    if forecasts.empty:
        st.write('No forecast data')
    else:
        target = 60.0
        proj = forecasts[(forecasts['scenario']==scenario)][['year','acc_pred_mean']].drop_duplicates().set_index('year')
        fig, ax = plt.subplots()
        ax.plot(proj.index, proj['acc_pred_mean'], marker='o')
        ax.axhline(target, color='red', linestyle='--', label='60% target')
        ax.set_ylabel('Percent of adults')
        ax.set_title('Projected Account Ownership vs 60% target')
        ax.legend()
        st.pyplot(fig)

st.markdown('---')
st.write('Answers: The dashboard shows trends, event-augmented forecasts, and projections toward a 60% target. Use the scenario selector in the sidebar to switch scenarios.')
"""
Entry point for the forecasting dashboard.

This is a placeholder application; extend it with your preferred
web framework (e.g. Dash, Streamlit, or FastAPI + frontend).
"""

if __name__ == "__main__":
    print("Dashboard app placeholder. Implement your UI here.")

