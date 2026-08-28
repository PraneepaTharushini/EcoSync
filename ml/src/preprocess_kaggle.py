"""
Preprocess the Kaggle 'Solar Power Generation Data' CSVs into an hourly
training table: one row per (plant, hour) with weather features and the
real measured total kWh output for that hour.

Usage:
    python preprocess_kaggle.py --raw-dir ../data/raw --out ../data/processed/train.csv
"""
import argparse
from pathlib import Path

import pandas as pd


def load_plant(raw_dir: Path, gen_file: str, weather_file: str, plant_label: str) -> pd.DataFrame:
    gen = pd.read_csv(raw_dir / gen_file)
    weather = pd.read_csv(raw_dir / weather_file)

    # DATE_TIME format differs slightly between the two Plant_1 files (one uses
    # DD-MM-YYYY, the other YYYY-MM-DD) - let pandas infer per-column rather
    # than assuming a single format.
    gen["DATE_TIME"] = pd.to_datetime(gen["DATE_TIME"], dayfirst=True, errors="coerce")
    weather["DATE_TIME"] = pd.to_datetime(weather["DATE_TIME"], dayfirst=True, errors="coerce")
    gen = gen.dropna(subset=["DATE_TIME"])
    weather = weather.dropna(subset=["DATE_TIME"])

    # Sum AC_POWER across all inverters (SOURCE_KEY) at each timestamp to get
    # total plant-level power, since we're predicting whole-system output.
    gen_plant = gen.groupby("DATE_TIME", as_index=False)["AC_POWER"].sum()

    # Weather is one sensor per plant, already one row per timestamp.
    weather_plant = weather[["DATE_TIME", "AMBIENT_TEMPERATURE", "MODULE_TEMPERATURE", "IRRADIATION"]]

    merged = pd.merge(gen_plant, weather_plant, on="DATE_TIME", how="inner")
    merged["plant"] = plant_label
    return merged


def to_hourly(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts 15-minute readings to hourly rows. AC_POWER is instantaneous kW,
    so hourly energy (kWh) = mean(kW over the hour's readings) * 1 hour.
    Weather features are averaged over the hour.
    """
    df = df.set_index("DATE_TIME")
    hourly = (
        df.groupby("plant")
        .resample("1h")
        .agg(
            {
                "AC_POWER": "mean",  # mean kW over the hour -> treated as kWh for a 1h bucket
                "AMBIENT_TEMPERATURE": "mean",
                "MODULE_TEMPERATURE": "mean",
                "IRRADIATION": "mean",
            }
        )
        .rename(columns={"AC_POWER": "actual_kwh"})
        .reset_index()
    )
    return hourly.dropna()


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df["hour_of_day"] = df["DATE_TIME"].dt.hour
    df["day_of_year"] = df["DATE_TIME"].dt.dayofyear
    # Irradiance in this dataset is already normalized (~0 to ~1.2, matching
    # standard-test-condition scaling), same convention your physics baseline
    # (irradiance / 1000) uses for W/m^2 - here it's already the ratio.
    df["irradiance_ratio"] = df["IRRADIATION"]
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    plant1 = load_plant(args.raw_dir, "Plant_1_Generation_Data.csv", "Plant_1_Weather_Sensor_Data.csv", "plant_1")
    plant2 = load_plant(args.raw_dir, "Plant_2_Generation_Data.csv", "Plant_2_Weather_Sensor_Data.csv", "plant_2")

    combined = pd.concat([plant1, plant2], ignore_index=True)
    hourly = to_hourly(combined)
    hourly = add_features(hourly)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    hourly.to_csv(args.out, index=False)
    print(f"Wrote {len(hourly)} hourly rows to {args.out}")
    print(hourly.groupby("plant")["actual_kwh"].describe())


if __name__ == "__main__":
    main()
