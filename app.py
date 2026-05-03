import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. Sahifa sozlamalari
st.set_page_config(page_title="O'zbekiston Qurilish Xaritasi", layout="wide")

# 2. GeoJSON faylini yuklash (O'zbekiston xaritasi konturlari)
geojson_url = "https://raw.githubusercontent.com/crearo/uzbekistan-geojson/master/uzbekistan.json"
uzb_geojson = requests.get(geojson_url).json()

# 3. Viloyatlar bo'yicha ma'lumotlar (GeoJSON dagi nomlarga moslangan)
data = {
    'Region': [
        'Tashkent City', 'Tashkent', 'Samarqand', 'Fergana', 'Andijon', 
        'Namangan', 'Bukhara', 'Navoi', 'Kashkadarya', 'Surkhandarya', 
        'Jizzakh', 'Sirdaryo', 'Khorezm', 'Karakalpakstan'
    ],
    'Ulush': [25.4, 12.8, 9.2, 8.5, 7.1, 6.8, 6.2, 5.9, 5.5, 4.8, 4.2, 3.1, 3.5, 4.0]
}
df_map = pd.DataFrame(data)

# 4. Asosiy sarlavha
st.title("🏗 O‘zbekiston qurilish sohasi hududiy tahlili")

# 5. Geografik xarita (Choropleth)
st.subheader("📍 Geografik ko'rinish")

fig = px.choropleth(
    df_map,
    geojson=uzb_geojson,
    locations='Region',      # Jadvaldagi ustun nomi
    featureidkey="properties.name", # GeoJSON dagi kalit nomi
    color='Ulush',           # Rang beriladigan qiymat
    color_continuous_scale="Viridis",
    range_color=(0, 30),
    labels={'Ulush': 'YAIM ulushi (%)'},
    scope="asia",            # Osiyo qit'asiga fokuslash
)

# Xarita markazini O'zbekistonga to'g'rilash
fig.update_geos(
    visible=False, 
    resolution=50,
    showcountries=True, 
    countrycolor="RebeccaPurple",
    center={"lat": 41.3, "lon": 64.5}, # O'zbekiston koordinatalari
    projection_scale=15 # Kattalashtirish darajasi
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500)

st.plotly_chart(fig, use_container_width=True)

# 6. Pastki qismda jadval ko'rinishi
col1, col2 = st.columns([2, 1])
with col1:
    st.write("Viloyatlar reytingi (Jadval)")
    st.dataframe(df_map.sort_values('Ulush', ascending=False), use_container_width=True)
with col2:
    st.info("💡 Ushbu xarita Stat.uz va Ochiq ma'lumotlar portali asosida tayyorlandi.")
