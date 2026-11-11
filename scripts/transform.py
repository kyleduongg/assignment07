"""Add the calendar date to each clean event."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main():
    events = pd.read_csv(ROOT / "data/clean/events.csv")
    timestamps = pd.to_datetime(events["timestamp"], format="%Y-%m-%dT%H:%M:%S")
    events["date"] = timestamps.dt.strftime("%Y-%m-%d")
    output = ROOT / "data/transformed/events.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(output, index=False)


if __name__ == "__main__":
    main()
