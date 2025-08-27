def main(run_parent_dir, num_scenarios, config_path='config.yaml', reset=True):
    gen = ScenarioGenerator(config_path)
    gen.run_parent = run_parent_dir
    gen.prepare_scenarios(num_scenarios, reset=reset)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python scenario_generator.py <run_parent_dir> <num_scenarios>')
        sys.exit(1)
    main(sys.argv[1], int(sys.argv[2]))
import os
import shutil
import yaml
import csv
from typing import Dict, Any, List

class ScenarioGenerator:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.base_dir = self.config['base_scenario_dir']
        self.run_parent = self.config['run_parent_dir']
        self.parameters = self.config['parameters']

    def clean_runs(self):
        # Remove the entire run_parent directory if it exists, then recreate it.
        if os.path.exists(self.run_parent):
            shutil.rmtree(self.run_parent)
        os.makedirs(self.run_parent, exist_ok=True)

    def generate_scenarios(self, n_scenarios: int) -> List[Dict[str, Any]]:
        # Use Sobol sequence for sampling
        try:
            from SALib.sample import sobol_sequence
        except ImportError:
            raise ImportError('SALib is required for Sobol sampling. Install with `pip install SALib`.')
        param_keys = list(self.parameters.keys())
        bounds = [[self.parameters[k]['min'], self.parameters[k]['max']] for k in param_keys]
        # Generate Sobol samples in [0,1]
        samples = sobol_sequence.sample(n_scenarios, len(param_keys))
        # Scale samples to parameter bounds
        scenarios = []
        for s in samples:
            scenario = {}
            for i, k in enumerate(param_keys):
                minv, maxv = bounds[i]
                scenario[k] = minv + s[i] * (maxv - minv)
            scenarios.append(scenario)
        return scenarios

    # Removed obsolete create_scenario_folder

    def update_csv(self, csv_path: str, column: str, value: Any):
        rows = []
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if column in row:
                    row[column] = str(value)
                rows.append(row)
        # Update ALL rows for the column
        for row in rows:
            if column in row:
                row[column] = str(value)
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def prepare_scenarios(self, n_scenarios: int, reset: bool = False):
        """Prepare multiple scenario folders, each with a Farm subfolder and updated CSVs."""
        if reset:
            self.clean_runs()
        scenarios = self.generate_scenarios(n_scenarios)
        scenario_paths = []
        for i, scenario in enumerate(scenarios):
            scenario_name = f"scenario_{i:05d}"
            scenario_dir = os.path.join(self.run_parent, scenario_name)
            # Forcefully delete scenario_dir if it exists
            if os.path.exists(scenario_dir):
                shutil.rmtree(scenario_dir)
            # Copy the entire baseline directory into scenario_dir
            shutil.copytree(self.base_dir, scenario_dir)
            # Overwrite Farm folder in scenario_dir with baseline Farm folder
            baseline_farm = os.path.join(self.base_dir, "Farm")
            scenario_farm = os.path.join(scenario_dir, "Farm")
            if os.path.exists(scenario_farm):
                shutil.rmtree(scenario_farm)
            shutil.copytree(baseline_farm, scenario_farm)
            # Update CSVs in scenario_farm
            for key, value in scenario.items():
                try:
                    rel_path, col = key.split('::')
                except ValueError:
                    continue
                csv_path = os.path.join(scenario_farm, rel_path)
                if os.path.exists(csv_path):
                    self.update_csv(csv_path, col, value)
            scenario_paths.append(scenario_dir)
        return scenario_paths
