import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Get data from FPL API
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data = response.json()

# Export data to DataFrame
players = pd.DataFrame(data['elements'])
teams = pd.DataFrame(data['teams'])

def grafik_selected_vs_points(players):

    # convert column to float
    players['selected_by_percent'] = pd.to_numeric(players['selected_by_percent'], errors='coerce')

    st.subheader("Player Selection Rate vs Total Points")

    # Get filter from user
    min_sel = st.slider("Min selection rate (%)", 0.0, 100.0, 3.0)
    max_sel = st.slider("Max selection rate (%)", 0.0, 100.0, 10.0)

    # Filter
    filtered = players[
        (players['selected_by_percent'] >= min_sel) &
        (players['selected_by_percent'] <= max_sel) &
        (players['total_points'] > 0)
    ]

    # Create Graphics
    fig, ax = plt.subplots()
    ax.scatter(filtered['selected_by_percent'], filtered['total_points'])

    # Name the spots
    for i, row in filtered.iterrows():
        ax.text(row['selected_by_percent'], row['total_points'], row['web_name'], fontsize=8)

    ax.set_xlabel('Selection Rate (%)')
    ax.set_ylabel('Total Points')
    ax.set_title('Selection Rate vs Total Points')

    # Publish to streamlit
    st.pyplot(fig)

def grafik_value_vs_points():
    df = pd.read_csv("./player_stats.csv")

    st.title("FPL Efficiency Analysis")

    # Pozisyon seçimi
    pozisyonlar = ["All Players"] + sorted(df["Position"].unique())
    secilen_pozisyon = st.selectbox("Filter by Position", pozisyonlar)

    if secilen_pozisyon != "All Players":
        df = df[df["Position"] == secilen_pozisyon]

    # Verimlilik hesapla (puan / değer)
    df["point_per_value"] = df["Points/Value"]

    # En verimli oyuncuları sırala
    df = df.sort_values("point_per_value", ascending=False)

    st.dataframe(df[["Player", "Team", "Position", "Value", "Points", "value_ratio"]].head(60))

def player_advice(players):
    cost_limit = st.slider("Maksimum Oyuncu Fiyatı (milyon)", 4.0, 12.5, 7.5)
    position = st.selectbox("Pozisyon", ["Tümü", "Kaleci", "Defans", "Orta Saha", "Forvet"])
    min_minutes = st.slider("Minimum oynadığı dakika", 0, 3000, 500)
    min_points = st.slider("Minimum puan", 0, 250, 50)
    sel_range = st.slider("Seçilme oranı (%)", 0.0, 100.0, (5.0, 25.0))

    # Pozisyon dönüşümü için eşleştirme sözlüğü
    position_map = {
        1: "Kaleci",
        2: "Defans",
        3: "Orta Saha",
        4: "Forvet"
    }

    # now_cost 10x formatından float'a çevriliyor
    players["cost_million"] = players["now_cost"] / 10

    # Pozisyon adı ekleniyor
    players["position_name"] = players["element_type"].map(position_map)

    # Seçilme oranı string olarak geliyorsa float'a çevir
    players["selected_by_percent"] = players["selected_by_percent"].astype(float)

    # Filtreleme işlemi
    filtered_players = players[
        (players["cost_million"] <= cost_limit) &
        (players["minutes"] >= min_minutes) &
        (players["total_points"] >= min_points) &
        (players["selected_by_percent"] >= sel_range[0]) &
        (players["selected_by_percent"] <= sel_range[1])
    ]

    # Pozisyon filtresi (eğer "Tümü" değilse)
    if position != "Tümü":
        filtered_players = filtered_players[filtered_players["position_name"] == position]

    # Verimlilik oranı hesaplama ve sıralama
    filtered_players["value_ratio"] = filtered_players["total_points"] / filtered_players["cost_million"]
    filtered_players = filtered_players.sort_values("value_ratio", ascending=False)

    # Kolonları seçerek göster
    st.subheader("Scout Asistanı - Önerilen Oyuncular")
    st.dataframe(filtered_players[["web_name", "team", "position_name", "cost_million", "total_points", "selected_by_percent", "value_ratio"]].reset_index(drop=True))
