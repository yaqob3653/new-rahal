import streamlit as st
import time
import streamlit.components.v1 as components
from src.app.data_service import get_supabase_client

def login_page():
    """
    Renders the login and registration page.
    """
    # Hide all Streamlit UI elements and apply styles
    st.markdown("""
    <style>
        /* Hide Streamlit UI */
        header, footer, #MainMenu, [data-testid="stToolbar"], 
        [data-testid="stDecoration"], [data-testid="stStatusWidget"],
        [data-testid="stHeader"], [data-testid="stSidebar"] {
            display: none !important;
        }
        
        .main, .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* Blue Gradient Background for the App */
        .stApp {
            background: linear-gradient(135deg, #142C63 0%, #0f2147 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 80px 20px 20px 20px;
        }
        
        /* The Row Container (The Card) */
        [data-testid="stHorizontalBlock"] {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
            max-width: 1000px;
            margin: auto;
            align-items: stretch;
        }
        
        /* Left Column (Blue Brand Panel) */
        [data-testid="stHorizontalBlock"] > div:nth-child(1) {
            background: linear-gradient(135deg, #142C63 0%, #1e40af 100%) !important;
            padding: 0 !important;
        }
        
        /* Right Column (White Form Panel) */
        [data-testid="stHorizontalBlock"] > div:nth-child(2) {
            background: white !important;
            padding: 0 !important;
        }
        
        /* Inner Content Padding */
        .left-content {
            padding: 60px 40px;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white !important;
        }
        
        .left-content h1, .left-content p, .left-content div {
            color: white !important;
        }
        
        /* Input Styling */
        .stTextInput > div > div > input {
            background-color: #F8FAFC !important;
            border: 2px solid #BCC5D6 !important;
            border-radius: 10px !important;
            padding: 16px !important;
            font-size: 15px !important;
            color: #142C63 !important;
            transition: all 0.3s !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #F57C00 !important;
            box-shadow: 0 0 0 3px rgba(245, 124, 0, 0.1) !important;
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #F57C00 0%, #FF9800 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 16px !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            width: 100% !important;
            margin-top: 20px !important;
            transition: all 0.3s !important;
            box-shadow: 0 4px 15px rgba(245, 124, 0, 0.4) !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(245, 124, 0, 0.6) !important;
            background: linear-gradient(135deg, #D92B7D 0%, #E91E63 100%) !important;
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            border-bottom: 2px solid #BCC5D6;
            margin-bottom: 20px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 12px 20px;
            color: #64748b;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            color: #F57C00;
            border-bottom: 3px solid #F57C00;
        }
        
        /* Fix Checkbox */
        .stCheckbox label {
            color: #64748b !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Use Streamlit Columns for the Layout
    col1, col2 = st.columns([1, 1])
    
    # LEFT COLUMN: Branding
    with col1:
        st.markdown("""
        <div class="left-content" style="position: relative;">
            <div style="margin-top: 60px;"></div>
        """, unsafe_allow_html=True)
        
        # --- Login Animation Video ---
        import base64
        try:
            with open("src/app/assets/logo.mp4", "rb") as f:
                login_video_b64 = base64.b64encode(f.read()).decode()
            
            video_html = f"""
                <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-bottom: 15px;">
                    <video width="85%" height="250px" autoplay loop muted playsinline style="border-radius: 15px; border: 3px solid rgba(255, 255, 255, 0.3); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); object-fit: cover;">
                        <source src="data:video/mp4;base64,{login_video_b64}" type="video/mp4">
                    </video>
                </div>
            """
            st.markdown(video_html, unsafe_allow_html=True)
        except Exception as e:
            # Fallback to Lottie if video fails
            lottie_html = """
                <script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script> 
                <dotlottie-player 
                    src="https://lottie.host/3de805f3-9654-44bb-8255-d99bd5cde31c/aYjjLtCtfW.lottie" 
                    background="transparent" 
                    speed="1" 
                    style="width: 100%; height: 280px;" 
                    loop 
                    autoplay>
                </dotlottie-player>
            """
            components.html(lottie_html, height=300)
        
        st.markdown("""
            <h1 style="font-size: 3.5rem; font-weight: 900; margin: 10px 0; text-align: center; text-shadow: 0 2px 10px rgba(0,0,0,0.2); color: white;">Rahhal</h1>
            <p style="font-size: 1.2rem; line-height: 1.8; opacity: 0.95; max-width: 400px; margin: 0 auto; text-align: center; color: white;">
                Advanced Analytics Platform<br>
                for Theme Park Excellence
            </p>
            <div style="margin-top: 40px; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 10px; backdrop-filter: blur(10px);">
                <p style="font-size: 0.9rem; margin: 0; opacity: 0.9; color: white;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h20"/><path d="M20 12v6a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-6"/><path d="M12 2a10 10 0 0 1 10 10"/><path d="M12 22a10 10 0 0 1 10-10"/><circle cx="12" cy="12" r="2"/></svg>
                        <span>Real-time Insights</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                        <span>Predictive Analytics</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8" y2="16"/><line x1="16" y1="16" x2="16" y2="16"/></svg>
                        <span>AI-Powered Recommendations</span>
                    </div>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # RIGHT COLUMN: Form or Legal Content
    with col2:
        # Initialize view state
        if 'current_view' not in st.session_state:
            st.session_state['current_view'] = 'login'
            
        view = st.session_state['current_view']
        
        if view == 'login':
            st.markdown("""
            <div style="padding: 60px 50px 20px 50px;">
                <h2 style="font-size: 2rem; font-weight: 700; color: #1e40af; margin: 0 0 10px 0;">Welcome Back</h2>
                <p style="color: #64748b; font-size: 1rem; margin: 0 0 30px 0;">Sign in to access your dashboard</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Inject a container with padding for the form
            with st.container():
                 st.markdown('<div style="margin: 0 50px;">', unsafe_allow_html=True)
                 
                 tab1, tab2 = st.tabs(["Login", "Register"])
                 
                 with tab1:
                     with st.form("login_form", clear_on_submit=False):
                         email = st.text_input("Email Address", placeholder="admin@rahhal.com", key="login_email")
                         password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
                         
                         # Role selection
                         role = st.selectbox("Login as", ["Admin", "Visitor"], key="login_role")
                         
                         col_rem, col_forgot = st.columns([1, 1])
                         with col_rem:
                             st.checkbox("Remember me", key="remember")
                         with col_forgot:
                             st.markdown('<p style="text-align: right; margin-top: 8px;"><a href="#" style="color: #3b82f6; text-decoration: none; font-size: 14px;">Forgot Password?</a></p>', unsafe_allow_html=True)
                         
                         submit = st.form_submit_button("Sign In")
                         
                         if submit:
                             if not email or not password:
                                 st.error("Please enter both email and password", icon=":material/error:")
                             else:
                                 # Demo mode bypass for testing
                                 if email == "demo@rahhal.com" and password == "demo123":
                                     st.session_state['authenticated'] = True
                                     st.session_state['user'] = {"email": "demo@rahhal.com"}
                                     st.session_state['role'] = role
                                     st.success("Login Successful! (Demo Mode)", icon=":material/check_circle:")
                                     time.sleep(0.5)
                                     st.rerun()
                                 else:
                                     # NETWORK DIAGNOSTIC
                                     import requests
                                     import socket
                                     from urllib.parse import urlparse
                                     
                                     st.write("--- Network Diagnostic ---")
                                     from src.app.config import SUPABASE_URL
                                     
                                     # 1. Check DNS Resolution
                                     try:
                                         domain = urlparse(SUPABASE_URL).netloc
                                         st.write(f"Resolving domain: {domain}")
                                         ip = socket.gethostbyname(domain)
                                         st.success(f"DNS Resolved: {ip}")
                                     except Exception as e:
                                         st.error(f"DNS Failed: {e}")
                                     
                                     # 2. Check HTTP Reachability
                                     try:
                                         st.write(f"Pinging: {SUPABASE_URL}")
                                         r = requests.get(SUPABASE_URL, timeout=5)
                                         st.success(f"HTTP Status: {r.status_code}")
                                     except Exception as e:
                                         st.error(f"HTTP Failed: {e}")
                                     st.write("--------------------------")

                                     try:
                                         supabase = get_supabase_client()
                                         if supabase:
                                             # Authenticate with Supabase
                                             res = supabase.auth.sign_in_with_password({
                                                 "email": email, 
                                                 "password": password
                                             })
                                             
                                             # Set session state with selected role
                                             st.session_state['authenticated'] = True
                                             st.session_state['user'] = res.user
                                             st.session_state['role'] = role  # Use selected role
                                             
                                             st.success("✅ Login Successful!")
                                             time.sleep(0.5)
                                             st.rerun()
                                         else:
                                             st.error("❌ Database connection error. Please check your .env file.")
                                     except Exception as e:
                                         error_msg = str(e)
                                         if "Invalid login credentials" in error_msg:
                                             st.error("❌ Invalid email or password")
                                         elif "Email not confirmed" in error_msg:
                                             st.error("❌ Please verify your email first")
                                         else:
                                             st.error(f"❌ Login failed: {error_msg}")
                 
                 with tab2:
                     with st.form("register_form", clear_on_submit=False):
                         new_email = st.text_input("Email Address", placeholder="your.email@example.com", key="reg_email")
                         new_password = st.text_input("Password", type="password", placeholder="Minimum 6 characters", key="reg_pass")
                         confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="reg_confirm")
                         
                         submit_reg = st.form_submit_button("Create Account")
                         
                         if submit_reg:
                             if not new_email or not new_password or not confirm_password:
                                 st.error("❌ Please fill in all fields")
                             elif new_password != confirm_password:
                                 st.error("❌ Passwords do not match")
                             elif len(new_password) < 6:
                                 st.error("❌ Password must be at least 6 characters")
                             else:
                                 try:
                                     supabase = get_supabase_client()
                                     if supabase:
                                         # Register new user with Supabase
                                         res = supabase.auth.sign_up({
                                             "email": new_email, 
                                             "password": new_password
                                         })
                                         
                                         if res.user:
                                             st.success("✅ Account created successfully! Please check your email to verify your account.")
                                             st.info("📧 A verification link has been sent to your email address.")
                                         else:
                                             st.error("❌ Registration failed. Please try again.")
                                 except Exception as e:
                                     st.error(f"❌ Registration Error: {e}")

def logout():
    """
    Handles user logout.
    """
    st.session_state['authenticated'] = False
    st.session_state['role'] = None
    st.rerun()
