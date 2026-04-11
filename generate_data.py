"""
Executive Dashboard 360° — Synthetic Data Generator
Produces 5 analytical tables covering Finance, RevOps, Marketing, Pipeline, and Retention.
Run: node generate_json.mjs   (Node.js — no Python deps required)
     python generate_data.py  (Python + pandas)
"""

import pandas as pd
import numpy as np
from datetime import datetime

np.random.seed(42)

N_MONTHS = 36          # 3 years of data
START_DATE = datetime(2022, 1, 1)
SEGMENTS = ['SMB', 'Mid-Market', 'Enterprise']
CHANNELS  = ['Inbound', 'Outbound', 'Partners', 'Direct']

dates  = pd.date_range(START_DATE, periods=N_MONTHS, freq='MS')
months = [d.strftime('%Y-%m') for d in dates]
t      = np.arange(N_MONTHS)


# ── helpers ───────────────────────────────────────────────────────────────────

def trend(start, end, noise=0):
    base = np.linspace(start, end, N_MONTHS)
    return base + np.random.normal(0, noise, N_MONTHS) if noise else base

def seasonal(amp):
    return amp * np.sin(2 * np.pi * t / 12 - np.pi / 2)


# ── 1. Monthly Executive Summary ─────────────────────────────────────────────

def build_summary():
    revenue = (trend(480_000, 920_000, 18_000) + seasonal(45_000)).clip(300_000).round(0)

    cogs_pct        = trend(0.48, 0.41, 0.01)               # improving margin
    gross_profit    = (revenue * (1 - cogs_pct)).round(0)
    gross_margin    = (gross_profit / revenue).round(4)

    opex            = (revenue * trend(0.28, 0.22, 0.008)).round(0)
    ebitda          = (gross_profit - opex).round(0)
    ebitda_margin   = (ebitda / revenue).round(4)

    mrr             = (revenue / 1).round(0)                 # SaaS: revenue = MRR
    arr             = (mrr * 12).round(0)

    new_customers   = (trend(120, 260, 12) + seasonal(18)).clip(40).astype(int)
    churned         = (new_customers * trend(0.08, 0.04, 0.005)).clip(1).astype(int)
    churn_rate      = (churned / new_customers.cumsum().clip(1)).round(4)

    expansion_rev   = (revenue * trend(0.06, 0.13, 0.008)).round(0)
    contraction_rev = (revenue * trend(0.03, 0.015, 0.004)).round(0)
    nrr             = ((revenue + expansion_rev - contraction_rev - churned * (revenue / new_customers.cumsum().clip(1))) / revenue).clip(0.7, 1.4).round(4)

    mkt_spend       = (revenue * trend(0.10, 0.07, 0.006)).round(0)
    mqls            = (mkt_spend / trend(180, 110, 12)).clip(1).astype(int)
    sqls            = (mqls * trend(0.28, 0.38, 0.02)).clip(1).astype(int)
    cac             = (mkt_spend / new_customers.clip(1)).round(2)
    ltv             = ((revenue / new_customers.cumsum().clip(1)) / churn_rate.clip(0.01)).round(2)
    ltv_cac         = (ltv / cac.clip(1)).round(2)
    payback_months  = (cac / (revenue / new_customers.cumsum().clip(1))).round(1)

    win_rate        = trend(0.22, 0.31, 0.015).clip(0.05, 0.6).round(4)
    sales_cycle     = (trend(52, 38, 3) + seasonal(4)).clip(20).round(1)
    pipeline_value  = (revenue * trend(3.2, 4.8, 0.2)).round(0)
    pipeline_cover  = (pipeline_value / revenue.clip(1)).round(2)

    df = pd.DataFrame({
        'month': months,
        'revenue': revenue,
        'gross_profit': gross_profit,
        'gross_margin_pct': gross_margin,
        'ebitda': ebitda,
        'ebitda_margin_pct': ebitda_margin,
        'mrr': mrr,
        'arr': arr,
        'new_customers': new_customers,
        'churned_customers': churned,
        'churn_rate': churn_rate,
        'nrr': nrr,
        'expansion_revenue': expansion_rev,
        'marketing_spend': mkt_spend,
        'mqls': mqls,
        'sqls': sqls,
        'cac': cac,
        'ltv': ltv,
        'ltv_cac_ratio': ltv_cac,
        'payback_months': payback_months,
        'win_rate': win_rate,
        'sales_cycle_days': sales_cycle,
        'pipeline_value': pipeline_value,
        'pipeline_coverage': pipeline_cover,
    })
    return df


# ── 2. Revenue by Segment ─────────────────────────────────────────────────────

