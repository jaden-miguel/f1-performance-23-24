import fastf1
from fastf1.core import Laps
import pandas as pd
import os
from tqdm import tqdm

# Setup
os.makedirs("data/f1_cache", exist_ok=True)
fastf1.Cache.enable_cache("data/f1_cache")

def get_time_gap_data(season):
    df_all = pd.DataFrame()
    schedule = fastf1.get_event_schedule(season)
    races = schedule[schedule['EventFormat'] != 'Testing']

    print(f"\n📦 Fetching {season}:")
    for _, event in tqdm(races.iterrows(), total=len(races)):
        try:
            session = fastf1.get_session(season, event['RoundNumber'], 'R')
            session.load()
            laps = session.laps.pick_quicklaps()

            # Get the last lap number of the race
            last_lap = laps['LapNumber'].max()

            # Get total race time for each driver
            last_laps = laps[laps['LapNumber'] == last_lap]
            last_laps = last_laps[['Driver', 'LapTime']].dropna()
            last_laps['TotalTimeSeconds'] = last_laps['LapTime'].dt.total_seconds()

            winner_time = last_laps['TotalTimeSeconds'].min()
            last_laps['TimeGapToLeader'] = last_laps['TotalTimeSeconds'] - winner_time
            last_laps['Season'] = season
            last_laps['Event'] = event['EventName']
            last_laps['Round'] = event['RoundNumber']

            df_all = pd.concat([df_all, last_laps], ignore_index=True)

        except Exception as e:
            print(f"⚠️ Skipped {season} {event['EventName']}: {e}")
            continue

    return df_all

# Main run
df = pd.concat([
    get_time_gap_data(2023),
    get_time_gap_data(2024)
])

df.to_csv("data/driver_time_gaps.csv", index=False)
print("\n✅ Saved: data/driver_time_gaps.csv")
