import streamlit as st
import pandas as pd
import plotly.express as px
import json

# 1. Sahifa sozlamalari
st.set_page_config(page_title="O'zbekiston Qurilish Tahlili", layout="wide")

# 2. GeoJSON yuklash va nomlarni tekshirish
@st.cache_data # Faylni har safar qayta yuklamaslik uchun keshga olamiz
def load_geojson():
    try:
        with open("uzbekistan.json", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Faylni o'qishda xatolik: {e}")
        return None

uzb_geojson = load_geojson()

# 3. MA'LUMOTLAR (GeoJSON standartiga mos nomlar bilan)
# DIQQAT: Agar xarita chiqmasa, quyidagi 'Region' nomlarini GeoJSON ichidagi 'name' bilan bir xil qiling
data = {
    'Region': [
        'Toshkent', 'Toshkent viloyati', 'Samarqand', 'Fargʻona', 'Andijon', 
        'Namangan', 'Buxoro', 'Navoiy', 'Qashqadaryo', 'Surxondaryo', 
        'Jizzax', 'Sirdaryo', 'Xorazm', 'Qoraqalpogʻiston Respublikasi'
    ],
    'YAIM_Ulushi': [25.4, 12.8, 9.2, 8.5, 7.1, 6.8, 6.2, 5.9, 5.5, 4.8, 4.2, 3.1, 3.5, 4.0]
}

df = pd.DataFrame(data)

# 4. Sarlavha
st.title("🏗 O'zbekiston Qurilish Sohasi Dashboardi")

# 5. Xarita va Ma'lumotlar tahlili
col1, col2 = st.columns([2, 1])

with col1:
    if uzb_geojson:
        st.subheader("📍 Hududiy nomutanosiblik xaritasi")
        
        # Xaritani chizish
        fig = px.choropleth(
            df,
            geojson=uzb_geojson,
            locations='Region',
            featureidkey="properties.name", # GeoJSON ichidagi 'name' kalitiga bog'lash
            color='YAIM_Ulushi',
            color_continuous_scale="Viridis",
            labels={'YAIM_Ulushi': 'Ulush (%)'},
            hover_name='Region'
        )
        
        # Xarita ko'rinishini sozlash
        fig.update_geos(
            fitbounds="locations", # Avtomatik hududni topib fokuslash
            visible=False
        )
        
        fig.update_layout(
            margin={"r":0,"t":30,"l":0,"b":0},
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("GeoJSON fayli yuklanmagan, xaritani ko'rsatib bo'lmaydi.")

with col2:
    st.subheader("📊 Statistik ma'lumotlar")
    st.write("Hududlar kesimida YAIM ulushi:")
    st.dataframe(
        df.sort_values(by='YAIM_Ulushi', ascending=False),
        hide_index=True,
        use_container_width=True
    )

# 6. GeoJSON nomlarini tekshirish (Ishlab ketganidan keyin bu qismni o'chirib tashlashingiz mumkin)
with st.expander("GeoJSON strukturasini tekshirish"):
    if uzb_geojson and len(uzb_geojson['features']) > 0:
        # Birinchi hududning barcha xususiyatlarini (properties) ko'rish
        st.write(uzb_geojson['features'][0]['properties'])
    else:
        st.write("Fayl topilmadi.")
