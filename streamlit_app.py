import streamlit as st
import requests
import pandas as pd
from visuals import grafik_selected_vs_points, player_advice, grafik_value_vs_points, team_dependency_ratio, consistency_index, show_table, show_player_stats

st.set_page_config(layout="wide")

# Get data from FPL API
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data = response.json()

# Export data to DataFrame
players = pd.DataFrame(data['elements'])
teams = pd.DataFrame(data['teams'])

# --- Global CSS for padding inside each box ---
# --- Global CSS for layout adjustments ---
st.markdown("""
    <style>
        /* Sayfa genelinde kenar boşluklarını büyüt */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }

        /* Kutu stilleri */
        .box {
            padding: 20px;       /* kutu içi boşluk */
            margin: 20px;        /* kutular arası mesafe */
            border-radius: 12px; /* köşeleri yuvarlat */
            background-color: #d3d3d3; /* hafif gri arka plan */
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1); /* gölge efekti */
        }
    </style>
""", unsafe_allow_html=True)

# --- 3x3 Grid Layout ---
rows = []
for _ in range(3):
    rows.append(st.columns(3))

# 1. satır
with rows[0][0]:
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        grafik_value_vs_points()
        st.markdown('</div>', unsafe_allow_html=True)

with rows[0][1]:
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        grafik_selected_vs_points(players)
        st.markdown('</div>', unsafe_allow_html=True)

with rows[0][2]:
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        player_advice(players)
        st.markdown('</div>', unsafe_allow_html=True)
  
# 2. satır
with rows[1][0]:
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        team_dependency_ratio()
        st.markdown('</div>', unsafe_allow_html=True)

with rows[1][1]:
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        consistency_index()
        st.markdown('</div>', unsafe_allow_html=True)

with rows[1][2]:
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        show_table() 
        st.markdown('</div>', unsafe_allow_html=True)

# 3. satır
with rows[2][0]:
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        st.write("Buraya başka bir grafik gelecek")
        st.markdown('</div>', unsafe_allow_html=True)

with rows[2][1]:
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        st.write("Buraya başka bir grafik gelecek")
        st.markdown('</div>', unsafe_allow_html=True)

with rows[2][2]:
    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)
        show_player_stats()
        st.markdown('</div>', unsafe_allow_html=True)
