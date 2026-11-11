"""Clean the original event records without changing their order."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
VALID_EVENT_TYPES = {"click", "login", "purchase", "scroll", "view"}


def main():
    events = pd.read_csv(ROOT / "data/raw/events.csv")
    events = events.replace(r"^\s*$", pd.NA, regex=True).dropna()
    durations = pd.to_numeric(events["duration_seconds"], errors="coerce")
    valid = (
        events["event_type"].isin(VALID_EVENT_TYPES)
        & durations.gt(0)
        & durations.mod(1).eq(0)
    )
    events = events.loc[valid].copy()
    events["duration_seconds"] = durations.loc[valid].astype("int64")
    timestamps = pd.to_datetime(events["timestamp"], format="mixed", errors="raise")
    events["timestamp"] = timestamps.dt.strftime("%Y-%m-%dT%H:%M:%S")
    output = ROOT / "data/clean/events.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(output, index=False)


if __name__ == "__main__":
    main()
