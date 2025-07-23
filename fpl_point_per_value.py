import requests
import pandas as pd

# Get data from FPL API
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data = response.json()

# Export data to DataFrame
players = pd.DataFrame(data['elements'])
teams = pd.DataFrame(data['teams'])

# Get the required columns
df = players[['first_name', 'second_name', 'team', 'now_cost', 'total_points', 'minutes']].copy()
df['now_cost'] = df['now_cost'] / 10  # 50 -> 5.0M gibi

# Match team name
team_map = teams.set_index('id')['name'].to_dict()
df['team_name'] = df['team'].map(team_map)

# Combine first and last name
df['name'] = df['first_name'] + ' ' + df['second_name']

# Calculate value ratio
df['value_ratio'] = df['total_points'] / df['now_cost']

# Eliminate players with very few minutes (e.g. less than 500 minutes)
df_filtered = df[df['minutes'] > 500]

# Get the top 30 players
top_value_players = df_filtered.sort_values(by='value_ratio', ascending=False).head(30)

# Show only required columns
result = top_value_players[['name', 'team_name', 'now_cost', 'total_points', 'value_ratio']]

from tabulate import tabulate

# Get only required columns
table_data = top_value_players[['name', 'team_name', 'now_cost', 'total_points', 'value_ratio']].copy()

# Rename column names
table_data.columns = ['Player', 'Team', 'Value', 'Points', 'Points/Value']

# Print table
print(tabulate(table_data, headers='keys', tablefmt='fancy_grid', showindex=False, floatfmt=".2f"))

# Oranları yuvarla
result['value_ratio'] = result['value_ratio'].round(2)
result['now_cost'] = result['now_cost'].round(1)

#print(result.to_string(index=False))
