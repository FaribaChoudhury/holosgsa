import os
import sys
import json
from src.collect import main as collect_main
from src.visualize import aggregate_kpis, visualize_kpis

def run_all(run_parent_dir, num_scenarios=None, delete_runs=False):
    import shutil
    # Optionally delete GSA_Runs directory
    if delete_runs and os.path.exists(run_parent_dir):
        shutil.rmtree(run_parent_dir)
    # Generate scenarios if num_scenarios is specified
    if num_scenarios is not None:
        from src.scenario_generator import main as scenario_gen_main
        scenario_gen_main(run_parent_dir, num_scenarios)
    # Only process scenario directories
    scenario_dirs = [os.path.join(run_parent_dir, d) for d in os.listdir(run_parent_dir)
                    if os.path.isdir(os.path.join(run_parent_dir, d)) and d.startswith('scenario_')]
    for scenario in scenario_dirs:
        kpis = collect_main(scenario, save_json=True)
    df = aggregate_kpis(run_parent_dir)
    visualize_kpis(df, os.path.join(run_parent_dir, 'visualizations'))
    print('Visualization images saved to:', os.path.join(run_parent_dir, 'visualizations'))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run Holos GSA workflow')
    parser.add_argument('run_parent_dir', help='GSA runs directory')
    parser.add_argument('num_scenarios', nargs='?', type=int, help='Number of scenarios to generate')
    parser.add_argument('--delete', action='store_true', help='Delete GSA runs directory before running')
    args = parser.parse_args()
    run_all(args.run_parent_dir, args.num_scenarios, args.delete)
