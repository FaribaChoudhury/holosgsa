## Setup: Update File Paths

Before running the tool, update all absolute file paths in your configuration files to match your system. Common files and locations to check:

- `config.yaml`:
  - `holos_cli_path`: Path to Holos CLI executable
  - `base_scenario_dir`: Path to baseline farm data
  - `run_parent_dir`: Path to output scenarios/results

If you copy this project to a new machine, search for any absolute paths (e.g., starting with `C:\Users\...`) and update them to your own directory structure.

## Contributions

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. For major changes, open an issue first to discuss what you would like to change.

Please ensure your code follows the project style and includes appropriate tests and documentation.
# Holos GSA Tool

## Overview
This tool automates Global Sensitivity Analysis (GSA) for the Holos CLI model. It generates scenarios, runs the Holos CLI, collects KPIs, and visualizes results for fast analysis.

## Quick Start

1. **Install requirements:**
  ```powershell
  pip install -r requirements.txt
  ```
2. **Run the main workflow:**
  ```powershell
  python main.py GSA_Runs 100 --delete
  ```
  - `GSA_Runs`: Output directory for scenarios and results
  - `100`: Number of scenarios to generate
  - `--delete`: (Optional) Delete old runs before starting

3. **View results:**
  - Aggregated KPIs and visualizations are saved in `GSA_Runs/visualizations`.
  - Two images: `kpi_barplot.png` and `kpi_heatmap.png` show scenario sensitivity and overview.

## File Structure

## File & Folder Structure

```
holos_gsa_tool/
├── main.py                # Main entry point
├── requirements.txt       # Python dependencies
├── config.yaml            # Scenario/config settings
├── baseline/              # Baseline farm data
│   └── Farm/
│       ├── Farm.settings
│       ├── Beef/Beef.csv
│       ├── Dairy/Dairy.csv
│       ├── Sheep/Sheep.csv
│       ├── Fields/Fields.csv
│       └── [other components]/
├── src/
│   ├── collect.py         # Extract KPIs from outputs
│   ├── visualize.py       # Aggregate & visualize KPIs
│   ├── scenario_generator.py # Scenario generation logic
│   └── holos_gsa.py       # Orchestration logic
├── GSA_Runs/              # Output scenarios & results
│   ├── scenario_00000/
│   │   └── Farm/
│   │       ├── Farm.settings
│   │       ├── Beef/Beef.csv
│   │       ├── Dairy/Dairy.csv
│   │       ├── Sheep/Sheep.csv
│   │       ├── Fields/Fields.csv
│   │       └── [other components]/
│   │       └── Outputs/
│   ├── scenario_00001/
│   │   └── Farm/
│   │       ├── Farm.settings
│   │       ├── Beef/Beef.csv
│   │       ├── Dairy/Dairy.csv
│   │       ├── Sheep/Sheep.csv
│   │       ├── Fields/Fields.csv
│   │       └── [other components]/
│   │       └── Outputs/
│   └── ...
│   └── visualizations/
│       ├── kpi_barplot.png
│       └── kpi_heatmap.png
```

## Notes
* The folder `Farm` qualifies as a "Farms" folder for the Holos CLI.
* Each scenario folder in `GSA_Runs` is a complete copy of the baseline, with parameters varied for sensitivity analysis.
* Visualizations are saved in `GSA_Runs/visualizations`.

## Notes
- Ensure the Holos CLI executable and baseline data are present as required by your config.
- For advanced usage, see `CLI_guide/CLI_guide.md`.

## Cleanup
To remove old versions, repos, and unneeded files, delete any folders or files not listed above. Only keep the latest codebase and required data/config files.
## Example Parameters (from config.yaml)
# Holos Global Sensitivity Analysis Tool

## Overview
This tool automates scenario generation, execution, and analysis for the Holos model using its Command Line Interface (CLI). It performs global sensitivity analysis by varying specified parameters in farm component CSVs, running the Holos CLI, and aggregating results from output CSVs.

## Requirements
- Python 3.13
- Holos CLI installed (see `config.yaml` for path)
- Baseline farm data in `baseline/Farm/`
- Output directory: `baseline/Outputs/TotalResultsForAllFarms/`

## Usage
1. **Configure**: Edit `config.yaml` to set paths and parameters to vary.
2. **Run**: Execute the main Python script to generate scenarios, run Holos CLI, and collect results.
3. **Analyze**: Results are aggregated for sensitivity analysis.

## Files
- `config.yaml`: Paths and parameters for analysis.
- `baseline/Farm/`: Input farm data (CSV files).
- `baseline/Outputs/TotalResultsForAllFarms/`: Output CSVs from Holos CLI.
- `runs/`: Folder for scenario runs (auto-created).
- `README.md`: This file.

## Example Parameters (from config.yaml)
```
parameters:
  "Fields/Fields.csv::Yield(kg ha^-1)":
    min: 2000
    max: 5000
  "Beef/Beef.csv::Number Of Animals":
    min: 10
    max: 200
  "Dairy/Dairy.csv::Number Of Animals":
    min: 20
    max: 150
  "Sheep/Sheep.csv::Number Of Animals":
    min: 50
    max: 300
```

## Output
- Aggregated scenario results for each varied parameter.
- Key totals extracted from Holos output CSVs.

## Notes
- Code is designed for deterministic, reproducible runs.
- For details on CLI operation, see `CLI_guide/CLI_guide.md`.
