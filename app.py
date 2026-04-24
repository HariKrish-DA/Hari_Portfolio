import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Hari Krishnan Kumaran Portfolio", layout="wide")

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("Hari Krishnan Kumaran")
st.sidebar.write("📍 Master Data Professional")
st.sidebar.write("🎓 Education: Conestoga College")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate Dashboard", ["Professional Summary", "Interactive CR Tracker"])
st.sidebar.markdown("---")
st.sidebar.button("How can I help you?")

# ==========================================
# PAGE 1: PROFESSIONAL SUMMARY
# ==========================================
if page == "Professional Summary":
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

# ==========================================
# PAGE 2: INTERACTIVE CR TRACKER
# ==========================================
elif page == "Interactive CR Tracker":
    st.title("Performance & CR Tracker Dashboard")
    st.write("Explore my workflow productivity, Change Requests (CRs), and process distributions interactively.")
    
    try:
        # Load the perfect CSV
        df = pd.read_csv("Data.csv")
        
        # Clean data (keep relevant columns and drop empty rows)
        df.dropna(subset=['Change Request', 'CR type'], inplace=True)
        
        # Calculate Top-Level KPIs
        total_crs = len(df)
        top_cr_type = df['CR type'].mode()[0] if not df.empty else "N/A"
        top_process = df['Process'].mode()[0] if not df.empty else "N/A"
        
        # Display KPIs
        st.markdown("### Overview Metrics")
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Change Requests (CRs)", f"{total_crs:,}")
        kpi2.metric("Dominant CR Type", top_cr_type)
        kpi3.metric("Top Process Handled", top_process)
        
        st.markdown("---")
        
        # Visualizations Row 1: CR Type & Monthly Completions
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # 1. Modules in SAP (Pie Chart)
            type_counts = df['CR type'].value_counts().reset_index()
            type_counts.columns = ['CR type', 'Count']
            fig1 = px.pie(type_counts, names='CR type', values='Count', title="Modules in SAP", hole=0.4)
            st.plotly_chart(fig1, use_container_width=True)
            
        with chart_col2:
            # 2. average number of process (Line Chart with Markers)
            month_counts = df.groupby('Month').size().reset_index(name='Total CRs')
            fig2 = px.line(month_counts, x='Month', y='Total CRs', title="average number of process", markers=True)
            st.plotly_chart(fig2, use_container_width=True)
            
        st.markdown("---")
        
        # Visualizations Row 2: Interactive Process Filter
        st.subheader("Areas of expertise in SAP")
        st.write("Use the filter below to select specific processes you want to analyze.")
        
        # Create a list of all unique processes
        all_processes = df['Process'].dropna().unique().tolist()
        
        # 3. Interactive Filter / Dropdown for Process
        selected_processes = st.multiselect(
            "Select Processes to View:", 
            options=all_processes, 
            default=all_processes # Show all by default
        )
        
        # Only draw the chart if at least one process is selected
        if selected_processes:
            filtered_df = df[df['Process'].isin(selected_processes)]
            process_counts = filtered_df['Process'].value_counts().reset_index()
            process_counts.columns = ['Process', 'Count']
            
            fig3 = px.bar(process_counts, x='Process', y='Count', title="Areas of expertise in SAP", color='Process', text='Count')
            fig3.update_traces(textposition='outside')
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("⚠️ Please select at least one process from the dropdown menu to view the chart.")
            
        st.markdown("---")
        
        # ==========================================
        # NEW SECTION: INTERACTIVE GLOBE CHART
        # ==========================================
        st.subheader("Global Reach & Supported Regions")
        st.write("Regions and markets managed across global Master Data operations.")
        
        # Define the regions worked with (Mapped Chugai to Japan)
        regions_list = [
            "United States", "Canada", "Mexico", "Brazil", "Costa Rica", 
            "Argentina", "Germany", "Switzerland", "Austria", "Poland", 
            "Spain", "China", "Japan", "India", "Singapore", 
            "Australia", "New Zealand"
        ]
        
        # Create a DataFrame for Plotly to read
        globe_df = pd.DataFrame({
            "Country": regions_list,
            "Worked": [1] * len(regions_list) # Dummy variable to color the map
        })
        
        # Create the 3D orthographic globe using Choropleth
        fig_globe = px.choropleth(
            globe_df,
            locations="Country",
            locationmode="country names",
            color="Worked",
            hover_name="Country",
            projection="orthographic", # This makes it a 3D globe!
            color_continuous_scale="Viridis" # A professional color scheme
        )
        
        # Clean up the look of the globe
        fig_globe.update_layout(
            coloraxis_showscale=False, # Hide the color legend
            geo=dict(
                showocean=True, oceancolor="#cce5ff", # Light blue oceans
                showland=True, landcolor="#f2f2f2",   # Grey land for non-selected
                showlakes=False,
                projection_rotation=dict(lon=-45, lat=20, roll=0) # Starts facing North America/Europe
            ),
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig_globe, use_container_width=True)
        
        # Expandable Raw Data Table
        with st.expander("🔍 View Raw Tracker Data"):
            st.dataframe(df, use_container_width=True)
            
    except Exception as e:
        st.error(f"⚠️ Unable to load the tracker dashboard. Error: {e}")
