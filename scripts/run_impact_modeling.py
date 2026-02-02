import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / 'data' / 'raw'
DATA_PROCESSED = ROOT / 'data' / 'processed'
OUT_DIR = ROOT / 'reports' / 'analysis_outputs'
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    impact_fp = DATA_RAW / 'Impact_sheet.csv'
    enriched_fp = DATA_PROCESSED / 'ethiopia_fi_enriched_data.csv'
    impact = pd.read_csv(impact_fp)
    enriched = pd.read_csv(enriched_fp)

    events = enriched[enriched['record_type'] == 'event'].copy()
    events = events.rename(columns={'record_id':'parent_id', 'indicator':'event_name', 'indicator_code':'event_code', 'observation_date':'event_date'})
    merged = impact.merge(events[['parent_id','event_name','event_code','event_date']], on='parent_id', how='left')

    merged['impact_magnitude_num'] = pd.to_numeric(merged['impact_magnitude'], errors='coerce')
    merged['impact_estimate_num'] = pd.to_numeric(merged['impact_estimate'], errors='coerce')
    merged['effect_value'] = merged['impact_magnitude_num'].fillna(merged['impact_estimate_num'])
    mask_decrease = merged['impact_direction'].str.lower().isin(['decrease','negative'])
    merged.loc[mask_decrease & merged['effect_value'].notna() & (merged['effect_value'] > 0), 'effect_value'] *= -1

    merged['event_label'] = merged['parent_id'] + ' | ' + merged['event_name'].fillna('')
    assoc = merged.pivot_table(index='event_label', columns='related_indicator', values='effect_value', aggfunc='first')
    assoc_filled = assoc.fillna(0)
    assoc_filled.to_csv(OUT_DIR / 'impact_association_matrix.csv')

    plt.figure(figsize=(12, max(4, 0.4 * assoc_filled.shape[0])))
    sns.heatmap(assoc_filled.replace(0, np.nan), annot=True, fmt='.1f', cmap='RdBu', center=0, linewidths=.5, cbar_kws={'label':'effect (pp or %)'} )
    plt.title('Event → Indicator Association Matrix (documented effect values)')
    plt.tight_layout()
    plt.savefig(OUT_DIR / 'impact_association_heatmap.png', dpi=150)
    plt.close()

    # Minimal validation prints
    def observed_by_year(indicator_code):
        df = enriched[enriched['indicator_code'] == indicator_code].copy()
        df = df[df['record_type'] == 'observation']
        df['observation_date'] = pd.to_datetime(df['observation_date'], errors='coerce')
        df['year'] = df['observation_date'].dt.year.fillna(df['fiscal_year']).astype(int)
        out = df.groupby('year')['value_numeric'].mean().sort_index()
        return out

    obs_mm = observed_by_year('ACC_MM_ACCOUNT')
    obs_acc = observed_by_year('ACC_OWNERSHIP')

    print('\nObserved Mobile Money Account Rate by year:\n', obs_mm)
    print('\nObserved Account Ownership by year:\n', obs_acc)


if __name__ == '__main__':
    main()
