import os
import subprocess
import yaml
import sys
from src.scenario_generator import ScenarioGenerator

def run_holos_cli(cli_path, scenario_dir, units):
    # Ensure paths are absolute and correctly formatted
    scenario_dir = os.path.abspath(scenario_dir)
    output_dir = os.path.join(scenario_dir, 'Outputs')
    os.makedirs(output_dir, exist_ok=True)  # Ensure Outputs directory exists

    units_str = 'Metric' if str(units) == '1' else 'Imperial'
    args = [cli_path, scenario_dir, '-f', 'Farm', '-u', units_str, '-o', output_dir]

    # Run the CLI with the scenario directory as working directory
    subprocess.run(args, cwd=scenario_dir, check=True)

def main():
    # Allow user to specify config file and number of scenarios
    import argparse
    parser = argparse.ArgumentParser(description='Run Holos GSA tool')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to config file')
    parser.add_argument('--n', type=int, default=8, help='Number of scenarios to generate')
    parser.add_argument('--reset', action='store_true', help='Reset GSA runs directory')
    parser.add_argument('--verbose', action='store_true', help='Verbose logging')
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    cli_path = config['holos_cli_path']
    units = config['units']
    # Always use run_parent_dir from config
    generator = ScenarioGenerator(args.config)
    scenario_paths = generator.prepare_scenarios(args.n, reset=args.reset)
    for scenario_dir in scenario_paths:
        if args.verbose:
            print(f"Processing scenario: {scenario_dir}")
        run_holos_cli(cli_path, scenario_dir, units)

if __name__ == "__main__":
    main()
