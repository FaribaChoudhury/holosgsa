# Holos GSA Tool

This script automates scenario generation, execution, and output parsing for the Holos CLI. It reads `config.yaml`, generates scenarios by varying parameters, runs the Holos CLI for each scenario, and parses output CSVs for totals.

## How to Use

1. **Edit `config.yaml`** to set paths and parameters.
2. **Run the script**:
   ```powershell
   python holos_gsa.py
   ```
3. **Results**: Each scenario's results are saved in its folder as `results.yaml`.

## Notes
- The script expects the Holos CLI to be installed and accessible at the path specified in `config.yaml`.
- Scenario folders are created in the `runs/` directory.
- Output totals are parsed from CSVs in `Outputs/TotalResultsForAllFarms/`.
- For more details, see the main README.
