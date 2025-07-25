import pandas as pd

def load_time_gap_data(path="data/driver_time_gaps.csv"):
    df = pd.read_csv(path)
    return df
