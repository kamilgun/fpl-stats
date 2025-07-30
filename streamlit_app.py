import streamlit as st
import requests
import pandas as pd
from select_totalpoints import grafik_selected_vs_points

# Get data from FPL API
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data = response.json()

# Export data to DataFrame
players = pd.DataFrame(data['elements'])
teams = pd.DataFrame(data['teams'])

# CSV dosyasını oku
import os
print("Current working directory:", os.getcwd())
df = pd.read_csv("./player_stats.csv")

print("Satır sayısı:", len(df))

print(df.head())  # İlk birkaç satırı yazdır

# Sayfa başlığı
st.title("FPL Efficiency Analysis")

# Pozisyon seçimi
pozisyonlar = ["All Players"] + sorted(df["Position"].unique())
secilen_pozisyon = st.selectbox("Filter by Position", pozisyonlar)

print("secilen_pozisyon")

# Filtreleme işlemi
if secilen_pozisyon != "All Players":
    df = df[df["Position"] == secilen_pozisyon]

# Verimlilik hesapla (puan / değer)
df["point_per_value"] = df["Points/Value"]

# En verimli oyuncuları sırala
df = df.sort_values("point_per_value", ascending=False)
print(df.columns)
# Tabloyu göster
st.dataframe(df[["Player", "Team", "Position", "Value", "Points", "value_ratio"]].head(60))

st.image("fantasy-football_logo.jpg", use_container_width=True)

grafik_selected_vs_points(players)

