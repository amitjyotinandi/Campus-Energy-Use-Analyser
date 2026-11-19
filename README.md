# Campus Energy-Use Analyser

Python Programming Laboratory – end semester project (Option 1: Campus energy-use analyser).

## What it does
- Reads daily electricity readings for campus buildings from a CSV file
- Rejects negative, non-numeric and missing readings and counts them
- Finds abnormal spikes using a z-score rule (|z| > 3)
- Calculates a 7-day moving average with NumPy
- Builds monthly total / average / peak summaries per building with Pandas
- Exports summaries to CSV and JSON, and saves plots with Matplotlib

## Data
`energy_readings.csv` is **synthetic**. It is produced by `generate_data.py`
with a fixed random seed. A few bad values (negative, blank, spikes) were put
in on purpose to test the validation. It is not real meter data.

## Files
| File | Purpose |
|------|---------|
| generate_data.py | creates the synthetic CSV |
| energy_analyser.py | main program |
| test_energy.py | simple tests |
| outputs/ | plots and summary files after running |

## How to run
```
pip install numpy pandas matplotlib
python generate_data.py
python energy_analyser.py
python test_energy.py
```

## Course outcome mapping
- CO1 functions and control flow: `is_valid_reading`, `load_csv`
- CO2 data structures and file I/O: lists, dicts, csv, json
- CO3 classes: `MeterRecord`, `MeterLog` (uses `__init__`, `__repr__`, `__len__`, `__iter__`)
- CO4 NumPy: moving average, z-score spike detection
- CO5 Pandas: group-by monthly summaries
- CO6 Matplotlib: trend plots and monthly bar chart

## Why `__len__` and `__iter__`
They let `MeterLog` behave like a normal Python container, so we can write
`len(log)` and `for rec in log` instead of reaching into `log.records`.

## Results (synthetic data)
590 of 600 rows valid, 10 rejected. Hostel has the highest average daily use
(about 379 kWh); Admin the lowest (about 148 kWh). Spikes were flagged in
Admin (2), LabBlock (1) and Library (2).

## Limitations
Synthetic data only, a simple z-score rule (a large spike can inflate the
standard deviation), and no real-time input.

## Team contributions
This is an individual project submitted by:

- Name: Amitjyoti Nandi
- Roll Number: 67
- Section: A2
- Department: Electronics and Communication Engineering

As the sole project member, I am responsible for the project implementation, dataset preparation, data analysis, testing, result generation, and project documentation.
