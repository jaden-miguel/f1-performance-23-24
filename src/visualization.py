import pandas as pd
import plotly.express as px

# Load raw data
df = pd.read_csv("data/avg_time_gaps.csv")

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

# Filter out unknown drivers
df = df[df["Driver"].isin(driver_meta)]

# Add metadata
df["FullName"] = df["Driver"].map(lambda d: driver_meta[d][0])
df["Team"] = df["Driver"].map(lambda d: driver_meta[d][1])

# Remove unknown teams or drivers
df = df[df["Team"] != "Unknown"]

# Ensure both drivers per team per year
team_driver_counts = df.groupby(["Team", "Season"])["Driver"].nunique().unstack()
valid_teams = team_driver_counts[(team_driver_counts[2023] == 2) & (team_driver_counts[2024] == 2)].index
df = df[df["Team"].isin(valid_teams)]

# Define team colors
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
    "Williams": "#37BEDD"
}

# Driver-specific color mapping
driver_colors = {
    driver: team_colors[driver_meta[driver][1]]
    for driver in df["Driver"].unique()
    if driver in driver_meta and driver_meta[driver][1] in team_colors
}

# Composite label for bar alignment: Team + Driver + Season
df["TeamDriver"] = df["Team"] + " | " + df["Driver"] + " | " + df["Season"].astype(str)

# Sort by team and driver for consistent bar order
df = df.sort_values(by=["Team", "Driver", "Season"])

# Create Plotly bar chart
fig = px.bar(
    df,
    x="TeamDriver",
    y="AvgGapToLeaderSec",
    color="Driver",
    color_discrete_map=driver_colors,
    hover_data=["FullName", "Team", "Season", "AvgGapToLeaderSec"],
    title="Average Time Gap to Race Winner by Driver (2023 & 2024)",
    labels={"AvgGapToLeaderSec": "Avg Time Gap (s)", "TeamDriver": "Driver | Season"},
    height=700
)

# Tweak bar and label spacing
fig.update_layout(
    bargap=0.1,          # Small gap between different drivers
    bargroupgap=0.02,    # Even tighter within teams
    xaxis_tickangle=90,  # Vertical label
    xaxis_tickfont=dict(size=10),
    margin=dict(l=50, r=50, t=80, b=200),
)

# Show the final chart
fig.show()