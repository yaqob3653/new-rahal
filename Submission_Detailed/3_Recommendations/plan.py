# ----------------------------------------------------------------------------
# 📅 Plan Your Visit (Recommendations) Logic
# ----------------------------------------------------------------------------
# الوظيفة: تقديم توصيات شخصية للألعاب
# المدخلات: العمر، الوزن، التفضيلات (إثارة، عائلة، طعام)
# المخرجات: قائمة بالألعاب المقترحة باستخدام نموذج Deep Learning (TensorFlow)
# ----------------------------------------------------------------------------

from flask import Flask, render_template, request, session
import joblib
import tensorflow as tf
import numpy as np
import pandas as pd

app = Flask(__name__)
app.secret_key = "secret"

# Load Deep Learning Model & Scaler
try:
    rec_model = tf.keras.models.load_model("recommendation_model.h5")
    scaler = joblib.load("scaler.pkl")
    print("✅ DL Model (TensorFlow) Loaded Successfully")
except:
    rec_model = None
    scaler = None
    print("⚠️ Model not found")

@app.route('/plan', methods=['GET', 'POST'])
def plan():
    """
    دالة التوصيات
    - تستقبل بيانات الزائر من النموذج
    - تستخدم نموذج شبكة عصبية (Deep Learning) لتصنيف الزائر
    - تقترح الألعاب المناسبة للفئة (Cluster)
    """
    recommendations = []
    cluster = None
    
    if request.method == 'POST':
        try:
            # 1. Capture Inputs
            age = float(request.form.get('age'))
            weight = float(request.form.get('weight'))
            accompanied = request.form.get('accompanied')
            pref_thrill = float(request.form.get('pref_thrill'))
            pref_family = float(request.form.get('pref_family'))
            pref_food = float(request.form.get('pref_food'))
            
            # Map 'Accompanied' to numeric
            acc_map = {"Alone": 0, "Friends": 1, "Family": 2, "With Children": 3}
            acc_val = acc_map.get(accompanied, 0)
            
            # 2. Prepare Data for DL Model
            if rec_model and scaler:
                input_data = [[age, weight, acc_val, pref_family, pref_thrill, pref_food]]
                input_scaled = scaler.transform(input_data)
                
                # 3. Predict Cluster (0, 1, 2, 3)
                pred = rec_model.predict(input_scaled)
                cluster = int(round(pred[0][0]))
                
                # 4. Filter Recommendations based on Cluster
                # This simulates fetching from database
                facilities = [
                    {"name": "Roller Coaster", "type": "Thrill"},
                    {"name": "Ferris Wheel", "type": "Family"},
                    {"name": "Water Log", "type": "Family"},
                    {"name": "Drop Tower", "type": "Thrill"},
                    {"name": "Circus Show", "type": "Show"},
                    {"name": "Burger Joint", "type": "Dining"}
                ]
                df = pd.DataFrame(facilities)
                
                if cluster == 0 or cluster == 2: # Thrill
                    recs = df[df['type'] == 'Thrill']
                elif cluster == 1: # Family
                    recs = df[df['type'] == 'Family']
                else: # Relaxed/Dining
                    recs = df[df['type'].isin(['Show', 'Dining'])]
                    
                recommendations = recs.to_dict('records')
                
        except Exception as e:
            print(f"Error: {e}")
            
    return render_template('plan.html', recommendations=recommendations, cluster=cluster)

if __name__ == '__main__':
    app.run(debug=True)
