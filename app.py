import streamlit as st
import pandas as pd
import plotly.express as px
import json

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Qurilish Sohasi Tahlili", layout="wide")

# 2. GeoJSON faylini mahalliy o'qish (Xato bermasligi uchun)
try:
    with open("uzbekistan.json", encoding='utf-8') as f:
        uzb_geojson = json.load(f)
except FileNotFoundError:
    st.error("Xarita fayli (uzbekistan.json) topilmadi. Iltimos, GitHub-ga yuklang.")
    uzb_geojson = None

# 3. Viloyatlar bo'yicha ilmiy ma'lumotlar
data = {
    'Region': [
        'Tashkent City', 'Tashkent', 'Samarqand', 'Fergana', 'Andijon', 
        'Namangan', 'Bukhara', 'Navoi', 'Kashkadarya', 'Surkhandarya', 
        'Jizzakh', 'Sirdaryo', 'Khorezm', 'Karakalpakstan'
    ],
    'YAIM_Ulushi': [25.4, 12.8, 9.2, 8.5, 7.1, 6.8, 6.2, 5.9, 5.5, 4.8, 4.2, 3.1, 3.5, 4.0]
}
df = pd.DataFrame(data)

# 4. Asosiy interfeys
st.title("🏗 O'zbekiston Qurilish Sohasi Tahliliy Dashboardi")
st.markdown("---")

# KPI ko'rsatkichlar
c1, c2, c3 = st.columns(3)
c1.metric("Respublika bo'yicha o'rtacha ulush", "6.4%")
c2.metric("Eng yuqori hudud", "Toshkent sh.")
c3.metric("Ma'lumotlar manbasi", "Stat.uz")

# 5. Geografik xarita qismi
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
    
    fig.update_geos(
        visible=False,
        center={"lat": 41.3, "lon": 64.5},
        projection_scale=18
    )
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=550)
    st.plotly_chart(fig, use_container_width=True)

# 6. Qo'shimcha tahlillar
st.markdown("---")
col_left, col_right = st.columns(2)

with col_left:
    st.write("📊 Viloyatlar reytingi")
    st.bar_chart(df.set_index('Region')['YAIM_Ulushi'])

with col_right:
    st.info("""
    **Ilmiy xulosa:**
    Ushbu tahlillar qurilish sohasining hududlararo keskin farq qilayotganini ko'rsatmoqda. 
    Toshkent shahridagi qurilish hajmi boshqa viloyatlarga nisbatan 2-3 barobar yuqori.
    """)

# 7. Yuklab olish imkoniyati
st.download_button("Ma'lumotlarni Excel formatida yuklash", df.to_csv(), "qurilish_tahlili.csv")
