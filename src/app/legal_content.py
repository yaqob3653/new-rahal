import streamlit as st

def show_header(title, icon):
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #1e40af; font-size: 2.5rem; margin-bottom: 10px;">{icon} {title}</h1>
        <div style="height: 4px; width: 60px; background: linear-gradient(90deg, #3b82f6, #8b5cf6); margin: 0 auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)

def show_back_button():
    if st.button("← Back to Login", type="secondary", use_container_width=True):
        st.session_state['current_view'] = 'login'
        st.rerun()

def show_contact_us():
    show_header("Contact Us", "📞")
    
    st.markdown("""
    <div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;">
        <h3 style="color: #334155; margin-bottom: 20px;">Get in Touch</h3>
        <p style="color: #64748b; margin-bottom: 30px;">We'd love to hear from you. Please fill out the form below or reach out to us directly.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("First Name", placeholder="John")
        with col2:
            st.text_input("Last Name", placeholder="Doe")
        
        st.text_input("Email Address", placeholder="john@example.com")
        st.selectbox("Subject", ["General Inquiry", "Technical Support", "Business Partnership", "Feedback"])
        st.text_area("Message", placeholder="How can we help you?", height=150)
        
        st.form_submit_button("Send Message", type="primary", use_container_width=True)

    st.markdown("""
    <div style="margin-top: 30px; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
        <div style="background: #f8fafc; padding: 20px; border-radius: 10px; text-align: center;">
            <div style="font-size: 24px; margin-bottom: 10px;">📍</div>
            <div style="font-weight: bold; color: #334155;">Visit Us</div>
            <div style="color: #64748b; font-size: 0.9rem;">King Abdullah II St.<br>Amman, Jordan</div>
        </div>
        <div style="background: #f8fafc; padding: 20px; border-radius: 10px; text-align: center;">
            <div style="font-size: 24px; margin-bottom: 10px;">📧</div>
            <div style="font-weight: bold; color: #334155;">Email Us</div>
            <div style="color: #64748b; font-size: 0.9rem;">support@rahhal.com<br>info@rahhal.com</div>
        </div>
        <div style="background: #f8fafc; padding: 20px; border-radius: 10px; text-align: center;">
            <div style="font-size: 24px; margin-bottom: 10px;">📱</div>
            <div style="font-weight: bold; color: #334155;">Call Us</div>
            <div style="color: #64748b; font-size: 0.9rem;">+962 6 555 0123<br>+962 79 555 0123</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    show_back_button()

def show_terms():
    show_header("Terms of Use", "📜")
    
    st.markdown("""
    <div style="background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); color: #475569; line-height: 1.6;">
        <h3 style="color: #1e293b;">1. Acceptance of Terms</h3>
        <p>By accessing and using the Rahhal Analytics Platform, you agree to be bound by these Terms of Use and all applicable laws and regulations.</p>
        
        <h3 style="color: #1e293b; margin-top: 20px;">2. Use License</h3>
        <p>Permission is granted to temporarily access the materials (information or software) on Rahhal's website for personal, non-commercial transitory viewing only.</p>
        
        <h3 style="color: #1e293b; margin-top: 20px;">3. Data Privacy</h3>
        <p>Your use of the platform is also governed by our Privacy Policy. We are committed to protecting your personal information and usage data.</p>
        
        <h3 style="color: #1e293b; margin-top: 20px;">4. Analytics & Reporting</h3>
        <p>The analytics provided by Rahhal are for informational purposes only. While we strive for accuracy, we do not guarantee the absolute precision of crowd predictions or wait times.</p>
        
        <h3 style="color: #1e293b; margin-top: 20px;">5. Modifications</h3>
        <p>Rahhal reserves the right to revise these terms of service for its website at any time without notice. By using this website you are agreeing to be bound by the then current version of these terms of service.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    show_back_button()

def show_privacy():
    show_header("Privacy Policy", "🔒")
    
    st.markdown("""
    <div style="background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); color: #475569; line-height: 1.6;">
        <h3 style="color: #1e293b;">1. Information We Collect</h3>
        <p>We collect information you provide directly to us, such as when you create an account, update your profile, or request customer support. This may include your name, email address, and usage preferences.</p>
        
        <h3 style="color: #1e293b; margin-top: 20px;">2. How We Use Your Information</h3>
        <p>We use the information we collect to provide, maintain, and improve our services, including to:</p>
        <ul>
            <li>Process transactions and send related information.</li>
            <li>Send you technical notices, updates, security alerts, and support messages.</li>
            <li>Respond to your comments, questions, and requests.</li>
        </ul>
        
        <h3 style="color: #1e293b; margin-top: 20px;">3. Data Security</h3>
        <p>We implement appropriate technical and organizational measures to protect your personal data against unauthorized or unlawful processing, accidental loss, destruction, or damage.</p>
        
        <h3 style="color: #1e293b; margin-top: 20px;">4. Cookies</h3>
        <p>We use cookies and similar tracking technologies to track the activity on our Service and hold certain information to improve your experience.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    show_back_button()
