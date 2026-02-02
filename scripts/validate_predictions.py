import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / 'data' / 'raw'
DATA_PROCESSED = ROOT / 'data' / 'processed'
OUT_DIR = ROOT / 'reports' / 'analysis_outputs'
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_effects():
    # Read impact sheet and event dates from enriched dataset, compute signed effect_value
    impact_fp = DATA_RAW / 'Impact_sheet.csv'
    enriched_fp = DATA_PROCESSED / 'ethiopia_fi_enriched_data.csv'

    impact = pd.read_csv(impact_fp)
    enriched = pd.read_csv(enriched_fp)

    events = enriched[enriched['record_type'] == 'event'].copy()
    events = events.rename(columns={'record_id': 'parent_id', 'indicator': 'event_name', 'indicator_code': 'event_code', 'observation_date': 'event_date'})

    merged = impact.merge(events[['parent_id', 'event_name', 'event_code', 'event_date']], on='parent_id', how='left')

    merged['impact_magnitude_num'] = pd.to_numeric(merged['impact_magnitude'], errors='coerce')
    merged['impact_estimate_num'] = pd.to_numeric(merged['impact_estimate'], errors='coerce')
    merged['effect_value'] = merged['impact_magnitude_num'].fillna(merged['impact_estimate_num']).fillna(0)
    mask_decrease = merged['impact_direction'].astype(str).str.lower().isin(['decrease', 'negative'])
    merged.loc[mask_decrease & merged['effect_value'].notna() & (merged['effect_value'] > 0), 'effect_value'] *= -1

    # Assign event year
    merged['event_date'] = pd.to_datetime(merged['event_date'], errors='coerce')
    merged['event_year'] = merged['event_date'].dt.year

    return merged


def observed_annual_series(enriched, indicator_code):
    df = enriched[enriched['indicator_code'] == indicator_code].copy()
    df = df[df['record_type'] == 'observation']
    df['observation_date'] = pd.to_datetime(df['observation_date'], errors='coerce')
    df['year'] = df['observation_date'].dt.year.fillna(df['fiscal_year']).astype('Int64')
    out = df.groupby('year')['value_numeric'].mean().sort_index()
    out.index = out.index.astype(int)
    return out


def build_predicted_series(enriched, effects, indicator_code):
    # Observed annual baseline
    obs = observed_annual_series(enriched, indicator_code)

    # Sum all event effects for this indicator by event_year
    ind_effects = effects[effects['related_indicator'] == indicator_code].copy()
    effects_by_year = ind_effects.groupby('event_year')['effect_value'].sum()

    # Align years (effects may be float index or have NaNs)
    effects_by_year.index = effects_by_year.index.astype('Int64')

    # Predicted = observed + effects occurring that year (simple additive model)
    # If no observed baseline exists for a year, we cannot compute a metric; keep NaN
    pred = obs.copy()
    for y, eff in effects_by_year.items():
        if pd.isna(y):
            continue
        if y in pred.index:
            pred.loc[y] = pred.loc[y] + eff
        else:
            # If we have no observation for that year, create entry using NaN baseline
            pred.loc[y] = np.nan + eff

    pred = pred.sort_index()
    return obs, pred


def compute_metrics(obs, pred):
    # Align indices and drop pairs where obs or pred is NaN
    df = pd.concat([obs, pred], axis=1)
    df.columns = ['obs', 'pred']
    df = df.dropna()
    if df.empty:
        return {'n': 0, 'MAE': np.nan, 'RMSE': np.nan, 'MAPE': np.nan}
    y_true = df['obs'].values
    y_pred = df['pred'].values
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    # MAPE: avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        mape = np.mean(np.abs((y_true - y_pred) / np.where(y_true == 0, np.nan, y_true))) * 100
    return {'n': len(df), 'MAE': mae, 'RMSE': rmse, 'MAPE': mape}


def main():
    effects = load_effects()

    enriched_fp = DATA_PROCESSED / 'ethiopia_fi_enriched_data.csv'
    enriched = pd.read_csv(enriched_fp)

    # Identify indicators to validate: intersection of columns in association matrix and observed indicators
    related_inds = effects['related_indicator'].dropna().unique().tolist()

    metrics = []
    for ind in related_inds:
        obs, pred = build_predicted_series(enriched, effects, ind)
        m = compute_metrics(obs, pred)
        m.update({'indicator': ind})
        metrics.append(m)

        # Save a quick plot for indicators with at least one paired year
        if m['n'] > 0:
            df_plot = pd.concat([obs, pred], axis=1)
            df_plot.columns = ['observed', 'predicted']
            df_plot.plot(marker='o', title=f'Observed vs Predicted: {ind}', figsize=(8,4))
            plt.xlabel('Year')
            plt.ylabel('Value')
            plt.tight_layout()
            plt.savefig(OUT_DIR / f'obs_vs_pred_{ind}.png', dpi=150)
            plt.close()

    metrics_df = pd.DataFrame(metrics).set_index('indicator')
    metrics_df.to_csv(OUT_DIR / 'prediction_validation_metrics.csv')
    print('Validation metrics saved to', OUT_DIR / 'prediction_validation_metrics.csv')


if __name__ == '__main__':
    main()
