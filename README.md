# Forecasting Financial Inclusion in Ethiopia

**10 Academy: Artificial Intelligence Mastery - Week 10 Challenge**

A forecasting system to track Ethiopia's digital financial transformation (2025-2027) using time series methods. This project analyzes drivers of financial inclusion—such as Telebirr's growth, M-Pesa's entry, and policy changes—to predict Access (Account Ownership) and Usage (Digital Payments) trends.

---

## 📊 Interim Submission Report (Task 1 & 2)

### 1. Data Enrichment Summary
We enriched the starter dataset (`ethiopia_fi_unified_data.csv`) to improve forecasting accuracy for the **Usage** pillar.
-   **Added Event**: *M-Pesa Ethiopia Launch* (Aug 16, 2023). This is a critical market driver for digital payments.
-   **Data Cleaning**: Averaged multiple conflicting 2021 values for `ACC_OWNERSHIP` to align with World Bank Findex baselines (46%).
-   **Total Records**: The enriched dataset now contains **44 records** (30 observations, 11 events, 3 targets).
-   **Documentation**: See `data_enrichment_log.md` for full details on sources and confidence levels.

### 2. Key Insights from EDA
Exploratory analysis revealed mixed progress in Ethiopia's financial landscape:
1.  **Account Ownership Stagnation**: Despite the launch of Telebirr and massive mobile money growth, reported *Account Ownership* only grew by +3pp (from 46% to 49%) between 2021 and 2024.
2.  **Infrastructure vs. Usage Gap**: While 4G coverage (`ACC_4G_COV`) and agent networks have expanded, active usage rates (`USG_ACTIVE_RATE`) remain a fraction of registered users.
3.  **Digital Payment Drivers**: Event analysis suggests that product launches (Telebirr, M-Pesa) correlate strongly with spikes in registered accounts, but the conversion to *active* financial inclusion is slower.
4.  **Sparse Data Reality**: Most indicators, such as `ACC_MOBILE_PEN` (Mobile Penetration) and `USG_ATM_VALUE`, have only 1-2 data points, necessitating robust modeling techniques for forecasting.
5.  **Target Gap**: Current growth trajectories suggest significant acceleration is needed to meet the National Financial Inclusion Strategy (NFIS) targets for 2026-2027.

### 3. Data Limitations
-   **Sparse Time Series**: Key indicators like *Mobile Penetration* and *ATM Usage* have extremely sparse coverage (often single data points), limiting the ability to run traditional lag-based regressions.
-   **Inconsistent Reporting**: Discrepancies between operator-reported figures (e.g., registered users) and survey-based Findex data (e.g., ownership rates) create "truth gaps" that models must account for.

---

## 📂 Project Structure

```text
ethiopia-fi-forecast/
├── data/
│   ├── raw/                      # Starter dataset & reference codes
│   └── processed/                # Enriched, analysis-ready data
├── notebooks/                    # Jupyter notebooks
│   ├── 01_data_exploration.ipynb # Initial exploration
│   └── task2_eda.ipynb           # Interim EDA Submission
├── src/                          # Source code
│   ├── enrich_data.py            # ETL and enrichment pipelines
│   └── analyze_insight.py        # Insight generation scripts
├── dashboard/                    # Interactive Streamlit/Dash app (Task 5)
│   └── app.py
├── models/                       # Predictive models (Task 3 & 4)
├── reports/                      # Generated figures and logs
│   └── figures/
├── data_enrichment_log.md        # Log of all data additions (Task 1)
└── requirements.txt              # Project dependencies
```

## 🚀 Getting Started

### Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Start-Tech-Academy/ethiopia-fi-forecast.git
    cd ethiopia-fi-forecast
    ```

2.  **Set up environment:**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

### Running the Pipeline
1.  **Enrich Data**: Run the enrichment script to generate `data/processed/ethiopia_fi_enriched_data.csv`.
    ```bash
    python src/enrich_data.py
    ```
2.  **Generate Insights**:
    ```bash
    python src/analyze_insight.py
    ```
3.  **View EDA**: Launch Jupyter Lab to view the Task 2 Notebook.
    ```bash
    jupyter lab notebooks/task2_eda.ipynb
    ```

### Streamlit dashboard

Run the dashboard locally (ensure dependencies in `requirements.txt` are installed):

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

The dashboard provides interactive views for trends, forecasts, and inclusion projections. Use the sidebar to switch scenarios and download forecast CSVs.

## 🛠️ Methodology

### Task 1: Data Exploration & Enrichment
We unified data from Findex surveys, NBE reports, and operator disclosures into a single schema. Additional events like the M-Pesa launch were manually curated and added to capture their "shock" effect on the ecosystem.

### Task 2: Exploratory Data Analysis (EDA)
We analyzed temporal trends and data quality. Visualizations (in `notebooks/task2_eda.ipynb`) focused on:
-   **Coverage Heatmaps**: Identifying years/indicators with missing data.
-   **Ownership Trajectories**: Comparing Ethiopia's 2014-2024 growth against regional peers.
-   **Event Overlays**: Plotting key policy changes (events) against indicator time series to visually assess impact.

## 🔮 Upcoming Tasks
-   **Task 3**: Event Impact Modeling (Quantifying the effect of policies/launches).
-   **Task 4**: Forecasting Access & Usage (2025-2027 scenarios).
-   **Task 5**: Interactive Dashboard Development.

## 🤝 Contributing
Contributions are welcome for the Final Submission. Please follow the `record_type` schema for any new data points.

