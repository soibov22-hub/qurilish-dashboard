import streamlit as st
import pandas as pd
import plotly.express as px
import json

# 1. Sahifa sozlamalari
st.set_page_config(page_title="O'zbekiston Qurilish Tahlili", layout="wide")

# 2. GeoJSON yuklash
@st.cache_data
def load_geojson():
    try:
        with open("uzbekistan.json", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Faylni o'qishda xatolik: {e}")
        return None

uzb_geojson = load_geojson()

# 3. MA'LUMOTLAR
data = {
    'Region': [
        'Toshkent sh.', 'Toshkent viloyati', 'Samarqand viloyati', 
        'Fargʻona viloyati', 'Andijon viloyati', 'Namangan viloyati', 
        'Buxoro viloyati', 'Navoiy viloyati', 'Qashqadaryo viloyati', 
        'Surxondaryo viloyati', 'Jizzax viloyati', 'Sirdaryo viloyati', 
        'Xorazm viloyati', 'Qoraqalpogʻiston Respublikasi'
    ],
    'YAIM_Ulushi': [25.4, 12.8, 9.2, 8.5, 7.1, 6.8, 6.2, 5.9, 5.5, 4.8, 4.2, 3.1, 3.5, 4.0]
}

df = pd.DataFrame(data)

# 4. Sarlavha
st.title("🏗 O'zbekiston Qurilish Sohasi Dashboardi")

# 5. Xarita
if uzb_geojson:
    st.subheader("📍 Hududiy nomutanosiblik xaritasi")

    fig = px.choropleth(
        df,
        geojson=uzb_geojson,
        locations='Region',
        featureidkey="properties.ADM1_UZ",
        color='YAIM_Ulushi',
        color_continuous_scale="Viridis",
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=600)

    st.plotly_chart(fig, use_container_width=True)

    # Jadval
    st.write("📊 Statistik ma'lumotlar:")
    st.dataframe(df, use_container_width=True, hide_index=True)
