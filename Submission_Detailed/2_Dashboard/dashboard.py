# ----------------------------------------------------------------------------
# 📈 Dashboard Logic
# ----------------------------------------------------------------------------
# الوظيفة: عرض لوحة التحكم الرئيسية والمؤشرات
# المدخلات: بيانات الزوار، أوقات الانتظار من قاعدة البيانات
# المخرجات: رسوم بيانية (Treemap, Area Chart) ومؤشرات رقمية
# ----------------------------------------------------------------------------

from flask import Flask, render_template, session
from supabase import create_client
import plotly.express as px
import pandas as pd
import json
import plotly

app = Flask(__name__)

# Supabase Setup
supabase = create_client("URL", "KEY")

@app.route('/dashboard')
def dashboard():
    """
    دالة لوحة التحكم
    - تجلب البيانات الحية من Supabase
    - تحسب المؤشرات (إجمالي الزوار، متوسط الانتظار)
    - تنشئ الرسوم البيانية باستخدام Plotly
    """
    # 1. Fetch Data
    visitors = supabase.table("visitors").select("*", count="exact").execute()
    waiting = supabase.table("waiting_times").select("*").execute()
    
    # 2. Calculate Metrics
    total_visitors = visitors.count
    df_wait = pd.DataFrame(waiting.data)
    avg_wait = int(df_wait['wait_time_max'].mean())
    
    # 3. Generate Charts
    # Treemap
    fig_treemap = px.treemap(df_wait, path=['entity_description_short'], values='wait_time_max')
    treemap_json = json.dumps(fig_treemap, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Trend
    fig_trend = px.area(df_wait, x='work_date', y='wait_time_max')
    trend_json = json.dumps(fig_trend, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', 
                           total_visitors=total_visitors,
                           avg_wait=avg_wait,
                           treemap_json=treemap_json,
                           trend_json=trend_json)

if __name__ == '__main__':
    app.run(debug=True)
