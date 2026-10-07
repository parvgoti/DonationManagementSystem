# Donation Management & Transparency System

A college Python project based on Project P24.

## Requirements
- Python 3.10+ recommended
- Tkinter
- Pandas
- NumPy
- Matplotlib

## Install
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

## Test
```bash
python -m unittest discover -s tests -v
```

## Main Features
- Donor CRUD
- Donation CRUD
- Search
- CSV persistent storage
- Total/average/median/min/max statistics
- Cause/source/month comparisons
- Contribution-pattern identification
- Tkinter GUI
- Three Matplotlib visual reports
- Input validation
- Exception handling
- Unit tests

## Data
`data/donors.csv` and `data/donations.csv` are persistent storage files.

## Reports
Generated files are saved inside `reports/`:
- donation_by_cause.png
- donation_by_source.png
- donation_trend_by_month.png
- donation_analysis.csv

## Recommended Viva Explanation
1. Tkinter is used to create the desktop GUI.
2. CSV files provide persistent storage.
3. Pandas converts donation records into a DataFrame for filtering and grouping.
4. NumPy performs numerical calculations such as sum, mean, median, min and max.
5. Matplotlib creates visual reports.
6. User-defined modules separate validation, storage, donor management, donation management, analytics and visualization.
7. Exception handling prevents the application from terminating unexpectedly.
