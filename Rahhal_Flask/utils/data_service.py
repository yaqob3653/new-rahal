import pandas as pd
from supabase import create_client
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_dashboard_metrics():
    """
    Fetches and calculates dashboard metrics (Flask Version)
    """
    supabase = get_supabase_client()
    if not supabase:
        return 0, 0, 0, 0, "N/A"
    
    # 1. Total Visitors
    try:
        latest_date_query = supabase.table("attendance").select("usage_date").order("usage_date", desc=True).limit(1).execute()
        if latest_date_query.data:
            target_date = latest_date_query.data[0]['usage_date']
            visitors_query = supabase.table("attendance").select("attendance").eq("usage_date", target_date).execute()
            visitors_df = pd.DataFrame(visitors_query.data)
            total_visitors = visitors_df['attendance'].sum() if not visitors_df.empty else 0
        else:
            target_date = "N/A"
            total_visitors = 0
    except Exception as e:
        print(f"Error fetching visitors: {e}")
        target_date = "N/A"
        total_visitors = 0

    # 2. Avg Wait Time
    try:
        wait_query = supabase.table("waiting_times").select("wait_time_max").order("work_date", desc=True).limit(100).execute()
        wait_df = pd.DataFrame(wait_query.data)
        avg_wait = int(wait_df['wait_time_max'].mean()) if not wait_df.empty else 0
    except Exception as e:
        print(f"Error fetching wait times: {e}")
        avg_wait = 0
    
    # 3. System Health
    health_penalty = (avg_wait / 60) * 50
    system_health = max(0, min(100, 100 - health_penalty))
    
    # 4. Predicted Peak (Simplified for Flask)
    try:
        peak_query = supabase.table("waiting_times").select("wait_time_max").order("wait_time_max", desc=True).limit(1).execute()
        if peak_query.data:
            capacity_pct = peak_query.data[0]['wait_time_max'] 
        else:
            capacity_pct = 0
    except:
        capacity_pct = 0

    return total_visitors, system_health, avg_wait, capacity_pct, target_date

def get_chart_data():
    """
    Fetches detailed data for charts (Flask Version)
    """
    supabase = get_supabase_client()
    if not supabase:
        return None
    
    try:
        wait_response = supabase.table("waiting_times").select("entity_description_short, wait_time_max, work_date").order("work_date", desc=True).limit(500).execute()
        wait_df = pd.DataFrame(wait_response.data)
    except Exception as e:
        print(f"Error fetching chart data: {e}")
        wait_df = pd.DataFrame()
    
    return wait_df
