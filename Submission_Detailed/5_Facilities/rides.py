# ----------------------------------------------------------------------------
# 🎡 Facility Analysis Logic
# ----------------------------------------------------------------------------
# الوظيفة: مراقبة حالة الألعاب وأوقات الانتظار
# المدخلات: بيانات المستشعرات (أوقات الانتظار)
# المخرجات: حالة كل لعبة (مفتوح/مغلق) ووقت الانتظار الحالي
# ----------------------------------------------------------------------------

from flask import Flask, render_template
from supabase import create_client
import pandas as pd

app = Flask(__name__)
supabase = create_client("URL", "KEY")

@app.route('/rides')
def rides():
    """
    دالة تحليل المرافق
    - تعرض قائمة الألعاب
    - تعرض وقت الانتظار الحالي لكل لعبة
    - تحسب متوسط وقت الانتظار في الحديقة
    """
    response = supabase.table("waiting_times").select("*").order("work_date", desc=True).limit(100).execute()
    df = pd.DataFrame(response.data)
    
    # Process latest status
    latest = df.drop_duplicates('entity_description_short')
    rides_data = latest.to_dict('records')
    
    avg_wait = int(latest['wait_time_max'].mean())
    
    return render_template('rides.html', rides=rides_data, avg_wait=avg_wait)

if __name__ == '__main__':
    app.run(debug=True)
