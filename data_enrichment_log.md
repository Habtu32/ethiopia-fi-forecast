# Data Enrichment Log

**Based on:** `notebooks/01_data_exploration.ipynb`

---

## 1. Exploratory Data Analysis (EDA)

### Dataset Loaded
- **Main data:** 43 records (`ethiopia_fi_unified_data.csv`)
- **Impact links:** 14 records (`Impact_sheet.csv`)

### Record Type Distribution
| record_type | count |
|-------------|-------|
| observation | 30    |
| event       | 10    |
| target      | 3     |

### Pillar Coverage
| pillar     | count |
|-----------|-------|
| ACCESS    | 16    |
| USAGE     | 11    |
| GENDER    | 5     |
| AFFORDABILITY | 1  |

### Temporal Range
- **Start:** 2014  
- **End:** 2030  

---

## 2. Data Cleaning

### 2021 Access Data (ACC_OWNERSHIP)
Multiple values existed for 2021. Values were **averaged** to align with Findex baselines.

| observation_date | value_numeric |
|------------------|---------------|
| 2021-12-31       | 46.0          |

---

## 3. Enrichment: New Observation / Event

### Added Record

| Field            | Value |
|------------------|-------|
| **record_id**    | EVT_011 |
| **record_type**  | event |
| **category**     | product_launch |
| **indicator**    | M-Pesa Ethiopia Launch |
| **observation_date** | 2023-08-16 |
| **source_name**  | Safaricom Ethiopia |
| **source_url**   | https://www.safaricom.et |
| **confidence**   | high |
| **collected_by** | Student |
| **notes**        | Major market entry that drives digital payment usage. |

### Rationale
Adding the **M-Pesa Ethiopia Launch** event improves **Usage**-pillar forecasting by explicitly modeling the 2023 market entry as a driver of digital payment adoption.

---

## 4. Impact Links (Context)

Events are linked to indicators via `Impact_sheet.csv` (e.g. Telebirr Launch → ACC_OWNERSHIP, USG_TELEBIRR_USERS, USG_P2P_COUNT; Safaricom Commercial Launch → ACC_4G_COV, AFF_DATA_INCOME). The new EVT_011 can be linked similarly for M-Pesa-driven usage metrics when building impact models.

---

## 5. Output

- **Saved to:** `data/processed/ethiopia_fi_enriched_data.csv`  
- Enriched dataset includes original 43 rows plus the one new event row (44 total).
