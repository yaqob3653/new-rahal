import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
import os
import numpy as np
import joblib
from datetime import datetime
import streamlit as st

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_data(ttl=60)
def get_dashboard_metrics():
    """
    Fetches and calculates dashboard metrics:
    - Total Visitors
    - System Health
    - Avg Wait Time
    - Predicted Peak
    """
    supabase = get_supabase_client()
    if not supabase:
        return 0, 0, 0, 0, "N/A"
    
    # 1. Total Visitors (Sum of attendance for LATEST date)
    # Find latest date first
    latest_date_query = supabase.table("attendance").select("usage_date").order("usage_date", desc=True).limit(1).execute()
    if latest_date_query.data:
        target_date = latest_date_query.data[0]['usage_date']
        visitors_query = supabase.table("attendance").select("attendance").eq("usage_date", target_date).execute()
        visitors_df = pd.DataFrame(visitors_query.data)
        total_visitors = visitors_df['attendance'].sum() if not visitors_df.empty else 0
    else:
        target_date = "N/A"
        total_visitors = 0

    # 2. Avg Wait Time (Latest available)
    wait_query = supabase.table("waiting_times").select("wait_time_max").order("work_date", desc=True).limit(100).execute()
    wait_df = pd.DataFrame(wait_query.data)
    avg_wait = int(wait_df['wait_time_max'].mean()) if not wait_df.empty else 0
    
    # 3. System Health (Dynamic)
    # Heuristic: Health drops as wait times increase. 
    # Base 100, subtract penalty. 60 min wait = -50 health.
    health_penalty = (avg_wait / 60) * 50
    system_health = max(0, min(100, 100 - health_penalty))
    
    # 4. Predicted Peak (Data-Driven Fallback)
    try:
        model = joblib.load('src/models/crowd_model.pkl')
        # Dummy prediction for now if model exists
        capacity_pct = 85 
    except:
        # Fallback: Find hour with max wait time in history
        peak_query = supabase.table("waiting_times").select("work_date, wait_time_max").order("wait_time_max", desc=True).limit(1).execute()
        if peak_query.data:
            # peak_time = pd.to_datetime(peak_query.data[0]['work_date']).strftime("%H:%M")
            capacity_pct = peak_query.data[0]['wait_time_max'] # Using max wait as proxy for capacity/peak
        else:
            capacity_pct = 0

    return total_visitors, system_health, avg_wait, capacity_pct, target_date

@st.cache_data(ttl=60)
def get_chart_data():
    """
    Fetches detailed data for charts.
    """
    supabase = get_supabase_client()
    if not supabase:
        return None
    
    # Simplified: Just get the latest 500 records ordered by date
    # This avoids the timeout issue from checking today's date first
    wait_response = supabase.table("waiting_times").select("entity_description_short, wait_time_max, work_date").order("work_date", desc=True).limit(500).execute()
    wait_df = pd.DataFrame(wait_response.data)
    
    return wait_df
