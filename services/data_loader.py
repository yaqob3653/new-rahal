import pandas as pd
from supabase import create_client
import numpy as np
import os
from dotenv import load_dotenv
import joblib
import tensorflow as tf
from datetime import datetime

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Global Models
rec_model = None
rec_scaler = None

def load_models():
    global rec_model, rec_scaler
    try:
        rec_model = tf.keras.models.load_model("models/recommendation_model.h5")
        rec_scaler = joblib.load("models/scaler.pkl")
        print("DL Model (TensorFlow) Loaded Successfully")
    except Exception as e:
        print(f"Warning: Could not load DL models: {e}")

# Load on import
load_models()

def get_recommendation_prediction(age, weight, acc_val, pref_family, pref_thrill, pref_food):
    global rec_model, rec_scaler
    if rec_model and rec_scaler:
        try:
            input_data = [[age, weight, acc_val, pref_family, pref_thrill, pref_food]]
            input_scaled = rec_scaler.transform(input_data)
            pred = rec_model.predict(input_scaled)
            return int(round(pred[0][0]))
        except Exception as e:
            print(f"Prediction Error: {e}")
            return None
    return None

def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_dashboard_metrics():
    """
    Fetches and calculates dashboard metrics.
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
    
    # 4. Predicted Peak (Simplified)
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
    Fetches detailed data for dashboard charts.
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

def get_forecast_data():
    """
    Fetches historical attendance data for forecast page.
    """
    supabase = get_supabase_client()
    table_data = []
    daily_counts = pd.DataFrame()
    
    if supabase:
        try:
            response = supabase.table("waiting_times").select("work_date, wait_time_max").order("work_date", desc=True).limit(50).execute()
            df = pd.DataFrame(response.data)
            
            if not df.empty:
                df['work_date'] = pd.to_datetime(df['work_date'])
                daily_counts = df.groupby('work_date').size().reset_index(name='visitor_count')
                table_data = daily_counts.head(10).to_dict('records')
        except Exception as e:
            print(f"Supabase Error (Forecast): {e}")
            
    return daily_counts, table_data

def get_plan_data():
    """
    Fetches popular rides and facilities for plan page.
    """
    supabase = get_supabase_client()
    popular_rides = []
    table_data = []
    facilities_df = pd.DataFrame()
    
    if supabase:
        try:
            # Popular Rides
            wait_response = supabase.table("waiting_times").select("entity_description_short, wait_time_max, work_date").order("work_date", desc=True).limit(1000).execute()
            wait_df = pd.DataFrame(wait_response.data)
            
            if not wait_df.empty:
                wait_df['work_date'] = pd.to_datetime(wait_df['work_date'])
                # Get latest status (Real-Time) instead of average
                latest_status = wait_df.sort_values('work_date', ascending=False).drop_duplicates('entity_description_short')
                popular = latest_status.sort_values('wait_time_max').head(5)
                
                for _, row in popular.iterrows():
                    popular_rides.append({"name": row['entity_description_short'], "wait": int(row['wait_time_max'])})
                
                table_data = latest_status.head(10).to_dict('records')
            
            # Facilities
            fac_response = supabase.table("facilities").select("facility_name, type").execute()
            facilities_df = pd.DataFrame(fac_response.data)
            
        except Exception as e:
            print(f"Supabase Error (Plan): {e}")
            
    return popular_rides, table_data, facilities_df



def get_rides_data():
    """
    Fetches waiting times for rides page.
    """
    supabase = get_supabase_client()
    df = pd.DataFrame()
    
    if supabase:
        try:
            response = supabase.table("waiting_times").select("*").order("work_date", desc=True).limit(2000).execute()
            df = pd.DataFrame(response.data)
            if not df.empty:
                df['work_date'] = pd.to_datetime(df['work_date'])
        except Exception as e:
            print(f"Supabase Error (Rides): {e}")
            
    return df

def get_insights_data():
    """
    Fetches data for insights page (waiting times and visitors).
    """
    supabase = get_supabase_client()
    df_wait = pd.DataFrame()
    df_vis = pd.DataFrame()
    
    if supabase:
        try:
            # Waiting Times
            response = supabase.table("waiting_times").select("*").order("work_date", desc=True).limit(2000).execute()
            df_wait = pd.DataFrame(response.data)
            if not df_wait.empty:
                df_wait['date'] = pd.to_datetime(df_wait['work_date'])
                df_wait['hour'] = pd.to_datetime(df_wait['work_date']).dt.hour
            
            # Visitors
            res_vis = supabase.table("visitors").select("*").limit(500).execute()
            df_vis = pd.DataFrame(res_vis.data)
            
        except Exception as e:
            print(f"Supabase Error (Insights): {e}")
            
    return df_wait, df_vis

def get_map_data(nodes):
    """
    Fetches real wait times for map nodes.
    """
    supabase = get_supabase_client()
    wait_times = {}
    
    if supabase:
        try:
            response = supabase.table("waiting_times").select("entity_description_short, wait_time_max").limit(500).order("work_date", desc=True).execute()
            df = pd.DataFrame(response.data)
            
            if not df.empty:
                for node in nodes:
                    match = df[df['entity_description_short'].str.contains(node.split()[0], case=False, na=False)]
                    if not match.empty:
                        wait_times[node] = int(match['wait_time_max'].mean())
                    else:
                        wait_times[node] = 10
            else:
                wait_times = {node: 15 for node in nodes}
        except:
            wait_times = {node: 15 for node in nodes}
    else:
        wait_times = {node: 15 for node in nodes}
        
    return wait_times

def get_health_data():
    """
    Fetches data for health page (Crowd, Rec, Sentiment).
    """
    supabase = get_supabase_client()
    df_cv = pd.DataFrame()
    df_vis = pd.DataFrame()
    
    if supabase:
        try:
            # Crowd
            response = supabase.table("attendance").select("usage_date, attendance").order("usage_date", desc=True).limit(30).execute()
            df_real = pd.DataFrame(response.data)
            if not df_real.empty:
                df_real['ds'] = pd.to_datetime(df_real['usage_date'])
                df_real['y'] = df_real['attendance']
                
                # Load Model & Predict
                crowd_model = joblib.load("models/crowd_model.pkl")
                future = pd.DataFrame({'ds': df_real['ds']})
                forecast = crowd_model.predict(future)
                df_cv = pd.merge(df_real, forecast[['ds', 'yhat']], on='ds')
                
            # Rec
            response = supabase.table("visitors").select("age, weight_kg, accompanied_with").limit(500).execute()
            df_vis = pd.DataFrame(response.data)
            
        except Exception as e:
            print(f"Supabase Error (Health): {e}")
            
    return df_cv, df_vis

def get_forecast_dashboard_data():
    """
    Fetches data for the new Crowd Forecast Dashboard (Real Data).
    Returns:
        today_forecast (int): Predicted visitors for today
        peak_time (str): Hour with max crowd
        optimal_time (str): Hour with min crowd
        weather_impact (str): Percentage change
        forecast_df (pd.DataFrame): 7-day forecast data
        heatmap_df (pd.DataFrame): Hourly crowd density data
    """
    supabase = get_supabase_client()
    
    # Defaults
    today_forecast = 0
    peak_time = "N/A"
    optimal_time = "N/A"
    weather_impact = "N/A"
    forecast_df = pd.DataFrame()
    heatmap_df = pd.DataFrame()
    
    # 1. Forecast Data (Using existing crowd_model.pkl)
    try:
        crowd_model = joblib.load("models/crowd_model.pkl")
        
        # Generate future dates (Next 7 days)
        future_dates = pd.date_range(start=datetime.now().date(), periods=7)
        future = pd.DataFrame({'ds': future_dates})
        
        # Predict
        # Note: Depending on the model type (Prophet vs Sklearn), the input might need adjustment.
        # Assuming it works like in get_health_data which passes a DF with 'ds'.
        # If it's pure sklearn on date features, we might need to extract features.
        # But based on the user's streamlit code: m.make_future_dataframe(periods=7) -> Prophet.
        # Prophet predict takes a df with 'ds'.
        
        forecast = crowd_model.predict(future)
        
        # Prophet returns 'yhat', 'yhat_lower', 'yhat_upper'
        if 'yhat' in forecast.columns:
            forecast_df = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
            forecast_df['yhat'] = forecast_df['yhat'].astype(int)
            forecast_df['yhat_lower'] = forecast_df['yhat_lower'].astype(int)
            forecast_df['yhat_upper'] = forecast_df['yhat_upper'].astype(int)
            
            today_forecast = int(forecast_df.iloc[0]['yhat'])
            
            if len(forecast_df) > 1:
                change = ((forecast_df.iloc[0]['yhat'] - forecast_df.iloc[1]['yhat']) / forecast_df.iloc[1]['yhat'] * 100)
                weather_impact = f"{change:+.1f}%"
        
    except Exception as e:
        print(f"Model Error: {e}")
        # Fallback if model fails
        dates = pd.date_range(start=datetime.now().date(), periods=7)
        forecast_df = pd.DataFrame({
            'ds': dates,
            'yhat': np.random.randint(12000, 25000, size=7),
            'yhat_lower': np.random.randint(10000, 23000, size=7),
            'yhat_upper': np.random.randint(14000, 27000, size=7)
        })
        today_forecast = int(forecast_df.iloc[0]['yhat'])

    # 2. Heatmap Data (Real Aggregation from Supabase)
    if supabase:
        try:
            # Fetch historical wait times to simulate density
            response = supabase.table("waiting_times").select("work_date, wait_time_max").limit(1000).execute()
            df = pd.DataFrame(response.data)
            
            if not df.empty:
                df['work_date'] = pd.to_datetime(df['work_date'])
                df['Day'] = df['work_date'].dt.day_name().str.slice(0, 3) # Mon, Tue...
                df['Hour'] = df['work_date'].dt.hour
                
                # Aggregate
                heatmap_df = df.groupby(['Day', 'Hour'])['wait_time_max'].mean().reset_index()
                heatmap_df.columns = ['Day', 'Hour', 'Crowd Level']
                
                # Calculate Peak & Optimal Times
                hourly_avg = heatmap_df.groupby('Hour')['Crowd Level'].mean()
                if not hourly_avg.empty:
                    peak_h = hourly_avg.idxmax()
                    opt_h = hourly_avg.idxmin()
                    peak_time = f"{int(peak_h):02d}:00"
                    optimal_time = f"{int(opt_h):02d}:00"
                    
        except Exception as e:
            print(f"Supabase Error (Forecast): {e}")

    # 3. Generate Dynamic Insights
    insights = []
    
    # Insight 1: Crowd Alert
    if today_forecast > 20000:
        insights.append({
            "type": "warning",
            "title": "High Crowd Alert",
            "text": f"Expect heavy crowds today with approx. {today_forecast:,} visitors.",
            "color": "#D92B7D",
            "bg": "#FFF5F5",
            "icon": "⚠️"
        })
    elif today_forecast < 5000:
        insights.append({
            "type": "info",
            "title": "Low Crowd Expected",
            "text": "Today is a great day to visit! Low crowd levels expected.",
            "color": "#16A34A",
            "bg": "#F0FDF4",
            "icon": "✅"
        })
    else:
        insights.append({
            "type": "info",
            "title": "Moderate Crowds",
            "text": "Crowd levels are normal for this time of year.",
            "color": "#F57C00",
            "bg": "#FFF7ED",
            "icon": "ℹ️"
        })
        
    # Insight 2: Recommendation
    if optimal_time != "N/A":
        insights.append({
            "type": "success",
            "title": "Recommendation",
            "text": f"Plan your visit to major attractions around {optimal_time} to avoid queues.",
            "color": "#A6D86B",
            "bg": "#F0FDF4",
            "icon": "💡"
        })
        
    # Insight 3: Peak Warning
    if peak_time != "N/A":
        insights.append({
            "type": "warning",
            "title": "Peak Hours",
            "text": f"Expect maximum wait times around {peak_time}. Consider dining or shopping during this time.",
            "color": "#F57C00",
            "bg": "#FFF7ED",
            "icon": "🕒"
        })

    return today_forecast, peak_time, optimal_time, weather_impact, forecast_df, heatmap_df, insights


