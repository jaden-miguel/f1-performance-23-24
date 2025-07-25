from data_processing import load_time_gap_data
import pandas as pd

def summarize_gaps():
    df = load_time_gap_data()
    summary = df.groupby(["Driver", "Season"])["TimeGapToLeader"].mean().reset_index()
    summary.rename(columns={"TimeGapToLeader": "AvgGapToLeaderSec"}, inplace=True)
    summary.to_csv("data/avg_time_gaps.csv", index=False)
    print("✅ Summary saved to data/avg_time_gaps.csv")

if __name__ == "__main__":
    summarize_gaps()
