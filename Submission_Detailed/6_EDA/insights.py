# ----------------------------------------------------------------------------
# 🔍 Park Insights (EDA) Logic
# ----------------------------------------------------------------------------
# الوظيفة: التحليل الاستكشافي للبيانات (Exploratory Data Analysis)
# المدخلات: جميع البيانات التاريخية ( انتظار، حضور)
# المخرجات: رسوم بيانية متقدمة وتحليلات إحصائية
# ----------------------------------------------------------------------------

from flask import Flask, render_template
from supabase import create_client
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import plotly

app = Flask(__name__)
supabase = create_client("URL", "KEY")

@app.route('/insights')
def insights():
    """
    دالة التحليل الاستكشافي
    - تعرض 3 تبويبات: الحضور، الانتظار، تنشئ رسوم بيانية تفاعلية لكل قسم
    - تعرض البيانات الخام في جداول
    """
    # 1. Fetch Data
    wait_res = supabase.table("waiting_times").select("*").limit(1000).execute()
    vis_res = supabase.table("visitors").select("*").limit(500).execute()
    
    df_wait = pd.DataFrame(wait_res.data)
    df_vis = pd.DataFrame(vis_res.data)
    
    # 2. Generate Charts
    # Attendance Trend
    daily = df_wait.groupby('work_date')['wait_time_max'].sum().reset_index()
    fig_trend = px.area(daily, x='work_date', y='wait_time_max', title='Attendance Trend')
    trend_json = json.dumps(fig_trend, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Visitor Age Dist
    fig_age = px.histogram(df_vis, x='age', title='Age Distribution')
    age_json = json.dumps(fig_age, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Prepare Data Tables
    attendance_data = df_wait.head(50).to_dict('records')
    visitors_data = df_vis.head(50).to_dict('records')

    return render_template('insights.html', 
                           trend_json=trend_json, 
                           age_json=age_json,
                           attendance_data=attendance_data,
                           visitors_data=visitors_data)

if __name__ == '__main__':
    app.run(debug=True)
