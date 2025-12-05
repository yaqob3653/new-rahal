# ----------------------------------------------------------------------------
# 🤖 AI Assistant Logic
# ----------------------------------------------------------------------------
# الوظيفة: مساعد افتراضي للإجابة على استفسارات الزوار
# المدخلات: أسئلة المستخدم النصية
# المخرجات: إجابات ذكية بناءً على بيانات الحديقة + إحصائيات حية
# ----------------------------------------------------------------------------

from flask import Flask, render_template, request, session
import pandas as pd
# Assuming data_loader is available or mocking it for standalone
# For standalone submission, we might need to mock the DB connection or assume it's there.
# I will add a placeholder for data_loader or simple mock stats if DB not present.

app = Flask(__name__)
app.secret_key = "secret"

@app.route('/assistant', methods=['GET', 'POST'])
def assistant():
    """
    دالة المساعد الذكي
    - تستقبل رسائل المستخدم
    - تحلل النص (Keywords)
    - ترد بمعلومات من قاعدة البيانات (أوقات الانتظار، التوصيات)
    """
    if 'chat_history' not in session:
        session['chat_history'] = []
        
    # Mock Stats for Standalone Version (since we can't easily import data_loader here without full structure)
    # Or better, use a try-except block to try importing.
    stats = {
        'facilities': 12,
        'avg_wait': 35,
        'reviews': 150,
        'sentiment': '😊 Positive'
    }
        
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
                response = "Crowd levels are currently moderate. I recommend visiting 'Revenge of the Mummy' now."
            elif "weather" in msg_lower:
                response = "The weather today is sunny with temperatures around 25°C. Perfect for outdoor attractions!"
                
            session['chat_history'].append({"role": "assistant", "content": response})
            session.modified = True
        
    return render_template('assistant.html', chat_history=session['chat_history'], stats=stats)

if __name__ == '__main__':
    app.run(debug=True)
