import streamlit as st
import plotly.express as px
import pandas as pd

# 1. Viloyatlar uchun namuna ma'lumotlar
hududlar_data = {
    'Region': ['Toshkent shahri', 'Toshkent viloyati', 'Samarqand', 'Farg\'ona', 'Andijon', 
               'Namangan', 'Buxoro', 'Navoiy', 'Qashqadaryo', 'Surxondaryo', 
               'Jizzax', 'Sirdaryo', 'Xorazm', 'Qoraqalpog\'iston R.'],
    'Qurilish_Hajmi': [25.4, 12.8, 9.2, 8.5, 7.1, 6.8, 6.2, 5.9, 5.5, 4.8, 4.2, 3.1, 3.5, 4.0]
}
df_regions = pd.DataFrame(hududlar_data)

st.subheader("🗺 O‘zbekiston hududlari bo‘yicha qurilish faolligi")

# 2. Xaritani chizish (Bar chart ko'rinishida hududiy taqsimot)
# Eslatma: To'liq geografik xarita uchun GeoJSON fayli yuklanishi shart.
# Hozircha hududiy reytingni interaktiv ko'rinishda chiqaramiz:

fig_map = px.bar(df_regions.sort_values('Qurilish_Hajmi'), 
                 x='Qurilish_Hajmi', 
                 y='Region', 
                 orientation='h',
                 title="Hududlar kesimida YAIMga qo'shilgan ulush (%)",
                 color='Qurilish_Hajmi',
                 color_continuous_scale='Viridis',
                 labels={'Qurilish_Hajmi': 'Ulush (%)', 'Region': 'Viloyat'})

st.plotly_chart(fig_map, use_container_width=True)

st.info("💡 Ushbu ma'lumotlar Stat.uz portali asosida shakllantirilishi mumkin.")
