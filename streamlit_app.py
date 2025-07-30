import streamlit as st
import pandas as pd

# CSV dosyasını oku
import os
print("Current working directory:", os.getcwd())
df = pd.read_csv("./player_stats.csv")

print("Satır sayısı:", len(df))

print(df.head())  # İlk birkaç satırı yazdır

# Sayfa başlığı
st.title("FPL Verimlilik Analizi")

# Pozisyon seçimi
pozisyonlar = ["Tüm Oyuncular"] + sorted(df["Position"].unique())
secilen_pozisyon = st.selectbox("Pozisyona göre filtrele", pozisyonlar)

print("secilen_pozisyon")

# Filtreleme işlemi
if secilen_pozisyon != "Tüm Oyuncular":
    df = df[df["Position"] == secilen_pozisyon]

# Verimlilik hesapla (puan / değer)
df["point_per_value"] = df["Points/Value"]

# En verimli oyuncuları sırala
df = df.sort_values("point_per_value", ascending=False)
print(df.columns)
# Tabloyu göster
st.dataframe(df[["Player", "Team", "Position", "Value", "Points", "Points/Value"]].head(20))
