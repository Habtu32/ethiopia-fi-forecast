# Forecasting Financial Inclusion in Ethiopia — Final Submission

This repository contains the **final, complete deliverable** for the **10 Academy – Week 10 Challenge**:
**Forecasting Financial Inclusion in Ethiopia using Time Series and Event-Impact Analysis**.

The project applies a **data-driven, evidence-based methodology** to analyze historical trends, quantify the impact of major fintech and policy events, and forecast **Account Ownership and Usage** outcomes for **2025–2027**.

---

## Project Scope and Objective

The primary objective of this project is to:

* Analyze Ethiopia’s financial inclusion trajectory using structured historical data
* Quantify the **impact of key market and policy events** (e.g., Telebirr, M-Pesa launches)
* Produce **scenario-based forecasts** (baseline, optimistic, conservative) for future adoption and usage
* Provide transparent, reproducible outputs suitable for **policy analysis and decision support**

---

## Contents of This Final Commit

This commit represents the **final evaluated submission** and includes all required outputs.

### 📊 Data & Outputs

* **Enriched dataset**
  `data/processed/ethiopia_fi_enriched_data.csv`
  Final cleaned dataset with manual event annotations and normalized indicators.

* **Forecast scenarios (2025–2027)**
  `reports/analysis_outputs/forecast_2025_2027_scenarios.csv`

* **Impact association matrix**
  `reports/analysis_outputs/impact_association_matrix.csv`

* **Validation metrics**
  `reports/analysis_outputs/prediction_validation_metrics.csv`

### 📄 Documentation

* **Impact modeling methodology**
  `reports/analysis_outputs/impact_methodology.md`

* **Key insights & interpretation**
  `reports/analysis_outputs/insights_financial_inclusion.md`

---

## Key Results and Insights

* Generated **Account Ownership and Usage forecasts** for 2025–2027 under three scenarios:

  * Baseline
  * Optimistic
  * Conservative

* Estimated **event-level impact magnitudes**, demonstrating how:

  * Mobile money launches
  * Regulatory shifts
  * Market expansion
    influence adoption and usage trends.

* Performed **model validation and correlation diagnostics** to assess forecast reliability and robustness.

---

## Repository Structure (Key Files)

```
data/
 └── processed/
     └── ethiopia_fi_enriched_data.csv

notebooks/
 └── Exploratory and modeling notebooks (reproducible analysis)

src/
 ├── enrich_data.py          # ETL and data enrichment pipeline
 └── analyze_insight.py      # Insight extraction and reporting logic

scripts/
 ├── run_impact_modeling.py  # Event-impact modeling runner
 └── validate_predictions.py# Forecast validation utilities

dashboard/
 └── app.py                  # Streamlit dashboard for scenario exploration

reports/
 └── analysis_outputs/
     ├── forecast_2025_2027_scenarios.csv
     ├── impact_association_matrix.csv
     ├── prediction_validation_metrics.csv
     ├── impact_methodology.md
     └── insights_financial_inclusion.md
```

---

## Quick Start (Local Reproduction)

### 1️⃣ Environment setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Data enrichment and analysis

```powershell
python src/enrich_data.py
python src/analyze_insight.py
```

### 3️⃣ Impact modeling and validation

```powershell
python scripts/run_impact_modeling.py
python scripts/validate_predictions.py
```

### 4️⃣ Optional: Launch interactive dashboard

```powershell
streamlit run dashboard/app.py
```

---

## Reproducibility and Transparency

* All **final CSV outputs** are included in `reports/analysis_outputs/` for immediate review.
* Full reproducibility is supported through the provided scripts and notebooks.
* **Data sources, assumptions, and manual event annotations** are documented in:

  * `data_enrichment_log.md`
  * `impact_methodology.md`

This ensures transparency and alignment with best practices in data science and policy analytics.

---

## Submission Status

✅ **Final version**
✅ **All required outputs included**
✅ **Ready for evaluation and grading**

---

## Contact & Next Steps

If further packaging is required (ZIP submission, slide deck, executive summary, or policy brief), the outputs in this repository are structured to support those formats directly.

---

**Thank you.**
This README reflects the
**final submission for the project evaluation**.