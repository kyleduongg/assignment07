"""Check every output against the original CSV using independent parsing."""
import csv
from datetime import datetime
from math import isclose
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative):
    with (ROOT / relative).open(newline="") as stream:
        return list(csv.DictReader(stream))


def timestamp(value):
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S", "%m/%d/%Y %H:%M:%S"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise ValueError(value)


def main():
    raw = read("data/raw/events.csv")
    expected = []
    for row in raw:
        if any(not value.strip() for value in row.values()):
            continue
        if row["event_type"] not in {"click", "login", "purchase", "scroll", "view"}:
            continue
        if int(row["duration_seconds"]) <= 0:
            continue
        expected.append({**row, "timestamp": timestamp(row["timestamp"]).strftime("%Y-%m-%dT%H:%M:%S")})
    clean = read("data/clean/events.csv")
    transformed = read("data/transformed/events.csv")
    features = read("data/features/events.csv")
    assert clean == expected
    assert len(clean) == len(transformed) == len(features)
    assert list(features[0]) == ["user_id", "timestamp", "event_type", "duration_seconds",
                                 "date", "duration_minutes", "weekday"]
    for original, dated, featured in zip(clean, transformed, features):
        date = datetime.strptime(original["timestamp"], "%Y-%m-%dT%H:%M:%S")
        assert dated == {**original, "date": date.strftime("%Y-%m-%d")}
        assert {key: featured[key] for key in dated} == dated
        assert isclose(float(featured["duration_minutes"]), int(original["duration_seconds"]) / 60)
        assert featured["weekday"] == date.strftime("%A")
    print(f"Verified {len(raw)} raw rows -> {len(clean)} clean/transformed/feature rows; all seven columns and values match.")


if __name__ == "__main__":
    main()
