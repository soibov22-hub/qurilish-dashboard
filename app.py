import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfiguratsiya
st.set_page_config(page_title="Pro Dashboard", layout="wide")

# 2. Ma'lumotlar
yillar = list(range(2015, 2026))
ulush = [5.2, 5.6, 5.4, 5.8, 6.3, 6.7, 6.7, 6.7, 7.3, 7.2, 7.3]
df = pd.DataFrame({'Yil': yillar, 'YAIM ulushi (%)': ulush})

# 3. Sidebar - Filtrlar
st.sidebar.header("Tahlil Sozlamalari")
rang_tanlash = st.sidebar.color_picker("Grafik rangini tanlang", "#00CC96")
yil_diapazon = st.sidebar.select_slider("Yillarni tanlang", options=yillar, value=(2015, 2025))

# Ma'lumotlarni filtrlash
filtered_df = df[(df['Yil'] >= yil_diapazon[0]) & (df['Yil'] <= yil_diapazon[1])]

# 4. Asosiy qism
st.title("🏗 Qurilish Sohasi Kengaytirilgan Dashboardi")

# KPI qismi
c1, c2, c3 = st.columns(3)
c1.metric("Tanlangan davrdagi o'rtacha", f"{filtered_df['YAIM ulushi (%)'].mean():.1f}%")
c2.metric("O'sish sur'ati", f"{filtered_df['YAIM ulushi (%)'].iloc[-1] - filtered_df['YAIM ulushi (%)'].iloc[0]:.1f}%")
c3.status("Ma'lumotlar holati", state="complete")

# 5. Grafik
fig = px.bar(filtered_df, x='Yil', y='YAIM ulushi (%)', 
             title="Yillik ulush (Bar Chart ko'rinishida)",
             text_auto=True)
fig.update_traces(marker_color=rang_tanlash)
st.plotly_chart(fig, use_container_width=True)

# 6. Izoh qo'shish
st.info(f"Siz hozirda {yil_diapazon[0]} va {yil_diapazon[1]} yillar oralig'idagi ma'lumotlarni ko'ryapsiz.")

# 7. Yuklab olish
st.download_button("Excelga eksport qilish", filtered_df.to_csv(), "data.csv")
