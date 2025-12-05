# ----------------------------------------------------------------------------
# 🔐 Login Page Logic
# ----------------------------------------------------------------------------
# الوظيفة: إدارة عملية تسجيل الدخول والتحقق من المستخدمين
# المدخلات: البريد الإلكتروني، كلمة المرور
# المخرجات: توجيه للموحة التحكم أو رسالة خطأ
# ----------------------------------------------------------------------------

from flask import Flask, render_template, request, redirect, url_for, session, flash
from supabase import create_client
import os

app = Flask(__name__)
app.secret_key = "secret"

# Supabase Setup (Placeholder)
SUPABASE_URL = "YOUR_URL"
SUPABASE_KEY = "YOUR_KEY"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/', methods=['GET', 'POST'])
def login():
    """
    دالة تسجيل الدخول
    - تتحقق من صحة البيانات
    - تنشئ جلسة للمستخدم
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # Demo Mode
        if email == "demo@rahhal.com" and password == "demo123":
            session['user'] = {"email": email, "role": role}
            flash('Login Successful! (Demo Mode)', 'success')
            return redirect(url_for('dashboard'))

        # Real Supabase Auth
        try:
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            session['user'] = {"email": res.user.email, "role": role}
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Login Failed: {str(e)}', 'danger')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
