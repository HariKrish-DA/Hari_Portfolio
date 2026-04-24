import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Hari Krishnan Kumaran Portfolio", layout="wide")

# Sidebar with your Education & Contact
st.sidebar.title("Hari Krishnan Kumaran")
st.sidebar.write("📍 Master Data Professional") [cite: 3]
st.sidebar.write("🎓 Education: Conestoga College") [cite: 6]
st.sidebar.markdown("---")
st.sidebar.button("How can I help you?") [cite: 8, 62]

# KPI Header
st.title("Interactive Professional Portfolio")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Inventory Discrepancy", "-25%", delta_color="normal") [cite: 21]
with col2:
    st.metric("ERP Systems", "SAP, NetSuite, S4") [cite: 31, 46, 55]
with col3:
    st.metric("Total Experience", "3.5+ Years") [cite: 16, 35, 51]

# Experience Tabs
tab1, tab2, tab3 = st.tabs(["Kenvue (J&J)", "Arctic Wolf", "Roche/Genentech"])

with tab1:
    st.header("Supply Planning & Master Data Analyst") [cite: 36, 41]
    st.write("**Brands:** Tylenol, Motrin") [cite: 39, 45]
    st.bullet_point("Supported SAP, MDG, and data migration for ERP transition.") [cite: 42, 43]
    st.bullet_point("Developed Win Shuttle script to facilitate automation.") [cite: 44]
    st.bullet_point("Implemented KANBAN to avoid production impacts.") [cite: 37]

with tab2:
    st.header("Supply Chain Specialist") [cite: 18]
    st.write("**Focus:** Geo-visualization & 3PL Integration") [cite: 19, 24]
    st.bullet_point("Integrated 3PL with company's ERP (NetSuite).") [cite: 24, 31]
    st.bullet_point("Implemented RMA tracker to avoid excess procurement.") [cite: 22, 23]
    # Visualizing the 25% improvement
    chart_data = pd.DataFrame({'Status': ['Before', 'After'], 'Discrepancy': [100, 75]})
    fig = px.bar(chart_data, x='Status', y='Discrepancy', title="Inventory Discrepancy Reduction")
    st.plotly_chart(fig)

with tab3:
    st.header("Associate Master Data Specialist") [cite: 52]
    st.bullet_point("Supported S4 go-live hypercare.") [cite: 55]
    st.bullet_point("Developed dashboard to measure KPI.") [cite: 53]
    st.bullet_point("Supported Make and PP module updates in SAP.") [cite: 56]
