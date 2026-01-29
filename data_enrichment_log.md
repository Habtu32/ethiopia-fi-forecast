# Data Enrichment Log

## Summary of Additions
**Date:** 2026-01-29
**Enriched By:** Antigravity

Added key 2025 observations for mobile money adoption to supplement the starter dataset.

## New Observations

| ID | Indicator | Value | Date | Source | Notes |
|----|-----------|-------|------|--------|-------|
| REC_NEW_001 | Total Mobile Money Accounts (Supply Side) | 136,000,000 | 2025-12-31 | NBE / BirrMetrics | Supply-side metric showing massive account proliferation compared to Findex ownership rates. |
| REC_NEW_002 | M-Pesa 90-Day Active Users | 11,150,000 | 2025-11-30 | Safaricom / TechWeez | Updates the Dec 2024 figure (7.1M) showing continued strong growth. |

## Rationale
- **Supply vs Demand Gap:** Adding usage/supply-side data (`ACC_MM_SUPPLY`) helps contrast with Findex demand-side data (`ACC_OWNERSHIP`), highlighting the "registered vs active" gap.
- **Recent Trends:** The 2025 M-Pesa data is crucial for accurate forecasting of Usage growth in the most recent period.

## Data Quality
- High confidence in Safaricom reported figures.
- NBE aggregate figures are generally reliable but may double-count individuals with multiple accounts, hence labeled as "Supply Side".
