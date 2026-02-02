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
    import streamlit as st
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go
    import matplotlib.pyplot as plt
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
    scenario = st.sidebar.selectbox('Scenario', options=sorted(forecasts['scenario'].unique()) if not forecasts.empty else ['base'], index=0)
    model_choice = st.sidebar.selectbox('Model for trend', ['Linear (default)'])
    download_data = st.sidebar.checkbox('Show raw data download')

    def _get_annual_mean(df, code):
        sub = df[(df['indicator_code']==code)&(df['record_type']=='observation')].copy()
        if sub.empty:
            return pd.Series()
        sub['observation_date'] = pd.to_datetime(sub['observation_date'], errors='coerce')
        sub['year'] = sub['observation_date'].dt.year.fillna(sub['fiscal_year']).astype('Int64')
        s = pd.to_numeric(sub['value_numeric'], errors='coerce').groupby(sub['year']).mean()
        s.index = s.index.astype(int)
        return s.sort_index()

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

    def _format_latest_usage(df):
        if df.empty:
            return 'n/a'
        try:
            acc = _get_annual_mean(df, 'ACC_MM_ACCOUNT')
            act = _get_annual_mean(df, 'USG_ACTIVE_RATE')
            common = sorted(set(acc.index)&set(act.index))
            if not common:
                return 'n/a'
            last_year = common[-1]
            val = acc.loc[last_year] * act.loc[last_year] / 100.0
            return f"{val:.2f}%"
        except Exception:
            return 'n/a'

    def _compute_p2p_atm_ratio(df):
        if df.empty:
            return 'n/a'
        p2p = _get_annual_mean(df, 'USG_P2P_COUNT')
        atm = _get_annual_mean(df, 'USG_ATM_COUNT')
        common = sorted(set(p2p.index)&set(atm.index))
        if not common:
            return 'n/a'
        y = common[-1]
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

    st.subheader('Trends — Time Series Explorer')
    left, right = st.columns([3,2])
    with left:
        years = st.slider('Select year range', 2010, 2030, (2014, 2027))
        indicator = st.selectbox('Indicator', ['ACC_OWNERSHIP','ACC_MM_ACCOUNT','USG_ACTIVE_RATE','USG_P2P_COUNT','USG_ATM_COUNT'])
        ts = _get_annual_mean(enriched, indicator)
        if not ts.empty:
            ts = ts[(ts.index>=years[0])&(ts.index<=years[1])]
            fig = px.line(x=ts.index, y=ts.values, labels={'x':'Year','y':indicator}, title=f'{indicator} over time')
            st.plotly_chart(fig, use_container_width=True)
    with right:
        st.markdown('**Channel comparison**')
        acc_mm = _get_annual_mean(enriched, 'ACC_MM_ACCOUNT')
        acc_own = _get_annual_mean(enriched, 'ACC_OWNERSHIP')
        combined = pd.DataFrame({'acc_mm': acc_mm, 'acc_own': acc_own}).dropna()
        if not combined.empty:
            fig2 = px.line(combined, x=combined.index, y=['acc_mm','acc_own'], labels={'value':'Percent','index':'Year'}, title='Accounts (registered) vs Account Ownership')
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown('---')

    st.subheader('Forecasts (2025–2027)')
    if forecasts.empty:
        st.info('No forecast file found.')
    else:
        sc = scenario
        sub = forecasts[forecasts['scenario']==sc].set_index('year')
        figf = go.Figure()
        figf.add_trace(go.Scatter(x=sub.index, y=sub['acc_pred_mean'], mode='lines+markers', name='Account (mean)', line=dict(color='royalblue')))
        if 'acc_ci_low' in sub.columns and 'acc_ci_high' in sub.columns:
            figf.add_trace(go.Scatter(x=sub.index, y=sub['acc_ci_low'], fill=None, mode='lines', line=dict(color='lightblue'), showlegend=False))
            figf.add_trace(go.Scatter(x=sub.index, y=sub['acc_ci_high'], fill='tonexty', mode='lines', line=dict(color='lightblue'), name='95% CI'))
        figf.update_layout(title='Account Ownership Forecast', xaxis_title='Year', yaxis_title='Percent of adults')
        st.plotly_chart(figf, use_container_width=True)
        # usage
        if 'usage_pred_mean' in sub.columns:
            figu = px.line(sub.reset_index(), x='year', y='usage_pred_mean', title='Usage (proxy) forecast', labels={'usage_pred_mean':'Percent of adults','year':'Year'})
            st.plotly_chart(figu, use_container_width=True)
        st.download_button('Download forecast CSV', data=forecasts.to_csv(index=False), file_name='forecast_2025_2027_scenarios.csv')

    st.markdown('---')

    st.subheader('Growth-rate heatmap')
    indicators = ['ACC_OWNERSHIP','ACC_MM_ACCOUNT','USG_ACTIVE_RATE']
    growth = {}
    for ind in indicators:
        s = _get_annual_mean(enriched, ind)
        if s.empty:
            continue
        growth[ind] = s.pct_change().fillna(0) * 100
    if growth:
        gdf = pd.DataFrame(growth).T
        gdf = gdf.sort_index()
        # ensure columns are strings for Plotly
        gdf.columns = gdf.columns.astype(str)
        fig_h = px.imshow(gdf, labels=dict(x='Year', y='Indicator', color='Growth %'), x=gdf.columns, y=gdf.index, aspect='auto', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_h, use_container_width=True)

    st.markdown('---')
    st.caption('Use the scenario selector to switch forecasts. Data download available in Forecasts panel.')

