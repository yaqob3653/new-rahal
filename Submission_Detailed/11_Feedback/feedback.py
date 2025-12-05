# ----------------------------------------------------------------------------
# 💬 Visitor Feedback Logic
# ----------------------------------------------------------------------------
# الوظيفة: تحليل تقييمات الزوار باستخدام معالجة اللغات الطبيعية (NLP)
# المدخلات: نصوص التقييمات من قاعدة البيانات
# المخرجات: تحليل المشاعر (إيجابي/سلبي) ورسوم بيانية
# ----------------------------------------------------------------------------

from flask import Flask, render_template
from supabase import create_client
import plotly.express as px
import pandas as pd
import json
import plotly

app = Flask(__name__)
supabase = create_client("URL", "KEY")

@app.route('/feedback')
def feedback():
    """
    دالة تحليل المشاعر
    - تجلب التقييمات من جدول reviews
    - تحسب نسبة الرضا
    - تعرض توزيع المشاعر
    """
    response = supabase.table("reviews").select("*").limit(500).execute()
    df = pd.DataFrame(response.data)
    
    # Calculate Sentiment Logic
    avg_sentiment = df['sentiment_score'].mean()
    positive_pct = (df['sentiment_score'] > 0).mean() * 100
    
    # Charts
    fig_pie = px.pie(df, names='sentiment_label', title='Sentiment Distribution')
    pie_json = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('feedback.html', 
                           avg_sentiment=avg_sentiment,
                           positive_pct=positive_pct,
                           pie_json=pie_json)

if __name__ == '__main__':
    app.run(debug=True)
