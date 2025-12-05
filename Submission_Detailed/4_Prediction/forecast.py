# ----------------------------------------------------------------------------
# 📊 Crowd Forecast Logic
# ----------------------------------------------------------------------------
# الوظيفة: التنبؤ بمستوى الزحام باستخدام نموذج Prophet
# المدخلات: درجة الحرارة، الرطوبة، هل هو يوم عطلة؟
# المخرجات: عدد الزوار المتوقع
# ملاحظة: يمكن تشغيل هذا الكود على Google Colab
# ----------------------------------------------------------------------------

from flask import Flask, render_template, request, session
import joblib
import pandas as pd
import requests

app = Flask(__name__)

# Load Model
try:
    crowd_model = joblib.load("crowd_model.pkl")
except:
    crowd_model = None

@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    """
    دالة التنبؤ بالزحام
    - تستقبل مدخلات الطقس
    - تستخدم نموذج Prophet للتنبؤ
    - تدعم الاتصال بـ Colab
    """
    prediction = None
    colab_url = ""
    
    if request.method == 'POST':
        colab_url = request.form.get('colab_url', '')
        temp = float(request.form.get('temp'))
        humidity = float(request.form.get('humidity'))
        is_weekend = int(request.form.get('is_weekend'))
        
        # 1. Try Remote Colab API
        if colab_url:
            try:
                # إرسال الطلب إلى Colab
                response = requests.post(f"{colab_url}/predict", json={
                    'features': [temp, humidity, is_weekend]
                })
                if response.status_code == 200:
                    prediction = int(response.json()['prediction'])
            except Exception as e:
                print(f"Colab Error: {e}")
        
        # 2. Local Prediction (Fallback)
        if prediction is None and crowd_model:
            future = pd.DataFrame({
                'ds': [pd.Timestamp.now()],
                'temperature': [temp],
                'humidity': [humidity],
                'is_weekend': [is_weekend == 1]
            })
            forecast = crowd_model.predict(future)
            prediction = int(forecast['yhat'].values[0])

    return render_template('forecast.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
