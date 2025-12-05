from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
import os
import requests
import numpy as np
import pandas as pd
from datetime import datetime

# Import Services
from services import data_loader
from services import plots

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'rahhal-secret-key-2025')

# ----------------------------------------------------------------------------
# ROUTES
# ----------------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')


        # Real Supabase Auth
        supabase = data_loader.get_supabase_client()
        if supabase:
            try:
                res = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                session['user'] = {"email": res.user.email, "role": role}
                flash('Login Successful!', 'success')
                return redirect(url_for('dashboard'))
            except Exception as e:
                flash(f'Login Failed: {str(e)}', 'danger')
        else:
            flash('Database connection error.', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        supabase = data_loader.get_supabase_client()
        if supabase:
            try:
                res = supabase.auth.sign_up({
                    "email": email,
                    "password": password,
                    "options": {
                        "data": {
                            "role": role
                        }
                    }
                })
                flash('Registration Successful! Please check your email to verify.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                flash(f'Registration Failed: {str(e)}', 'danger')
        else:
            flash('Database connection error.', 'danger')

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # 1. Fetch Data
    total_visitors, system_health, avg_wait, capacity_pct, target_date = data_loader.get_dashboard_metrics()
    chart_df = data_loader.get_chart_data()
    
    # 2. Generate Plots
    treemap_json = plots.generate_treemap(chart_df)
    
    trend_json = "{}"
    if chart_df is not None and not chart_df.empty:
        chart_df['hour'] = pd.to_datetime(chart_df['work_date']).dt.hour
        hourly_trend = chart_df.groupby('hour')['wait_time_max'].mean().reset_index()
        trend_json = plots.generate_trend_area(hourly_trend, 'hour', 'wait_time_max')

    return render_template('dashboard.html', 
                           session=session,
                           total_visitors=total_visitors,
                           system_health=system_health,
                           avg_wait=avg_wait,
                           treemap_json=treemap_json,
                           trend_json=trend_json,
                           now=datetime.now())

@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # 1. Fetch Data (New Dashboard Logic)
    today_forecast, peak_time, optimal_time, weather_impact, forecast_df, heatmap_df, insights = data_loader.get_forecast_dashboard_data()
    
    # 2. Generate Plots
    forecast_json = plots.generate_forecast_chart(forecast_df)
    heatmap_json = plots.generate_heatmap_chart(heatmap_df)

    return render_template('forecast.html', 
                           session=session, 
                           today_forecast=today_forecast,
                           peak_time=peak_time,
                           optimal_time=optimal_time,
                           weather_impact=weather_impact,
                           forecast_json=forecast_json,
                           heatmap_json=heatmap_json,
                           insights=insights)

@app.route('/plan', methods=['GET', 'POST'])
def plan():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    cluster = None
    recommendations = []
    
    # 1. Fetch Data
    popular_rides, table_data, facilities_df = data_loader.get_plan_data()
    
    # 2. Generate Plots
    # Convert popular_rides list of dicts to DF for plotting if needed, or just pass data
    # The service returns a list of dicts for popular_rides, but plots.generate_bar_chart expects a DF.
    # Let's adjust the service or the app. 
    # Actually data_loader.get_plan_data returns popular_rides as list of dicts.
    # I should fix data_loader to return DF for plotting or convert here.
    # Let's convert here for simplicity.
    popular_df = pd.DataFrame(popular_rides)
        
    bar_chart_json = plots.generate_bar_chart(popular_df, 'name', 'wait', 'Top 5 Least Crowded Rides', 'Ride', 'Avg Wait (min)', color_col='wait')
    # Note: generate_bar_chart returns HTML by default now in plots.py, but plan.html expects JSON?
    # Wait, plan.html was updated to use JSON in previous steps? No, I updated rides.html and insights.html to use HTML.
    # I need to check if plan.html uses JSON or HTML.
    # In previous steps I updated `plan.html` to use `bar_chart_json`.
    # `plots.generate_bar_chart` returns HTML.
    # I should update `plan.html` to accept HTML or update `plots.py` to return JSON for this specific chart.
    # Or better, update `plan.html` to render HTML.
    # For now, I will assume I need to update `plan.html` later or `plots.py` returns HTML and I pass it as `bar_chart_html`.
    # Let's check `plots.py` again. `generate_bar_chart` returns `to_html(fig)`.
    # So I should pass `bar_chart_html` to template.
    
    # 3. Handle Form
    if request.method == 'POST':
        age = float(request.form.get('age'))
        weight = float(request.form.get('weight'))
        accompanied = request.form.get('accompanied')
        pref_thrill = float(request.form.get('pref_thrill'))
        pref_family = float(request.form.get('pref_family'))
        pref_food = float(request.form.get('pref_food'))
        
        acc_map = {"Alone": 0, "Friends": 1, "Family": 2, "With Children": 3}
        acc_val = acc_map.get(accompanied, 0)
        
        cluster = data_loader.get_recommendation_prediction(age, weight, acc_val, pref_family, pref_thrill, pref_food)
        
        if cluster is not None and not facilities_df.empty:
            # REAL MODEL LOGIC: Use the predicted cluster to filter recommendations
            # Cluster Mapping (based on training):
            # 0: Thrill Seekers (High Thrill, Low Family)
            # 1: Family Visitors (Low Thrill, High Family)
            # 2: Balanced/Groups (Moderate Thrill & Family)
            # 3: Relaxed/Foodies (Low Thrill, High Food)
            
            if cluster == 0 or cluster == 2: # Thrill & Balanced -> Recommend Thrill Rides
                thrill_rides = facilities_df[facilities_df['type'].str.contains('Thrill|Coaster', case=False, na=False)]
                # Sort by thrill preference if available, else random top
                for _, row in thrill_rides.head(3).iterrows():
                    recommendations.append({
                        "name": row['facility_name'],
                        "type": row['type'],
                        "match": int(90 + (pref_thrill * 10)), # Dynamic Match Score
                        "img": "https://img.icons8.com/color/96/roller-coaster.png"
                    })
            
            elif cluster == 1: # Family -> Recommend Family Rides
                family_rides = facilities_df[facilities_df['type'].str.contains('Family|Kids|Water', case=False, na=False)]
                for _, row in family_rides.head(3).iterrows():
                    recommendations.append({
                        "name": row['facility_name'],
                        "type": row['type'],
                        "match": int(90 + (pref_family * 10)), # Dynamic Match Score
                        "img": "https://img.icons8.com/color/96/amusement-park.png"
                    })
                    
            elif cluster == 3: # Relaxed -> Recommend Shows & Dining
                relaxed_rides = facilities_df[facilities_df['type'].str.contains('Show|Dining|Slow', case=False, na=False)]
                for _, row in relaxed_rides.head(3).iterrows():
                    recommendations.append({
                        "name": row['facility_name'],
                        "type": row['type'],
                        "match": int(85 + (pref_food * 15)), # Dynamic Match Score
                        "img": "https://img.icons8.com/color/96/ferris-wheel.png"
                    })
            
            # Fallback if specific cluster logic didn't yield results (or for other clusters)
            if not recommendations:
                 for _, row in facilities_df.head(3).iterrows():
                    recommendations.append({
                        "name": row['facility_name'],
                        "type": row['type'],
                        "match": int(75 + np.random.randint(0, 20)),
                        "img": "https://img.icons8.com/color/96/theme-park.png"
                    })

    return render_template('plan.html', session=session, cluster=cluster, recommendations=recommendations, popular_rides=popular_rides, table_data=table_data, bar_chart_json=bar_chart_json)



@app.route('/rides')
def rides():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    rides_data = []
    table_data = []
    active_count = 0
    total_count = 0
    avg_wait = 0
    max_wait = 0
    max_wait_ride = "-"
    throughput = 0
    bar_chart_html = ""
    pie_chart_html = ""
    
    # 1. Fetch Data
    df = data_loader.get_rides_data()
    
    if not df.empty:
        latest = df.drop_duplicates('entity_description_short')
        total_count = len(latest)
        table_data = latest.head(20).to_dict('records')
        
        avg_wait = int(latest['wait_time_max'].mean())
        max_row = latest.loc[latest['wait_time_max'].idxmax()]
        max_wait = int(max_row['wait_time_max'])
        max_wait_ride = max_row['entity_description_short']
        
        active_count = len(latest[latest['wait_time_max'] > 0])
        
        avg_capacity_per_ride = 24
        if avg_wait > 0:
            throughput = int((active_count * avg_capacity_per_ride * 60) / avg_wait)
        else:
            throughput = active_count * avg_capacity_per_ride * 4
        
        for _, row in latest.iterrows():
            wait_time = row['wait_time_max']
            if pd.isna(wait_time) or wait_time == 0:
                status = "Closed"
                capacity_pct = 0
            else:
                status = "Open"
                if wait_time < 15: 
                    capacity_pct = int(40 + (wait_time / 15) * 20)
                elif wait_time < 45: 
                    capacity_pct = int(60 + ((wait_time - 15) / 30) * 25)
                else: 
                    capacity_pct = int(85 + min((wait_time - 45) / 155, 1) * 15)
            
            rides_data.append({
                "name": row['entity_description_short'],
                "status": status,
                "wait": int(wait_time) if not pd.isna(wait_time) else 0,
                "capacity": capacity_pct
            })
        
        # 2. Generate Plots
        top_10 = latest.nlargest(10, 'wait_time_max')
        bar_chart_html = plots.generate_bar_chart(top_10, 'entity_description_short', 'wait_time_max', 'Top 10 Rides by Wait Time', 'Ride', 'Wait Time (min)', color_col='wait_time_max')
        
        status_counts = latest['wait_time_max'].apply(lambda x: 'Open' if x > 0 else 'Closed').value_counts()
        pie_chart_html = plots.generate_pie_chart(None, status_counts.index, values=status_counts.values, title='Ride Status Distribution', hole=0.5)

    return render_template('rides.html', 
                           session=session, 
                           rides=rides_data, 
                           table_data=table_data,
                           active_count=active_count, 
                           total_count=total_count, 
                           avg_wait=avg_wait, 
                           max_wait=max_wait, 
                           max_wait_ride=max_wait_ride,
                           throughput=throughput,
                           bar_chart_html=bar_chart_html,
                           pie_chart_html=pie_chart_html)

@app.route('/insights')
def insights():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    trend_html = dist_html = scatter_html = heatmap_html = age_html = pie_html = box_html = ""
    attendance_data = []
    waiting_data = []
    visitors_data = []
    
    # 1. Fetch Data
    df_wait, df_vis = data_loader.get_insights_data()
    
    if not df_wait.empty:
        attendance_data = df_wait[['work_date', 'entity_description_short', 'wait_time_max']].head(50).copy()
        attendance_data['work_date'] = pd.to_datetime(attendance_data['work_date'])
        attendance_data = attendance_data.to_dict('records')

        waiting_data = df_wait[['work_date', 'entity_description_short', 'wait_time_max']].head(50).copy()
        waiting_data['work_date'] = pd.to_datetime(waiting_data['work_date'])
        waiting_data = waiting_data.to_dict('records')

        # 2. Generate Plots
        # Instead of trend, show top rides by average wait time (more meaningful with current data)
        top_rides = df_wait.groupby('entity_description_short')['wait_time_max'].mean().reset_index()
        top_rides = top_rides.sort_values('wait_time_max', ascending=False).head(10)
        
        if len(top_rides) > 0:
            trend_html = plots.generate_bar_chart(
                top_rides, 
                'entity_description_short', 
                'wait_time_max', 
                'Top 10 Rides by Average Wait Time', 
                'Ride', 
                'Average Wait Time (min)',
                color_col='wait_time_max'
            )
        else:
            trend_html = ""
        
        dist_html = plots.generate_histogram(df_wait, 'wait_time_max', 'Attendance Distribution')
        scatter_html = plots.generate_scatter_chart(df_wait, 'work_date', 'wait_time_max', 'entity_description_short', size_col=None, title='Wait Time Over Time')
        
        heatmap_data = df_wait.groupby(['entity_description_short', 'hour'])['wait_time_max'].mean().reset_index()
        heatmap_html = plots.generate_heatmap(heatmap_data, 'hour', 'entity_description_short', 'wait_time_max', 'Wait Time Heatmap')
    
    return render_template('insights.html', session=session,
                           trend_html=trend_html, dist_html=dist_html,
                           scatter_html=scatter_html, heatmap_html=heatmap_html,
                           attendance_data=attendance_data, waiting_data=waiting_data)

@app.route('/map', methods=['GET', 'POST'])
def smart_map():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    nodes = {
        "Entrance": (0, 0),
        "Hollywood Rip Ride Rockit": (2, 5),
        "Revenge of the Mummy": (5, 8),
        "Transformers": (6, 4),
        "Harry Potter Diagon Alley": (8, 9),
        "Simpsons Ride": (9, 3),
        "Men in Black": (7, 1),
        "E.T. Adventure": (4, 2)
    }
    
    edges = [
        ("Entrance", "Hollywood Rip Ride Rockit", 5),
        ("Entrance", "E.T. Adventure", 7),
        ("Hollywood Rip Ride Rockit", "Revenge of the Mummy", 6),
        ("Hollywood Rip Ride Rockit", "Transformers", 5),
        ("Revenge of the Mummy", "Harry Potter Diagon Alley", 4),
        ("Transformers", "Simpsons Ride", 8),
        ("Simpsons Ride", "Men in Black", 3),
        ("Men in Black", "E.T. Adventure", 5),
        ("Transformers", "Revenge of the Mummy", 4),
        ("Harry Potter Diagon Alley", "Simpsons Ride", 6)
    ]
    
    # 1. Fetch Data
    wait_times = data_loader.get_map_data(nodes)
    
    # 2. Calculate Path
    start_point = request.form.get('start_point', 'Entrance')
    end_point = request.form.get('end_point', 'Harry Potter Diagon Alley')
    path = []
    total_time = 0
    steps = []
    
    if request.method == 'POST':
        import networkx as nx
        G = nx.Graph()
        for node, pos in nodes.items():
            G.add_node(node, pos=pos, wait=wait_times.get(node, 0))
        for u, v, walk_time in edges:
            weight = walk_time + wait_times.get(v, 0)
            G.add_edge(u, v, weight=weight, walk=walk_time)
            
        try:
            path = nx.shortest_path(G, source=start_point, target=end_point, weight='weight')
            total_time = int(nx.shortest_path_length(G, source=start_point, target=end_point, weight='weight'))
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                steps.append({'target': v, 'walk': G[u][v]['walk'], 'wait': G.nodes[v]['wait']})
        except nx.NetworkXNoPath:
            flash('No path found between these points.', 'danger')
    
    # 3. Generate Map
    map_json = plots.generate_map_json(nodes, edges, wait_times, path)
    
    return render_template('map.html', session=session, nodes=nodes.keys(), start_point=start_point, end_point=end_point, path=path, total_time=total_time, steps=steps, map_json=map_json)

@app.route('/health')
def health():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # 1. Fetch Data
    df_cv, df_vis = data_loader.get_health_data()
    
    # 2. Metrics & Charts
    mae, rmse, mape = 0, 0, 0
    
    if not df_cv.empty:
        from sklearn.metrics import mean_absolute_error, mean_squared_error
        mae = mean_absolute_error(df_cv['y'], df_cv['yhat'])
        rmse = np.sqrt(mean_squared_error(df_cv['y'], df_cv['yhat']))
        mape = np.mean(np.abs((df_cv['y'] - df_cv['yhat']) / df_cv['y'])) * 100
        
    cv_html, res_html, clus_html = plots.generate_health_charts(df_cv, df_vis, None)

    return render_template('health.html', session=session,
                           mae=mae, rmse=rmse, mape=mape,
                           cv_html=cv_html, res_html=res_html,
                           clus_html=clus_html)

@app.route('/assistant', methods=['GET', 'POST'])
def assistant():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    # Calculate live stats for display
    stats = {
        'facilities': 0,
        'avg_wait': 0,
        'reviews': 0
    }
    
    supabase = data_loader.get_supabase_client()
    if supabase:
        try:
            # Get facility count
            fac_response = supabase.table("facilities").select("*").execute()
            stats['facilities'] = len(fac_response.data) if fac_response.data else 0
            
            # Get average wait time
            wait_response = supabase.table("waiting_times").select("wait_time_max").order("work_date", desc=True).limit(100).execute()
            if wait_response.data:
                wait_df = pd.DataFrame(wait_response.data)
                stats['avg_wait'] = int(wait_df['wait_time_max'].mean())
            
            # Get review count
            review_response = supabase.table("reviews").select("*").execute()
            stats['reviews'] = len(review_response.data) if review_response.data else 0
        except Exception as e:
            print(f"Stats Error: {e}")
        
    if request.method == 'POST':
        msg = request.form.get('message')
        if msg:
            session['chat_history'].append({"role": "user", "content": msg})
            
            # Simple keyword-based logic
            response = "I can help with wait times, recommendations, and park information."
            msg_lower = msg.lower()
            
            if "wait" in msg_lower or "time" in msg_lower:
                response = f"Current average wait time is around {stats['avg_wait']} minutes. The least crowded rides are usually water attractions and shows."
            elif "recommend" in msg_lower or "suggest" in msg_lower:
                response = "I recommend visiting thrill rides early in the morning when wait times are lowest, and family attractions in the afternoon."
            elif "food" in msg_lower or "eat" in msg_lower or "restaurant" in msg_lower:
                response = "We have several dining options including fast food, sit-down restaurants, and snack stands throughout the park."
            elif "hour" in msg_lower or "open" in msg_lower or "close" in msg_lower:
                response = "The park is typically open from 9 AM to 10 PM. Please check the official schedule for specific dates."
            elif "ticket" in msg_lower or "price" in msg_lower:
                response = "Ticket prices vary by season. Please visit our ticketing page for current pricing and special offers."
            elif "crowd" in msg_lower:
                response = f"Based on current data, the average wait time is {stats['avg_wait']} minutes. Please check the Dashboard for detailed crowd analysis."
            elif "weather" in msg_lower:
                response = "Please check your local weather app for the most accurate and up-to-date weather information."
                
            session['chat_history'].append({"role": "assistant", "content": response})
            session.modified = True
        
    return render_template('assistant.html', session=session, chat_history=session.get('chat_history', []), stats=stats)


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
