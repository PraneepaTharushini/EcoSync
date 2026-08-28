"""
Trains a Random Forest to predict solar output as a CAPACITY FACTOR
(actual_kwh / plant_capacity_kw) rather than raw kWh. This matters because
the training data comes from utility-scale plants (capacity in the
thousands of kW), while the app targets residential systems (a handful of
kW) - training on raw kWh would learn relationships that don't transfer
across system sizes. A capacity factor generalizes: multiply the model's
predicted factor by ANY user's real capacity_kw at inference time.

Usage:
    python train.py --data ../data/processed/train.csv --out ../models/rf_v1.joblib
"""
import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error

FEATURE_COLS = ["irradiance_ratio", "AMBIENT_TEMPERATURE", "MODULE_TEMPERATURE", "hour_of_day", "day_of_year"]
PERFORMANCE_RATIO = 0.80  # same constant used in the physics baseline, for a fair comparison


def estimate_capacity(df: pd.DataFrame) -> dict:
    """Per-plant capacity estimate: 99th percentile of observed output, since
    the dataset has no explicit rated-capacity field."""
    return df.groupby("plant")["actual_kwh"].quantile(0.99).to_dict()


def physics_baseline_predict(irradiance_ratio: np.ndarray, capacity_kw: np.ndarray) -> np.ndarray:
    """Same formula as backend/app/services/forecast_service.py, vectorized."""
    return np.clip(irradiance_ratio, 0, None) * capacity_kw * PERFORMANCE_RATIO


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.data, parse_dates=["DATE_TIME"])

    capacity_by_plant = estimate_capacity(df)
    df["capacity_kw"] = df["plant"].map(capacity_by_plant)
    df["capacity_factor"] = (df["actual_kwh"] / df["capacity_kw"]).clip(0, 1.5)

    # Time-based split (not random) - the last ~20% of days become the test
    # set. Random shuffling would leak nearby hours between train/test and
    # overstate accuracy, since consecutive hours are highly correlated.
    df = df.sort_values("DATE_TIME")
    split_idx = int(len(df) * 0.8)
    train_df, test_df = df.iloc[:split_idx], df.iloc[split_idx:]

    X_train, y_train = train_df[FEATURE_COLS], train_df["capacity_factor"]
    X_test, y_test = test_df[FEATURE_COLS], test_df["capacity_factor"]

    model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    # Evaluate both the trained model AND the physics baseline on the same
    # held-out test set, rescaled back to real kWh using each row's real
    # capacity, so the comparison is apples-to-apples and report-ready.
    rf_pred_factor = model.predict(X_test)
    rf_pred_kwh = rf_pred_factor * test_df["capacity_kw"].values
    baseline_pred_kwh = physics_baseline_predict(test_df["irradiance_ratio"].values, test_df["capacity_kw"].values)
    actual_kwh = test_df["actual_kwh"].values

    def metrics(pred, actual, label):
        # MAPE blows up near-zero actuals (night hours), so also report
        # MAE/RMSE in absolute kWh, which are more meaningful here.
        mae = mean_absolute_error(actual, pred)
        rmse = np.sqrt(mean_squared_error(actual, pred))
        nonzero = actual > (0.01 * test_df["capacity_kw"].values)  # skip near-zero night hours for MAPE
        mape = mean_absolute_percentage_error(actual[nonzero], pred[nonzero]) * 100
        print(f"{label}: MAE={mae:.2f} kWh, RMSE={rmse:.2f} kWh, MAPE={mape:.1f}% (daylight hours only)")
        return {"mae": mae, "rmse": rmse, "mape": mape}

    print(f"\nTest set: {len(test_df)} hours, plants: {test_df['plant'].unique().tolist()}")
    print(f"Estimated capacity per plant: {capacity_by_plant}\n")
    rf_metrics = metrics(rf_pred_kwh, actual_kwh, "Random Forest")
    baseline_metrics = metrics(baseline_pred_kwh, actual_kwh, "Physics baseline")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "feature_cols": FEATURE_COLS, "performance_ratio": PERFORMANCE_RATIO}, args.out)
    print(f"\nSaved trained model to {args.out}")

    report = {
        "test_set_size": len(test_df),
        "capacity_by_plant": {k: float(v) for k, v in capacity_by_plant.items()},
        "random_forest": rf_metrics,
        "physics_baseline": baseline_metrics,
    }
    report_path = args.out.parent / "evaluation_report.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"Saved evaluation report to {report_path}")


if __name__ == "__main__":
    main()
