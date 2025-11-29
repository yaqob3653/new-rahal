import streamlit as st
import time
from src.app.config import SUPABASE_URL, SUPABASE_KEY

if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("Please login first.")
    time.sleep(1)
    st.switch_page("main.py")
    st.stop()

import pandas as pd
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
st.set_page_config(page_title="EDA & Insights | Rahhal", page_icon="🔍", layout="wide")

# Custom CSS
def local_css(file_name):
    with open(file_name, encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("src/app/style.css")

from src.app.utils.ui_components import render_page_header

render_page_header(
    title="Exploratory Data Analysis",
    subtitle="Deep Dive into Park Data",
    lottie_url="https://lottie.host/d162a475-bccd-4613-828d-42ed00268a55/rvWKCI5xyM.lottie"  # Using the same high-quality data animation
)

# --- Data Loading ---
@st.cache_data
def load_data(table_name, limit=1000):
    if supabase:
        response = supabase.table(table_name).select("*").limit(limit).execute()
        return pd.DataFrame(response.data)
    return pd.DataFrame()

# Tabs for different datasets
tab1, tab2, tab3 = st.tabs(["📊 Attendance", "⏳ Waiting Times", "👥 Visitors Profile"])

with tab1:
    st.markdown("### Attendance Patterns")
    df_attendance = load_data("attendance")
    
    if not df_attendance.empty:
        # Convert date
        if 'usage_date' in df_attendance.columns:
            df_attendance['usage_date'] = pd.to_datetime(df_attendance['usage_date'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Daily Attendance Trend")
            fig_att = px.line(df_attendance, x='usage_date', y='attendance', color='facility_name',
                              title="Attendance by Facility")
            fig_att.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Outfit", size=12, color="#142C63")
            )
            st.plotly_chart(fig_att, use_container_width=True)
            
        with col2:
            st.markdown("#### Attendance Distribution")
            fig_hist = px.histogram(df_attendance, x='attendance', color='facility_name', nbins=30)
            fig_hist.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Outfit", size=12, color="#142C63")
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            
        st.markdown("#### Raw Data")
        st.dataframe(df_attendance, use_container_width=True)
    else:
        st.info("Loading data or no data available...")

with tab2:
    st.markdown("### Waiting Times Analysis")
    df_wait = load_data("waiting_times", limit=500)
    
    if not df_wait.empty:
        # Clean data: fill NaN values in nb_units with a default value
        if 'nb_units' in df_wait.columns:
            df_wait['nb_units'] = df_wait['nb_units'].fillna(1)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Wait Time vs Capacity")
            fig_scatter = px.scatter(df_wait, x='wait_time_max', y='capacity', color='entity_description_short',
                                     size='nb_units', hover_data=['work_date'])
            fig_scatter.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Outfit", size=12, color="#142C63")
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with col2:
            st.markdown("#### Wait Time Heatmap (Hour vs Entity)")
            # Need to process hour if available, else mock for demo
            if 'deb_time_hour' in df_wait.columns:
                fig_heat = px.density_heatmap(df_wait, x='deb_time_hour', y='entity_description_short', z='wait_time_max',
                                              color_continuous_scale='Viridis')
                fig_heat.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Outfit", size=12, color="#142C63")
                )
                st.plotly_chart(fig_heat, use_container_width=True)
                
        st.markdown("#### Raw Data")
        st.dataframe(df_wait, use_container_width=True)
    else:
        st.info("Loading data or no data available...")

with tab3:
    st.markdown("### Visitor Demographics")
    df_visitors = load_data("visitors", limit=500)
    
    if not df_visitors.empty:
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown("#### Age Distribution")
            fig_age = px.histogram(df_visitors, x='age', nbins=20, color_discrete_sequence=['#F57C00'])
            fig_age.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Outfit", size=12, color="#142C63")
            )
            st.plotly_chart(fig_age, use_container_width=True)
            
        with c2:
            st.markdown("#### Group Type")
            if 'accompanied_with' in df_visitors.columns:
                fig_group = px.pie(df_visitors, names='accompanied_with', hole=0.5,
                                   color_discrete_sequence=px.colors.qualitative.Bold)
                fig_group.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Outfit", size=12, color="#142C63")
                )
                st.plotly_chart(fig_group, use_container_width=True)
                
        with c3:
            st.markdown("#### Weight Distribution")
            fig_weight = px.box(df_visitors, y='weight_kg', color_discrete_sequence=['#D92B7D'])
            fig_weight.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Outfit", size=12, color="#142C63")
            )
            st.plotly_chart(fig_weight, use_container_width=True)
            
        st.markdown("#### Raw Data")
        st.dataframe(df_visitors, use_container_width=True)
    else:
        st.info("Loading data or no data available...")
