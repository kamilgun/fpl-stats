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

    # Kolonları float'a çevir
    players['selected_by_percent'] = pd.to_numeric(players['selected_by_percent'], errors='coerce')

    st.subheader("Oyuncu Seçilme Oranı vs Toplam Puan")
    
    # Kullanıcıdan filtre al
    min_sel = st.slider("Min seçilme oranı (%)", 0.0, 100.0, 3.0)
    max_sel = st.slider("Max seçilme oranı (%)", 0.0, 100.0, 10.0)

    # Filtrele
    filtered = players[
        (players['selected_by_percent'] >= min_sel) &
        (players['selected_by_percent'] <= max_sel) &
        (players['total_points'] > 0)
    ]

    # Grafik oluştur
    fig, ax = plt.subplots()
    ax.scatter(filtered['selected_by_percent'], filtered['total_points'])

    # Noktaların üzerine oyuncu ismini yaz
    for i, row in filtered.iterrows():
        ax.text(row['selected_by_percent'], row['total_points'], row['web_name'], fontsize=8)

    ax.set_xlabel('Seçilme Oranı (%)')
    ax.set_ylabel('Toplam Puan')
    ax.set_title('Seçilme Oranı vs Toplam Puan')

    # Streamlit'te göster
    st.pyplot(fig)