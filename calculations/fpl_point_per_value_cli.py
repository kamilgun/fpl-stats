import requests
import pandas as pd
import argparse

POSITION_MAP = {
    "GK": "Goalkeeper",
    "DEF": "Defender",
    "MID": "Midfielder",
    "FWD": "Forward"
}

def fetch_fpl_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["elements"]

def process_data(data, position_filter=None):
    df = pd.DataFrame(data)
    df["point_per_value"] = (df["total_points"]) / (df["now_cost"]/10)
    df = df[["first_name", "second_name", "element_type", "now_cost", "total_points", "point_per_value"]]
    df["now_cost"] = df["now_cost"] / 10
    df['point_per_value'] = df['point_per_value'].round(2)

    if position_filter:
        position_id = list(POSITION_MAP.keys()).index(position_filter) + 1
        df = df[df["element_type"] == position_id]
    
    df = df.sort_values(by="point_per_value", ascending=False).head(10)
    return df

def main():
    parser = argparse.ArgumentParser(description="Filter PL players by position")
    parser.add_argument("--position", choices=POSITION_MAP.keys(), help="Position filter: GK, DEF, MID, FWD")
    args = parser.parse_args()

    data = fetch_fpl_data()
    df = process_data(data, position_filter=args.position)

    print(df.to_string(index=False))

if __name__ == "__main__":
    main()