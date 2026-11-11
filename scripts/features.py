"""Add duration and weekday features, preserving every transformed row."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main():
    events = pd.read_csv(ROOT / "data/transformed/events.csv")
    events["duration_minutes"] = events["duration_seconds"] / 60
    events["weekday"] = pd.to_datetime(events["date"], format="%Y-%m-%d").dt.day_name()
    output = ROOT / "data/features/events.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(output, index=False)


if __name__ == "__main__":
    main()