def build_by_segment(summary_df):
    rows = []
    splits = {
        'SMB':        trend(0.45, 0.32, 0.01),
        'Mid-Market': trend(0.35, 0.40, 0.01),
        'Enterprise': trend(0.20, 0.28, 0.01),
    }
    for seg, share in splits.items():
        share = share / sum(splits.values())   # normalise
        rev  = (summary_df['revenue'].values * share).round(0)
        cust = (summary_df['new_customers'].values * share * np.random.uniform(0.9, 1.1, N_MONTHS)).clip(1).astype(int)
        churn = {
            'SMB': trend(0.07, 0.04, 0.004),
            'Mid-Market': trend(0.05, 0.03, 0.003),
            'Enterprise': trend(0.03, 0.015, 0.002),
        }[seg]
        for i, m in enumerate(months):
            rows.append({
                'month': m, 'segment': seg,
                'revenue': rev[i], 'new_customers': cust[i],
                'churn_rate': round(churn[i], 4),
                'avg_deal_size': round(rev[i] / max(cust[i], 1), 2),
            })
    return pd.DataFrame(rows)


# ── 3. Revenue by Channel ─────────────────────────────────────────────────────

def build_by_channel(summary_df):
    rows = []
    splits = {
        'Inbound':  trend(0.38, 0.44, 0.012),
        'Outbound': trend(0.30, 0.22, 0.010),
        'Partners': trend(0.18, 0.24, 0.008),
        'Direct':   trend(0.14, 0.10, 0.006),
    }
    cac_base = {'Inbound': 0.7, 'Outbound': 1.4, 'Partners': 0.9, 'Direct': 0.5}
    for ch, share in splits.items():
        rev  = (summary_df['revenue'].values * share).round(0)
        cust = (summary_df['new_customers'].values * share * np.random.uniform(0.85, 1.15, N_MONTHS)).clip(1).astype(int)
        cac  = (summary_df['cac'].values * cac_base[ch] * np.random.uniform(0.9, 1.1, N_MONTHS)).round(2)
        for i, m in enumerate(months):
            rows.append({
                'month': m, 'channel': ch,
                'revenue': rev[i], 'new_customers': cust[i], 'cac': cac[i],
            })
    return pd.DataFrame(rows)


# ── 4. Marketing Funnel ───────────────────────────────────────────────────────

def build_marketing(summary_df):
    df = summary_df[['month', 'marketing_spend', 'mqls', 'sqls', 'new_customers', 'cac']].copy()
    df['mql_to_sql_rate']   = (df['sqls'] / df['mqls'].clip(1)).round(4)
    df['sql_to_won_rate']   = (df['new_customers'] / df['sqls'].clip(1)).round(4)
    df['cpl']               = (df['marketing_spend'] / df['mqls'].clip(1)).round(2)
    df['roas']              = (summary_df['revenue'] / df['marketing_spend'].clip(1)).round(2)
    return df


# ── 5. Pipeline Snapshot ─────────────────────────────────────────────────────

def build_pipeline(summary_df):
    stages = ['Prospecting', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won']
    weights = np.array([0.40, 0.25, 0.18, 0.12, 0.05])
    rows = []
    for i, m in enumerate(months):
        total_pipe = summary_df['pipeline_value'].iloc[i]
        for stage, w in zip(stages, weights):
            noise = np.random.uniform(0.85, 1.15)
            rows.append({
                'month': m, 'stage': stage,
                'deals': max(1, int(summary_df['new_customers'].iloc[i] * w * 4 * noise)),
                'value': round(total_pipe * w * noise, 0),
            })
    return pd.DataFrame(rows)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import os
    os.makedirs('data', exist_ok=True)

    summary   = build_summary()
    by_seg    = build_by_segment(summary)
    by_ch     = build_by_channel(summary)
    marketing = build_marketing(summary)
    pipeline  = build_pipeline(summary)

    summary.to_csv('data/executive_summary.csv',   index=False)
    by_seg.to_csv('data/revenue_by_segment.csv',   index=False)
    by_ch.to_csv('data/revenue_by_channel.csv',    index=False)
    marketing.to_csv('data/marketing_funnel.csv',  index=False)
    pipeline.to_csv('data/pipeline_stages.csv',    index=False)

    # Legacy file for backwards compatibility
    summary.to_csv('executive_dashboard_data.csv', index=False)

    print(f"✓ executive_summary.csv     — {len(summary)} rows, {len(summary.columns)} KPIs")
    print(f"✓ revenue_by_segment.csv    — {len(by_seg)} rows")
    print(f"✓ revenue_by_channel.csv    — {len(by_ch)} rows")
    print(f"✓ marketing_funnel.csv      — {len(marketing)} rows")
    print(f"✓ pipeline_stages.csv       — {len(pipeline)} rows")
    print("Done.")
