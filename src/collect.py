import os
import csv
import json

def extract_kpis_from_csv(csv_path, kpi_map, total_row_names):
    kpis = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Look for total row
            if any(total_name in row for total_name in total_row_names):
                for kpi, col_name in kpi_map.items():
                    if col_name in header:
                        idx = header.index(col_name)
                        kpis[kpi] = row[idx]
    return kpis

def collect_all_kpis(scenario_dir):
    results = {}
    farm_results = os.path.join(scenario_dir, 'Outputs', 'Farm_Results')
    # CO2E Emissions
    co2e_map = {
        'Total_Enteric_CH4_Mg_CO2e': 'Enteric CH4 (Mg C02e)',
        'Total_Manure_CH4_Mg_CO2e': 'Manure CH4 (Mg C02e)',
        'Total_Direct_N2O_Mg_CO2e': 'Direct N2O (Mg C02e)',
        'Total_Indirect_N2O_Mg_CO2e': 'Indirect N2O (Mg C02e)',
        'Total_Energy_CO2_Mg_CO2e': 'Energy CO2 (Mg C02e)',
        'Total_CO2E_Mg_CO2e': 'Sub-total (Mg C02e)',
    }
    results['CO2E_Emissions'] = extract_kpis_from_csv(
        os.path.join(farm_results, 'Farm_CO2EEmissions_Farm-en-US.csv'),
        co2e_map, ['Totals', 'Farm Total']
    )
    # Production Estimates
    prod_map = {
        'Total_Beef_kg': 'Beef (kg)',
        'Total_Lamb_kg': 'Lamb (kg)',
        'Total_Milk_kg': 'Milk (kg)',
        'Total_FPCM_kg': 'FPCM (kg)',
        'Total_Land_Applied_Manure_kg_N': 'Land Applied Manure (kg N)',
    }
    results['Production_Estimates'] = extract_kpis_from_csv(
        os.path.join(farm_results, 'Farm_EstimatesOfProduction_Farm-en-US.csv'),
        prod_map, ['Totals', 'Farm Total']
    )
    # GHG Emissions
    ghg_map = {
        'Total_Enteric_CH4_kg': 'Enteric CH4 (Kg GHGs)',
        'Total_Manure_CH4_kg': 'Manure CH4 (Kg GHGs)',
        'Total_Direct_N2O_kg': 'Direct N2O (Kg GHGs)',
        'Total_Indirect_N2O_kg': 'Indirect N2O (Kg GHGs)',
        'Total_Energy_CO2_kg': 'Energy CO2 (Kg GHGs)',
        'Total_GHG_kg': 'CO2 (Kg GHGs)',
    }
    results['GHG_Emissions'] = extract_kpis_from_csv(
        os.path.join(farm_results, 'Farm_GHGEmissions_Farm-en-US.csv'),
        ghg_map, ['Totals', 'Farm Total']
    )
    return results


def main(scenario_dir, save_json=False):
    kpis = collect_all_kpis(scenario_dir)
    if save_json:
        with open(os.path.join(scenario_dir, 'kpis.json'), 'w') as f:
            json.dump(kpis, f, indent=2)
    return kpis

if __name__ == '__main__':
    import sys
    scenario_dir = sys.argv[1] if len(sys.argv) > 1 else 'GSA_Runs/scenario_00000'
    kpis = main(scenario_dir, save_json=False)
    print(json.dumps(kpis, indent=2))
