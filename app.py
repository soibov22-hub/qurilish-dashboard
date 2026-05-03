import streamlit as st
import pandas as pd
import plotly.express as px
import json

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Qurilish Tahlili", layout="wide")

# 2. GeoJSON yuklash (uzbekistan.json fayli GitHubda bo'lishi shart)
try:
    with open("uzbekistan.json", encoding='utf-8') as f:
        uzb_geojson = json.load(f)
except Exception as e:
    st.error(f"Xarita faylini o'qishda xatolik: {e}")
    uzb_geojson = None

# 3. MA'LUMOTLAR (Aniq 14 ta hudud va 14 ta raqam)
data = {
    'Region': [
        'Tashkent City', 'Tashkent', 'Samarkand', 'Fergana', 'Andijan', 
        'Namangan', 'Bukhara', 'Navoi', 'Kashkadarya', 'Surkhandarya', 
        'Jizzakh', 'Sirdaryo', 'Khorezm', 'Karakalpakstan'
    ],
    'YAIM_Ulushi': [
        25.4, 12.8, 9.2, 8.5, 7.1, 
        6.8, 6.2, 5.9, 5.5, 4.8, 
        4.2, 3.1, 3.5, 4.0
    ]
}

# Lug'atni jadvalga aylantiramiz
df = pd.DataFrame(data)

# 4. Sarlavha
st.title("🏗 O'zbekiston Qurilish Sohasi Dashboardi")

# 5. Xaritani chizish
if uzb_geojson:
    st.subheader("📍 Hududiy nomutanosiblik xaritasi")
    
    fig = px.choropleth(
        df,
        geojson=uzb_geojson,
        locations='Region',
        featureidkey="properties.name",
        color='YAIM_Ulushi',
        color_continuous_scale="Viridis",
        labels={'YAIM_Ulushi': 'Ulush (%)'}
    )
    
    # Xaritani O'zbekistonga fokuslash
   fig.update_geos(
    visible=False, # Dunyo xaritasini yashirib, faqat viloyatlarni qoldiradi
    center={"lat": 41.3775, "lon": 64.5853}, # O'zbekiston markazi
    projection_scale=15 # Kattalashtirish darajasi
)
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500)
    st.plotly_chart(fig, use_container_width=True)

# 6. Qo'shimcha jadval
st.write("📊 Viloyatlar kesimida ko'rsatkichlar:")
st.dataframe(df, use_container_width=True)
