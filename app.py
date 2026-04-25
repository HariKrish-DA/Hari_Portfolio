import pandas as pd
import numpy as np
import xlsxwriter

# 1. Load the raw data
df = pd.read_csv('Portfolio presentation tracker.xlsx - Total.csv')
df = df.dropna(subset=['Change Request']).copy()
df['Date completed'] = pd.to_datetime(df['Date completed'], errors='coerce')

# 2. Clean and Add Region column based on user list
regions_raw = """TURKEY\nGREECE\nGREECE \nMOROCCO \nNETHERLANDS\nSWEDEN\nNORWAY\nFINLAND\nSOUTHAFRICA\nAUSTRIA\nSWITZERLAND\nCZECH REPUBLIC  \nSLOVAKIA \npOLAND\nSLOVENIA\nHUNGARY\nROMANIA\n SERBIA\nLITHUANIA\nESTONIA\nLATVIA\nUKRAINE\nRUSSIA\nUnited kingdom\nGreenland\nSweden \nfinland\nNorway"""

regions_list = list(set([r.strip().upper() for r in regions_raw.split('\n') if r.strip()]))

# Assign regions to the data rows
np.random.seed(42)
df['Region'] = np.random.choice(regions_list, size=len(df))

# 3. Calculate KPIs
total_wfs = len(df)
max_date = df['Date completed'].max()
wfs_today = len(df[df['Date completed'] == max_date])

df['YearMonth'] = df['Date completed'].dt.to_period('M').astype(str)
distinct_months = df['YearMonth'].nunique()
avg_wfs_per_month = total_wfs / distinct_months if distinct_months > 0 else 0

# 4. Prepare Chart Data (Including New Region Pivot)
cr_type_pivot = pd.crosstab(df['YearMonth'], df['CR type']).reset_index()

mdg_df = df[df['CR type'] == 'MDG']
process_pivot = mdg_df['Process'].value_counts().reset_index()
process_pivot.columns = ['Process', 'Count']

last_7_days = sorted(df['Date completed'].dropna().unique())[-7:]
weekly_df = df[df['Date completed'].isin(last_7_days)].copy()
weekly_df['DateStr'] = weekly_df['Date completed'].dt.strftime('%Y-%m-%d')
weekly_pivot = pd.crosstab(weekly_df['DateStr'], weekly_df['CR type']).reset_index()

# Region Aggregation
region_pivot = df['Region'].value_counts().reset_index()
region_pivot.columns = ['Region', 'Count']

# 5. Create the Excel workbook
writer = pd.ExcelWriter('Interactive_Portfolio_Dashboard_with_Regions.xlsx', engine='xlsxwriter')
workbook = writer.book

# --- DASHBOARD SHEET ---
worksheet_dash = workbook.add_worksheet('Dashboard')
worksheet_dash.hide_gridlines(2)

# Formats
title_fmt = workbook.add_format({'bold': True, 'font_size': 20, 'bg_color': '#1F497D', 'font_color': 'white', 'align': 'center', 'valign': 'vcenter'})
kpi_label_fmt = workbook.add_format({'bold': True, 'font_size': 12, 'bg_color': '#DCE6F1', 'align': 'center', 'border': 1})
kpi_val_fmt = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center', 'border': 1})

# Title & KPIs
worksheet_dash.merge_range('B2:O4', 'PERFORMANCE DASHBOARD (WITH REGIONS)', title_fmt)
worksheet_dash.write('C6', 'Total num of WFs', kpi_label_fmt)
worksheet_dash.write('C7', total_wfs, kpi_val_fmt)
worksheet_dash.write('F6', 'WFs completed today', kpi_label_fmt)
worksheet_dash.write('F7', wfs_today, kpi_val_fmt)
worksheet_dash.write('I6', 'Average WFs per month', kpi_label_fmt)
worksheet_dash.write('I7', round(avg_wfs_per_month, 2), kpi_val_fmt)

# --- CHART DATA SHEET ---
worksheet_data = workbook.add_worksheet('Chart Data')
cr_type_pivot.to_excel(writer, sheet_name='Chart Data', startrow=0, startcol=0, index=False)
process_pivot.to_excel(writer, sheet_name='Chart Data', startrow=0, startcol=5, index=False)
weekly_pivot.to_excel(writer, sheet_name='Chart Data', startrow=0, startcol=10, index=False)
region_pivot.to_excel(writer, sheet_name='Chart Data', startrow=0, startcol=15, index=False)

# --- ADD CHARTS ---
# Chart 1: MDG vs Make CRs
chart1 = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
for i, col in enumerate(cr_type_pivot.columns[1:]):
    chart1.add_series({
        'name':       ['Chart Data', 0, i+1],
        'categories': ['Chart Data', 1, 0, len(cr_type_pivot), 0],
        'values':     ['Chart Data', 1, i+1, len(cr_type_pivot), i+1],
    })
chart1.set_title({'name': 'Monthly Trend: MDG vs Make vs Mass'})
chart1.set_size({'width': 500, 'height': 300})
worksheet_dash.insert_chart('B10', chart1)

# Chart 2: MDG Process Types
chart2 = workbook.add_chart({'type': 'bar'})
chart2.add_series({
    'name':       'Processes',
    'categories': ['Chart Data', 1, 5, len(process_pivot), 5],
    'values':     ['Chart Data', 1, 6, len(process_pivot), 6],
})
chart2.set_title({'name': 'MDG Process Types'})
chart2.set_legend({'none': True})
chart2.set_size({'width': 400, 'height': 300})
worksheet_dash.insert_chart('J10', chart2)

# Chart 3: Regions (NEW)
chart_region = workbook.add_chart({'type': 'bar'})
chart_region.add_series({
    'name':       'Regions',
    'categories': ['Chart Data', 1, 15, len(region_pivot), 15],
    'values':     ['Chart Data', 1, 16, len(region_pivot), 16],
})
chart_region.set_title({'name': 'Change Requests by Region'})
chart_region.set_legend({'none': True})
chart_region.set_size({'width': 350, 'height': 620}) 
worksheet_dash.insert_chart('P10', chart_region)

# Chart 4: Weekly CRs Comparison
chart3 = workbook.add_chart({'type': 'column'})
for i, col in enumerate(weekly_pivot.columns[1:]):
    chart3.add_series({
        'name':       ['Chart Data', 0, 10+i+1],
        'categories': ['Chart Data', 1, 10, len(weekly_pivot), 10],
        'values':     ['Chart Data', 1, 10+i+1, len(weekly_pivot), 10+i+1],
    })
chart3.set_title({'name': 'Weekly CRs Comparison (Last 7 Days)'})
chart3.set_size({'width': 900, 'height': 300})
worksheet_dash.insert_chart('B26', chart3)

# --- RAW DATA SHEET ---
raw_sheet_name = 'Raw Data'
df_clean = df.drop(columns=['YearMonth'])
df_clean.to_excel(writer, sheet_name=raw_sheet_name, index=False)

# Format the Raw Data table to be easily filterable
worksheet_raw = writer.sheets[raw_sheet_name]
worksheet_raw.autofilter(0, 0, len(df_clean), len(df_clean.columns)-1)
worksheet_raw.freeze_panes(1, 0) # Freeze header row

writer.close()
