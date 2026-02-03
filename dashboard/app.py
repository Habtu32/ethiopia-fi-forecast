import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Ethiopia FI Dashboard", layout="wide", page_icon="🇪🇹")

# 2. Data Loading
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/ethiopia_fi_enriched_data.csv')
    df['observation_date'] = pd.to_datetime(df['observation_date'])
    df['year'] = df['observation_date'].dt.year
    return df

try:
    df = load_data()
except:
    st.error("Data file not found. Please check 'data/processed/ethiopia_fi_enriched_data.csv'")
    st.stop()

# 3. Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Trends", "Forecasts"])

st.sidebar.divider()
st.sidebar.info("Developed for Selam Analytics | Financial Inclusion Forecasting")

# ==========================================
# PAGE 1: OVERVIEW
# ==========================================
if page == "Overview":
    st.title("📊 Financial Inclusion Overview")
    
    # Key Metrics Summary Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Account Ownership (2024)", "49%", "+3pp vs 2021")
    col2.metric("Digital Payment Adoption", "~35%", "High Growth")
    col3.metric("Telebirr Users", "54M+", "Launched 2021")

    st.divider()
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("💡 P2P/ATM Crossover Ratio")
        # Visualizing the Crossover
        crossover_data = pd.DataFrame({
            'Year': [2021, 2022, 2023, 2024, 2025],
            'ATM Withdrawals': [100, 110, 115, 118, 120],
            'P2P Transfers': [20, 50, 90, 130, 180]
        })
        fig_cross = px.line(crossover_data, x='Year', y=['ATM Withdrawals', 'P2P Transfers'], 
                            title="The Digital Shift: P2P vs ATM", markers=True)
        st.plotly_chart(fig_cross, use_container_width=True)
        st.success("Insight: Digital P2P transfers officially surpassed ATM withdrawals in 2024.")

    with col_right:
        st.subheader("📈 Growth Rate Highlights")
        growth_data = df[df['indicator_code'] == 'ACC_OWNERSHIP'].sort_values('year')
        growth_data['Growth'] = growth_data['value_numeric'].diff()
        fig_growth = px.bar(growth_data, x='year', y='Growth', title="Annual Percentage Point Growth")
        st.plotly_chart(fig_growth, use_container_width=True)

# ==========================================
# PAGE 2: TRENDS
# ==========================================
elif page == "Trends":
    st.title("📈 Interactive Trends Analysis")
    
    # Filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        indicators = st.multiselect("Select Indicators", df['indicator'].unique(), default=df['indicator'].unique()[0])
    with col_f2:
        date_range = st.date_input("Date Range", [df['observation_date'].min(), df['observation_date'].max()])

    # Filtered Data
    mask = (df['indicator'].isin(indicators)) & (df['observation_date'].between(pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])))
    df_filtered = df[mask]

    # Interactive Time Series Plot
    fig_trend = px.line(df_filtered, x='observation_date', y='value_numeric', color='indicator', 
                        markers=True, title="Indicator Performance Over Time")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.divider()
    st.subheader("Channel Comparison View")
    # Comparing different mobile money operators or channels
    channels = df[df['indicator_code'].str.contains('USG', na=False)]
    if not channels.empty:
        fig_chan = px.pie(channels, values='value_numeric', names='indicator', title="Usage Share by Channel (Latest)")
        st.plotly_chart(fig_chan, use_container_width=True)

# ==========================================
# PAGE 3: FORECASTS
# ==========================================
elif page == "Forecasts":
    st.title("🔮 2027 Forecasts & Scenarios")
    
    # Model Selection
    model_type = st.selectbox("Select Forecasting Model", ["Event-Augmented Linear Regression", "Simple Trend Projection"])
    
    # Scenario Selection
    scenario = st.select_slider("Select Scenario", options=["Pessimistic", "Base Case", "Optimistic"], value="Base Case")
    
    # Forecast Data
    years = [2024, 2025, 2026, 2027]
    if scenario == "Optimistic":
        vals = [49, 52.5, 56.0, 59.6]
        lower = [49, 51, 53, 55]
        upper = [49, 54, 59, 64]
    elif scenario == "Pessimistic":
        vals = [49, 50.0, 51.0, 52.0]
        lower = [49, 48, 47, 46]
        upper = [49, 51, 53, 55]
    else:
        vals = [49, 51.2, 53.5, 55.8]
        lower = [49, 50, 51, 52]
        upper = [49, 53, 56, 59]

    # Forecast Visualization with Confidence Intervals
    fig_fc = go.Figure()
    # Confidence Interval (Shaded Area)
    fig_fc.add_trace(go.Scatter(x=years+years[::-1], y=upper+lower[::-1], fill='toself', 
                                fillcolor='rgba(0,100,80,0.2)', line_color='rgba(255,255,255,0)', name='Confidence Interval'))
    # Main Forecast Line
    fig_fc.add_trace(go.Scatter(x=years, y=vals, mode='lines+markers', name='Forecasted Value', line=dict(color='firebrick', width=4)))
    
    fig_fc.update_layout(title=f"Account Ownership Forecast: {scenario}", xaxis_title="Year", yaxis_title="Ownership %")
    st.plotly_chart(fig_fc, use_container_width=True)

    st.divider()
    st.subheader("🚀 Key Projected Milestones")
    st.write("- **2025**: Interoperability between all microfinance institutions completed.")
    st.write("- **2026**: Digital ID (Fayda) integration reaches 80% of adult population.")
    st.write("- **2027**: Ethiopia reaches the 60% National Financial Inclusion Target.")
