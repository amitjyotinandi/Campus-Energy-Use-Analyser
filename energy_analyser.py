"""Campus Energy-Use Analyser
Reads daily meter readings from CSV, rejects bad rows, finds abnormal spikes,
summarises usage per building/month and plots trends.
"""
import csv
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ---------- procedural part: validation helpers ----------
def is_valid_reading(value):
    """A reading must be a number and not negative."""
    try:
        return float(value) >= 0
    except (TypeError, ValueError):
        return False


# ---------- class part ----------
class MeterRecord:
    def __init__(self, date, building, kwh):
        self.date = date
        self.building = building.strip()
        self.kwh = float(kwh)

    def __repr__(self):
        return f"MeterRecord({self.date}, {self.building}, {self.kwh})"

    def to_dict(self):
        return {"date": self.date, "building": self.building, "kwh": self.kwh}


class MeterLog:
    """Collection of records. __len__ lets us use len(log) and __iter__ lets
    us loop over the log directly, so it behaves like a normal container."""

    def __init__(self):
        self.records = []

    def add(self, rec):
        self.records.append(rec)

    def __len__(self):
        return len(self.records)

    def __iter__(self):
        return iter(self.records)


def load_csv(path):
    log = MeterLog()
    rejected = []
    with open(path, newline="") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            if row["building"].strip() and is_valid_reading(row["kwh"]):
                log.add(MeterRecord(row["date"], row["building"], row["kwh"]))
            else:
                rejected.append((line_no, dict(row)))
    return log, rejected


# ---------- NumPy part ----------
def moving_average(values, window=7):
    kernel = np.ones(window) / window
    return np.convolve(values, kernel, mode="valid")


def find_spikes(values, z_limit=3.0):
    arr = np.array(values)
    z = (arr - arr.mean()) / arr.std()
    return np.where(np.abs(z) > z_limit)[0]


# ---------- Pandas part ----------
def to_dataframe(log):
    df = pd.DataFrame([r.to_dict() for r in log])
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df


def monthly_summary(df):
    return (df.groupby(["building", "month"])["kwh"]
              .agg(total="sum", average="mean", peak="max")
              .round(1)
              .reset_index())


# ---------- plotting ----------
def plot_trend(df, building, outdir):
    sub = df[df["building"] == building].sort_values("date")
    vals = sub["kwh"].values
    ma = moving_average(vals, 7)
    spikes = find_spikes(vals)

    plt.figure(figsize=(9, 4))
    plt.plot(sub["date"], vals, color="lightgray", label="daily kWh")
    plt.plot(sub["date"].iloc[6:], ma, color="tab:blue", label="7-day average")
    plt.scatter(sub["date"].iloc[spikes], vals[spikes], color="red", zorder=3, label="spike")
    plt.title(f"{building} - daily consumption")
    plt.xlabel("Date")
    plt.ylabel("kWh")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"trend_{building}.png"), dpi=120)
    plt.close()


def plot_monthly(summary, outdir):
    pivot = summary.pivot(index="month", columns="building", values="total")
    pivot.plot(kind="bar", figsize=(9, 4))
    plt.title("Monthly total consumption by building")
    plt.ylabel("kWh")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "monthly_totals.png"), dpi=120)
    plt.close()


def main():
    outdir = "outputs"
    os.makedirs(outdir, exist_ok=True)

    log, rejected = load_csv("energy_readings.csv")
    print(f"valid records: {len(log)}   rejected rows: {len(rejected)}")

    df = to_dataframe(log)
    summary = monthly_summary(df)
    summary.to_csv(os.path.join(outdir, "monthly_summary.csv"), index=False)
    with open(os.path.join(outdir, "monthly_summary.json"), "w") as f:
        json.dump(summary.to_dict(orient="records"), f, indent=2)

    print("\nSpikes found per building (|z| > 3):")
    for b in sorted(df["building"].unique()):
        vals = df[df["building"] == b].sort_values("date")["kwh"].values
        print(f"  {b}: {len(find_spikes(vals))}")
        plot_trend(df, b, outdir)
    plot_monthly(summary, outdir)

    print("\nHighest average daily use:")
    print(df.groupby("building")["kwh"].mean().round(1).sort_values(ascending=False))
    print("\nFiles saved in ./outputs")


if __name__ == "__main__":
    main()
