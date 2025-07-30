import streamlit as st
import requests
import pandas as pd
from visuals import grafik_selected_vs_points, player_advice, grafik_value_vs_points

# Get data from FPL API
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data = response.json()

# Export data to DataFrame
players = pd.DataFrame(data['elements'])
teams = pd.DataFrame(data['teams'])


grafik_value_vs_points()

st.image("fantasy-football_logo.jpg", use_container_width=True)

grafik_selected_vs_points(players)

st.image("fantasy-football_logo.jpg", use_container_width=True)

player_advice(players) 


