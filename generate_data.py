"""Generates a SYNTHETIC campus electricity dataset (not real meter data).

Run:  python generate_data.py
Output: energy_readings.csv
"""
import csv
import random
from datetime import date, timedelta

random.seed(2026)

BUILDINGS = {"Library": 220, "Hostel": 380, "LabBlock": 300, "Admin": 150}
START = date(2026, 1, 1)
DAYS = 150

rows = []
for d in range(DAYS):
    day = START + timedelta(days=d)
    weekend = day.weekday() >= 5
    for name, base in BUILDINGS.items():
        factor = 0.7 if weekend and name != "Hostel" else 1.0
        kwh = random.gauss(base * factor, base * 0.08)
        rows.append([day.isoformat(), name, round(kwh, 1)])

# deliberately damage a few rows so the validation code has work to do
for i in random.sample(range(len(rows)), 6):
    rows[i][2] = -abs(rows[i][2])          # negative readings
for i in random.sample(range(len(rows)), 4):
    rows[i][2] = ""                        # missing readings
for i in random.sample(range(len(rows)), 5):
    rows[i][2] = round(float(rows[i][2] or 0) * 3 + 400, 1) if rows[i][2] != "" else ""  # spikes

with open("energy_readings.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "building", "kwh"])
    w.writerows(rows)

print("wrote", len(rows), "rows to energy_readings.csv")
