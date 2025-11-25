from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import pandas as pd
import plotly.express as px

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "avg_time_gaps.csv"
DEFAULT_HTML_OUTPUT = PROJECT_ROOT / "dist" / "driver_gap_dashboard.html"

# Mapping: Abbreviation → (Full Name, Team)
driver_meta = {
    "VER": ("Max Verstappen", "Red Bull"),
    "PER": ("Sergio Perez", "Red Bull"),
    "LEC": ("Charles Leclerc", "Ferrari"),
    "SAI": ("Carlos Sainz", "Ferrari"),
    "HAM": ("Lewis Hamilton", "Mercedes"),
    "RUS": ("George Russell", "Mercedes"),
    "NOR": ("Lando Norris", "McLaren"),
    "PIA": ("Oscar Piastri", "McLaren"),
    "ALO": ("Fernando Alonso", "Aston Martin"),
    "STR": ("Lance Stroll", "Aston Martin"),
    "TSU": ("Yuki Tsunoda", "RB"),
    "RIC": ("Daniel Ricciardo", "RB"),
    "GAS": ("Pierre Gasly", "Alpine"),
    "OCO": ("Esteban Ocon", "Alpine"),
    "BOT": ("Valtteri Bottas", "Kick Sauber"),
    "ZHO": ("Guanyu Zhou", "Kick Sauber"),
    "MAG": ("Kevin Magnussen", "Haas"),
    "HUL": ("Nico Hülkenberg", "Haas"),
    "ALB": ("Alex Albon", "Williams"),
    "SAR": ("Logan Sargeant", "Williams"),
    "LAW": ("Liam Lawson", "RB"),
    "DOO": ("Jack Doohan", "Alpine"),
    "COL": ("Jamie Chadwick", "Williams"),
    "BEA": ("Unknown", "Unknown"),  # To prevent KeyError
}

team_colors = {
    "Red Bull": "#1E41FF",
    "Ferrari": "#DC0000",
    "Mercedes": "#00D2BE",
    "McLaren": "#FF8700",
    "Aston Martin": "#006F62",
    "RB": "#6692FF",
    "Alpine": "#FF87BC",
    "Kick Sauber": "#52E252",
    "Haas": "#B6BABD",
    "Williams": "#37BEDD",
}


def _prepare_dataframe(data_path: Path = DATA_PATH) -> pd.DataFrame:
    """Load and enrich the raw time gap data for visualization."""
    df = pd.read_csv(data_path)
    df = df[df["Driver"].isin(driver_meta)].copy()
    df["FullName"] = df["Driver"].map(lambda d: driver_meta[d][0])
    df["Team"] = df["Driver"].map(lambda d: driver_meta[d][1])
    df = df[df["Team"] != "Unknown"].copy()

    team_driver_counts = df.groupby(["Team", "Season"])["Driver"].nunique().unstack(fill_value=0)
    team_driver_counts = team_driver_counts.reindex(columns=[2023, 2024], fill_value=0)
    valid_teams = team_driver_counts[(team_driver_counts[2023] == 2) & (team_driver_counts[2024] == 2)].index
    df = df[df["Team"].isin(valid_teams)].copy()

    df["TeamDriver"] = df["Team"] + " | " + df["Driver"] + " | " + df["Season"].astype(str)
    df = df.sort_values(by=["Team", "Driver", "Season"])
    return df


def _driver_color_map(drivers: Iterable[str]) -> dict[str, str]:
    return {
        driver: team_colors[driver_meta[driver][1]]
        for driver in drivers
        if driver in driver_meta and driver_meta[driver][1] in team_colors
    }


def create_figure(data_path: Path = DATA_PATH):
    """Create the Plotly figure for the dashboard."""
    df = _prepare_dataframe(data_path)
    driver_colors = _driver_color_map(df["Driver"].unique())
    fig = px.bar(
        df,
        x="TeamDriver",
        y="AvgGapToLeaderSec",
        color="Driver",
        color_discrete_map=driver_colors,
        hover_data=["FullName", "Team", "Season", "AvgGapToLeaderSec"],
        title="Average Time Gap to Race Winner by Driver (2023 & 2024)",
        labels={"AvgGapToLeaderSec": "Avg Time Gap (s)", "TeamDriver": "Driver | Season"},
        height=700,
    )
    fig.update_layout(
        bargap=0.1,
        bargroupgap=0.02,
        xaxis_tickangle=90,
        xaxis_tickfont=dict(size=10),
        margin=dict(l=50, r=50, t=80, b=200),
    )
    return fig


def build_dashboard(
    data_path: Path = DATA_PATH,
    output_html: Path = DEFAULT_HTML_OUTPUT,
    open_browser: bool = False,
):
    """Persist the dashboard to an HTML file and optionally open it."""
    fig = create_figure(data_path)
    output_html = Path(output_html)
    output_html.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_html), include_plotlyjs="cdn", full_html=True)
    if open_browser:
        fig.show()
    return output_html


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the interactive driver gap dashboard.")
    parser.add_argument(
        "--output-html",
        default=str(DEFAULT_HTML_OUTPUT),
        help="Path for the generated dashboard HTML file (default: dist/driver_gap_dashboard.html).",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Open the dashboard in a browser window after exporting.",
    )
    args = parser.parse_args()
    build_dashboard(output_html=Path(args.output_html), open_browser=args.show)