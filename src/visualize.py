import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def aggregate_kpis(run_parent_dir):
    scenario_dirs = [os.path.join(run_parent_dir, d) for d in os.listdir(run_parent_dir) if os.path.isdir(os.path.join(run_parent_dir, d))]
    records = []
    for scenario in scenario_dirs:
        kpi_path = os.path.join(scenario, 'kpis.json')
        if os.path.exists(kpi_path):
            with open(kpi_path, 'r') as f:
                kpis = json.load(f)
            flat = {}
            for section, vals in kpis.items():
                for k, v in vals.items():
                    flat[f'{section}_{k}'] = v
            flat['scenario'] = os.path.basename(scenario)
            records.append(flat)
    df = pd.DataFrame(records)
    return df

def visualize_kpis(df, outdir):
    os.makedirs(outdir, exist_ok=True)
    # Barplot for each KPI (mean across scenarios), horizontal, sorted descending
    kpi_cols = [c for c in df.columns if c != 'scenario']
    means = df[kpi_cols].apply(pd.to_numeric, errors='coerce').mean().sort_values(ascending=False)
    plt.figure(figsize=(max(8, len(means)*0.7), 6))
    sns.barplot(y=means.index, x=means.values, orient='h')
    plt.xlabel('Mean Value Across Scenarios')
    plt.ylabel('KPI')
    plt.title('Mean KPI Values Across All Scenarios')
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, 'kpi_barplot.png'))
    plt.close()
    # Heatmap: KPIs on y-axis, scenarios on x-axis
    data = df[kpi_cols].apply(pd.to_numeric, errors='coerce').T
    plt.figure(figsize=(max(8, len(df)*0.7), max(6, len(kpi_cols)*0.3)))
    sns.heatmap(data, annot=False, cmap='viridis', yticklabels=data.index, xticklabels=df['scenario'])
    plt.xlabel('Scenario')
    plt.ylabel('KPI')
    plt.title('KPI Values Across Scenarios')
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, 'kpi_heatmap.png'))
    plt.close()
