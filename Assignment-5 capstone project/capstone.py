
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# ==========================
# TASK 1: DATA INGESTION
# ==========================

def load_all_data():
    data_folder = Path("data")              # folder with CSV files
    print("Looking in:", data_folder.resolve())

    all_files = list(data_folder.glob("*.csv"))
    if not all_files:
        print("No valid CSV files found.")
        return pd.DataFrame()

    combined = []

    for file in all_files:
        try:
            df = pd.read_csv(file)

            # expect columns: timestamp, kwh
            if "timestamp" not in df.columns or "kwh" not in df.columns:
                print(f"Skipping {file.name}: missing 'timestamp' or 'kwh' column")
                continue

            df["Building"] = file.stem
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            combined.append(df)
        except Exception as e:
            print(f"Error reading {file.name}: {e}")

    if not combined:
        print("No data to process.")
        return pd.DataFrame()

    final_df = pd.concat(combined, ignore_index=True)
    return final_df

# ==========================
# TASK 2: AGGREGATION LOGIC
# ==========================

def calculate_daily_totals(df):
    df = df.set_index("timestamp")
    daily = df["kwh"].resample("D").sum()
    return daily

def calculate_weekly_totals(df):
    df = df.set_index("timestamp")
    weekly = df["kwh"].resample("W").sum()
    return weekly

def building_summary(df):
    summary = df.groupby("Building")["kwh"].agg(
        mean="mean",
        min="min",
        max="max",
        sum="sum"
    )
    return summary

# ==========================
# TASK 3: OOP MODEL
# ==========================

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, reading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def get_or_create(self, name):
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        return self.buildings[name]

    def load_from_dataframe(self, df):
        for _, row in df.iterrows():
            b = self.get_or_create(row["Building"])
            r = MeterReading(row["timestamp"], row["kwh"])
            b.add_reading(r)

    def total_campus_consumption(self):
        return sum(b.calculate_total_consumption() for b in self.buildings.values())

# ==========================
# TASK 4: VISUALIZATION
# ==========================

def create_dashboard(df, daily, weekly):
    fig, axes = plt.subplots(3, 1, figsize=(10, 12))

    # 1. Trend line: daily totals
    axes[0].plot(daily.index, daily.values, marker="o")
    axes[0].set_title("Daily Campus Energy Consumption")
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("kWh")

    # 2. Bar chart: average weekly usage per building
    df2 = df.set_index("timestamp")
    weekly_building = (
        df2.groupby("Building")["kwh"]
           .resample("W")
           .sum()
           .groupby("Building")
           .mean()
    )
    axes[1].bar(weekly_building.index, weekly_building.values)
    axes[1].set_title("Average Weekly Usage by Building")
    axes[1].set_ylabel("kWh")
    axes[1].tick_params(axis="x", rotation=45)

    # 3. Scatter: peak-hour (max) per building
    hourly = df2["kwh"].resample("h").sum()
    axes[2].scatter(hourly.index, hourly.values, s=5)
    axes[2].set_title("Hourly Consumption (All Buildings)")
    axes[2].set_xlabel("Time")
    axes[2].set_ylabel("kWh")

    plt.tight_layout()
    plt.savefig("dashboard.png")
    plt.close()

# ==========================
# TASK 5: SAVE & SUMMARY
# ==========================

def save_outputs(df, summary, daily, weekly):
    df.to_csv("cleaned_energy_data.csv", index=False)
    summary.to_csv("building_summary.csv")

    total_campus = df["kwh"].sum()
    top_building = summary["sum"].idxmax()
    peak_row = df.loc[df["kwh"].idxmax()]

    with open("summary.txt", "w") as f:
        f.write(f"Total campus consumption: {total_campus:.2f} kWh\n")
        f.write(f"Highest-consuming building: {top_building}\n")
        f.write(f"Peak load time: {peak_row['timestamp']}\n")

# ==========================
# MAIN
# ==========================

def main():
    df = load_all_data()
    if df.empty:
        print("No data loaded. Exiting.")
        return

    daily = calculate_daily_totals(df.copy())
    weekly = calculate_weekly_totals(df.copy())
    summary = building_summary(df.copy())

    manager = BuildingManager()
    manager.load_from_dataframe(df.copy())
    print("Total campus (OOP):", manager.total_campus_consumption())

    create_dashboard(df.copy(), daily, weekly)
    save_outputs(df.copy(), summary, daily, weekly)

if __name__ == "__main__":
    main()
