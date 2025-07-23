import requests
import pandas as pd
from tabulate import tabulate

# 1. Get data from FPL API
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data = response.json()

# 2. Export data to DataFrame
players_df = pd.DataFrame(data['elements'])
teams_df = pd.DataFrame(data['teams'])
positions_df = pd.DataFrame(data['element_types'])


# 3. Match team name
team_map = dict(zip(teams_df['id'], teams_df['name']))
position_map = {
    1: 'Goalkeeper',
    2: 'Defence',
    3: 'Midfielder',
    4: 'Forward'
}

players_df['team_name'] = players_df['team'].map(team_map)
players_df['position'] = players_df['element_type'].map(position_map)
players_df['now_cost'] = players_df['now_cost'] / 10  # 50 -> 5.0M gibi

# 4. Add player name and rating
players_df['name'] = players_df['first_name'] + ' ' + players_df['second_name']
players_df['value_ratio'] = (players_df['total_points']) / (players_df['now_cost'])

print(players_df['total_points'] .head())

print(players_df['now_cost'] .head())
print(players_df['value_ratio'] .head())

# 5. Take the top 5 players from position
top_players_by_position = (
    players_df
    .sort_values(by='value_ratio', ascending=False)
    .groupby('position')
    .head(5)
)

# 6. Select and rename the required columns for the table

goalkeepers = top_players_by_position[top_players_by_position['position'] == 'Goalkeeper']
table_gk = goalkeepers[['name', 'team_name', 'position', 'now_cost', 'total_points', 'value_ratio']]
table_gk.columns = ['Player', 'Team', 'Position', 'Value', 'Points', 'Points/Value']

# 7. Tabloyu yazdır
print("\n💎 BEST P/P Goalkeepers by Position:\n")
print(tabulate(table_gk, headers='keys', tablefmt='fancy_grid', showindex=False, floatfmt=".2f"))
