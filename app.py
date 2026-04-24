import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Hari Krishnan Kumaran Portfolio", layout="wide")

# Sidebar with your Education & Contact
st.sidebar.title("Hari Krishnan Kumaran")
st.sidebar.write("📍 Master Data Professional")
st.sidebar.write("🎓 Education: Conestoga College")
st.sidebar.markdown("---")
st.sidebar.button("How can I help you?")

# KPI Header
st.title("Interactive Professional Portfolio")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Inventory Discrepancy", "-25%", delta_color="normal")
with col2:
    st.metric("ERP Systems", "SAP, NetSuite, S4")
with col3:
    st.metric("Total Experience", "3.5+ Years")

# Experience Tabs
tab1, tab2, tab3 = st.tabs(["Kenvue (J&J)", "Arctic Wolf", "Roche/Genentech"])

with tab1:
    st.header("Supply Planning & Master Data Analyst")
    st.write("**Brands:** Tylenol, Motrin")
    st.write("- Supported SAP, MDG, and data migration for ERP transition.")
    st.write("- Developed Win Shuttle script to facilitate automation.")
    st.write("- Implemented KANBAN to avoid production impacts.")

with tab2:
    st.header("Supply Chain Specialist")
    st.write("**Focus:** Geo-visualization & 3PL Integration")
    st.write("- Integrated 3PL with company's ERP (NetSuite).")
    st.write("- Implemented RMA tracker to avoid excess procurement.")
    
    # Visualizing the 25% improvement
    chart_data = pd.DataFrame({'Status': ['Before', 'After'], 'Discrepancy': [100, 75]})
    fig = px.bar(chart_data, x='Status', y='Discrepancy', title="Inventory Discrepancy Reduction")
    st.plotly_chart(fig)

with tab3:
    st.header("Associate Master Data Specialist")
    st.write("- Supported S4 go-live hypercare.")
    st.write("- Developed dashboard to measure KPI.")
    st.write("- Supported Make and PP module updates in SAP.")
