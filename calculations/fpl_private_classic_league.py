import requests
import pandas as pd
import json

# Lig ID
league_id = 155574

# API URL
url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/"


# İstek gönder
response = requests.get(url)
data = response.json()
print(json.dumps(data, indent=4))
exit()

# Eğer istek başarısız olduysa hata mesajı göster 
if response.status_code != 200:
    print("Hata:", data.get('detail', 'Bilinmeyen hata'))
    exit() 

df = pd.DataFrame(data)
print(df.columns)
print(df.head(5))

exit()

# Katılımcı bilgilerini al
standings = data['standings']['results']

# DataFrame'e aktar
df = pd.DataFrame(standings)

# İstediğimiz alanları seç
df_filtered = df[['entry_name', 'player_name', 'rank', 'total']]

# Sıralayıp göster
df_filtered = df_filtered.sort_values('rank').reset_index(drop=True)
print(df_filtered)

# CSV olarak kaydetmek istersen:
# df_filtered.to_csv("lig_siralamasi.csv", index=False)
