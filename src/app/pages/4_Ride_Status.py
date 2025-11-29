import streamlit as st
import time
from src.app.config import SUPABASE_URL, SUPABASE_KEY

if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("Please login first.")
    time.sleep(1)
    st.switch_page("main.py")
    st.stop()

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client

# Load environment variables


def init_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# Page Config
st.set_page_config(page_title="Facility Analysis | Rahhal", page_icon="🎡", layout="wide")

# Custom CSS
def local_css(file_name):
    with open(file_name, encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("src/app/style.css")

from src.app.utils.ui_components import render_page_header

render_page_header(
    title="Facility Operations Center",
    subtitle="Real-time Ride Performance & Status",
    lottie_url="https://lottie.host/f06068cc-8949-4e62-b88f-6932603aca1f/8KTreeanyv.lottie"  # Using the same high-quality park animation
)

# --- Real Data Loading ---
# --- Real Data Loading ---
@st.cache_data(ttl=1) # Reduced TTL for debugging, can increase later
def load_facility_data():
    if not supabase:
        return pd.DataFrame()
    
    try:
        # 1. Get Facilities
        fac_response = supabase.table("facilities").select("*").execute()
        df_fac = pd.DataFrame(fac_response.data)
        
        if df_fac.empty:
            return pd.DataFrame()
        
        # 2. Get Latest Wait Times
        # Fetch a larger sample to ensure we cover most facilities
        wait_response = supabase.table("waiting_times").select("entity_description_short, wait_time_max, capacity").limit(500).order("work_date", desc=True).execute()
        df_wait = pd.DataFrame(wait_response.data)
        
        if df_wait.empty:
            # If no wait times, still return facilities but with 0 wait
            df_fac['wait'] = 0
            df_fac['capacity'] = 100
            df_fac['status'] = "Open" # Assume open if no data? Or "Unknown"
            df_fac['name'] = df_fac['facility_name']
            return df_fac

        # Aggregate to get "current" status
        df_status = df_wait.groupby('entity_description_short').agg({
            'wait_time_max': 'mean',
            'capacity': 'mean'
        }).reset_index()
        
        # Merge
        # Use lower case for matching to be safe
        df_fac['match_name'] = df_fac['facility_name'].str.lower().str.strip()
        df_status['match_name'] = df_status['entity_description_short'].str.lower().str.strip()
        
        df_merged = pd.merge(df_fac, df_status, on='match_name', how='left')
        
        # Clean up
        df_merged['wait'] = df_merged['wait_time_max'].fillna(0).astype(int)
        df_merged['capacity'] = df_merged['capacity'].fillna(100).astype(int)
        
        # Status logic
        def get_status(row):
            if row['wait'] == 0: return "Open" # If wait is 0, it might just be empty, not closed.
            if row['wait'] > 60: return "High Traffic"
            return "Open"
            
        df_merged['status'] = df_merged.apply(get_status, axis=1)
        df_merged['name'] = df_merged['facility_name']
        
        return df_merged
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df_facilities = load_facility_data()

if df_facilities.empty:
    st.warning("No facility data found in database.")
    # Fallback structure to prevent crash if DB is empty
    df_facilities = pd.DataFrame(columns=['name', 'status', 'wait', 'capacity', 'type'])


# --- Dashboard Layout ---

# 1. Overview Metrics
m1, m2, m3, m4 = st.columns(4)

if not df_facilities.empty:
    total_open = len(df_facilities[df_facilities['status'] == 'Open'])
    avg_wait = df_facilities[df_facilities['status'] == 'Open']['wait'].mean()
    if pd.isna(avg_wait): avg_wait = 0
    
    if not df_facilities['wait'].empty and df_facilities['wait'].max() > 0:
        max_wait_ride = df_facilities.loc[df_facilities['wait'].idxmax()]
        max_wait_val = max_wait_ride['wait']
        max_wait_name = max_wait_ride['name']
    else:
        max_wait_val = 0
        max_wait_name = "N/A"
    
    # Calculate total throughput from capacity (sum of all open facilities)
    total_throughput = df_facilities[df_facilities['status'] == 'Open']['capacity'].sum()
    if pd.isna(total_throughput): total_throughput = 0
    throughput_display = f"{total_throughput/1000:.1f}k" if total_throughput >= 1000 else f"{total_throughput:.0f}"
else:
    total_open = 0
    avg_wait = 0
    max_wait_val = 0
    max_wait_name = "N/A"
    throughput_display = "0"

with m1:
    st.markdown(f"""
    <div class="card" style="border-left-color: #A6D86B;">
        <h4>Operational Status</h4>
        <p class="big-stat">{total_open}/{len(df_facilities)}</p>
        <p style="color: green;">Rides Active</p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="card" style="border-left-color: #F57C00;">
        <h4>Avg Wait Time</h4>
        <p class="big-stat">{avg_wait:.0f} min</p>
        <p style="color: #F57C00;">Moderate Load</p>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="card" style="border-left-color: #D92B7D;">
        <h4>Highest Wait</h4>
        <p class="big-stat">{max_wait_val} min</p>
        <p style="font-size: 0.8rem;">{max_wait_name}</p>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="card" style="border-left-color: #142C63;">
        <h4>Total Throughput</h4>
        <p class="big-stat">{throughput_display}</p>
        <p style="color: #142C63;">Guests/Hour</p>
    </div>
    """, unsafe_allow_html=True)

# 2. Facility Details Grid
st.markdown("### 🎢 Ride Status Board")

# Filter
col_filter, _ = st.columns([1, 3])
with col_filter:
    status_filter = st.multiselect("Filter by Status", ["Open", "Closed", "Maintenance", "Scheduled"], default=["Open", "Maintenance"])

filtered_df = df_facilities[df_facilities['status'].isin(status_filter)]

# Display Cards Grid
cols = st.columns(3)
for i, row in filtered_df.iterrows():
    status_color = "#A6D86B" if row['status'] == "Open" else "#D92B7D"
    if row['status'] == "Maintenance": status_color = "#F57C00"
    if row['status'] == "Scheduled": status_color = "#142C63"
    
    with cols[i % 3]:
        st.markdown(f"""<div class="card" style="border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid rgba(0,0,0,0.05); background: white; padding: 20px; position: relative; overflow: hidden; transition: transform 0.3s ease;"><div style="position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: {status_color};"></div><div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;"><div><h4 style="color: #142C63; font-weight: 700; margin: 0 0 5px 0; font-size: 1.1rem;">{row['name']}</h4><p style="color: #64748b; font-size: 0.85rem; margin: 0; font-weight: 500;">{row['type']}</p></div><span style="background-color: {status_color}15; color: {status_color}; padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 0.75rem; letter-spacing: 0.5px; text-transform: uppercase;">{row['status']}</span></div><div style="display: flex; gap: 15px; margin-bottom: 20px;"><div style="flex: 1; background: #F8FAFC; padding: 12px; border-radius: 12px; text-align: center;"><p style="font-size: 0.75rem; color: #64748b; margin-bottom: 4px; text-transform: uppercase; font-weight: 600;">Wait Time</p><p style="font-weight: 800; font-size: 1.2rem; color: #142C63; margin: 0;">{row['wait']} <span style="font-size: 0.8rem; font-weight: 500;">min</span></p></div><div style="flex: 1; background: #F8FAFC; padding: 12px; border-radius: 12px; text-align: center;"><p style="font-size: 0.75rem; color: #64748b; margin-bottom: 4px; text-transform: uppercase; font-weight: 600;">Capacity</p><p style="font-weight: 800; font-size: 1.2rem; color: #142C63; margin: 0;">{row['capacity']}<span style="font-size: 0.8rem; font-weight: 500;">%</span></p></div></div><div style="background-color: #F1F5F9; height: 6px; border-radius: 3px; overflow: hidden;"><div style="width: {row['capacity']}%; background: linear-gradient(90deg, {status_color} 0%, {status_color}dd 100%); height: 100%; border-radius: 3px;"></div></div></div>""", unsafe_allow_html=True)

# 3. Analytics Charts
st.markdown("### 📈 Performance Analytics")
c1, c2 = st.columns(2)

with c1:
    st.markdown("#### Wait Time Distribution")
    fig_bar = px.bar(filtered_df, x='name', y='wait', color='wait',
                     color_continuous_scale=['#A6D86B', '#F57C00', '#D92B7D'],
                     labels={'wait': 'Minutes', 'name': 'Facility'})
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit", size=12, color="#142C63"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#E0E0E0'),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.markdown("#### Capacity Utilization")
    fig_scatter = px.scatter(filtered_df, x='wait', y='capacity', size='capacity', color='type',
                             hover_name='name', size_max=40,
                             color_discrete_sequence=['#142C63', '#F57C00', '#D92B7D', '#A6D86B'])
    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit", size=12, color="#142C63"),
        xaxis=dict(title='Wait Time (min)', showgrid=True, gridcolor='#E0E0E0'),
        yaxis=dict(title='Capacity (%)', showgrid=True, gridcolor='#E0E0E0')
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
