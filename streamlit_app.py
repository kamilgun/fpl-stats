import streamlit as st
import pandas as pd

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
