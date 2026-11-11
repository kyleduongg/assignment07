import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    from pathlib import Path

    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd

    return Path, mo, pd, plt


@app.cell
def _(mo):
    mo.md("""
    # Event durations
    Distribution of event durations after cleaning and feature generation.
    """)
    return


@app.cell
def _(Path, mo, pd):
    project_root = Path(mo.notebook_location()).parent
    events = pd.read_csv(project_root / "data/features/events.csv")
    return (events,)


@app.cell
def _(events, plt):
    fig, ax = plt.subplots()
    ax.hist(events["duration_minutes"], bins=30, edgecolor="white")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of events")
    ax.set_title("Event duration distribution")
    fig.tight_layout()
    fig
    return


if __name__ == "__main__":
    app.run()
