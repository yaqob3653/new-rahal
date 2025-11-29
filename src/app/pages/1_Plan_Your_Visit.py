import streamlit as st
import time
from src.app.config import SUPABASE_URL, SUPABASE_KEY

if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("Please login first.")
    time.sleep(1)
    st.switch_page("main.py")
    st.stop()

import pandas as pd
import numpy as np
import joblib
from supabase import create_client

# Load environment variables


def init_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Load Models
@st.cache_resource
def load_models():
    try:
        model = joblib.load("src/models/recommendation_model.pkl")
        scaler = joblib.load("src/models/scaler.pkl")
        return model, scaler
    except:
        return None, None

model, scaler = load_models()
supabase = init_supabase()

# Page Config
st.set_page_config(page_title="Smart Recommendations | Rahhal", page_icon="🎯", layout="wide")

# Custom CSS
def local_css(file_name):
    with open(file_name, encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("src/app/style.css")

# Inject Fun/Disney-like CSS ONLY for this page
st.markdown("""
<style>
    /* Animated Background Gradient for this page only */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glassmorphism Cards */
    .card, div[data-testid="stExpander"], .stMetric {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }

    .card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(31, 38, 135, 0.25) !important;
        border-color: #F57C00 !important;
    }

    /* Fun Headings */
    h1, h2, h3 {
        background: linear-gradient(120deg, #142C63, #D92B7D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Interactive Buttons */
    div.stButton > button {
        background: linear-gradient(45deg, #142C63, #3b82f6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.6) !important;
        background: linear-gradient(45deg, #3b82f6, #142C63) !important;
    }
</style>
""", unsafe_allow_html=True)

from src.app.utils.ui_components import render_page_header, inject_particles, trigger_fireworks

# Inject Magical Particles
inject_particles()

render_page_header(
    title="Smart Recommendations",
    subtitle="Personalized Ride Suggestions Engine",
    lottie_url="https://lottie.host/d1cb8951-bcb4-453c-b9dc-d39edd28b796/DzWSR5Rb4p.lottie"
)

# Layout: Two columns (Input Form | Results)
col_input, col_result = st.columns([1, 2])

with col_input:
    st.markdown("""
    <div class="card">
        <h4>Visitor Profile</h4>
    """, unsafe_allow_html=True)
    
    with st.form("user_input_form"):
        age = st.number_input("Age", min_value=5, max_value=100, value=25)
        weight = st.number_input("Weight (kg)", min_value=20, max_value=150, value=70)
        accompanied = st.selectbox("Group Type", ["Alone", "Friends", "Family", "With Children"])
        
        st.markdown("#### Preferences")
        pref_thrill = st.slider("Thrill Seeking", 0.0, 1.0, 0.5)
        pref_family = st.slider("Family Oriented", 0.0, 1.0, 0.5)
        pref_food = st.slider("Foodie Score", 0.0, 1.0, 0.5)
        
        submitted = st.form_submit_button("Generate Recommendations", icon=":material/rocket_launch:")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_result:
    if submitted:
        # Trigger Celebration!
        trigger_fireworks()

        # 1. Process Input
        acc_map = {"Alone": 0, "Friends": 1, "Family": 2, "With Children": 3}
        acc_val = acc_map[accompanied]
        
        # Create input vector
        input_data = pd.DataFrame({
            'age': [age],
            'weight_kg': [weight],
            'accompanied_with': [acc_val],
            'preference_score_family': [pref_family],
            'preference_score_thrill': [pref_thrill],
            'preference_score_food': [pref_food]
        })
        
        # 2. Predict Cluster
        if model and scaler:
            try:
                input_scaled = scaler.transform(input_data)
                cluster = model.predict(input_scaled)[0]
                
                st.success(f"Profile Analyzed! You belong to Cluster: **{cluster}**")
                
                # 3. Get Real Recommendations from Database
                st.markdown("### 🎢 Recommended for You")
                
                # Fetch facilities from database
                if supabase:
                    fac_response = supabase.table("facilities").select("facility_name, type").execute()
                    facilities_df = pd.DataFrame(fac_response.data)
                    
                    if not facilities_df.empty:
                        # Filter based on preferences
                        recs = []
                        
                        if pref_thrill > 0.7:
                            # High thrill seekers
                            thrill_rides = facilities_df[facilities_df['type'].str.contains('Thrill|Coaster', case=False, na=False)]
                            for _, row in thrill_rides.head(3).iterrows():
                                match_score = int(85 + (pref_thrill * 15))
                                recs.append({
                                    "name": row['facility_name'],
                                    "type": row['type'],
                                    "match": match_score,
                                    "img": "https://img.icons8.com/color/96/roller-coaster.png"
                                })
                        elif pref_family > 0.7 or accompanied == "With Children":
                            # Family oriented
                            family_rides = facilities_df[facilities_df['type'].str.contains('Family|Show|Kids', case=False, na=False)]
                            for _, row in family_rides.head(3).iterrows():
                                match_score = int(90 + (pref_family * 10))
                                recs.append({
                                    "name": row['facility_name'],
                                    "type": row['type'],
                                    "match": match_score,
                                    "img": "https://img.icons8.com/color/96/amusement-park.png"
                                })
                        else:
                            # General recommendations
                            for _, row in facilities_df.head(3).iterrows():
                                match_score = int(75 + np.random.randint(0, 20))
                                recs.append({
                                    "name": row['facility_name'],
                                    "type": row['type'],
                                    "match": match_score,
                                    "img": "https://img.icons8.com/color/96/theme-park.png"
                                })
                        
                        # If no matches, show top 3 facilities
                        if not recs:
                            for _, row in facilities_df.head(3).iterrows():
                                recs.append({
                                    "name": row['facility_name'],
                                    "type": row['type'],
                                    "match": 80,
                                    "img": "https://img.icons8.com/color/96/theme-park.png"
                                })
                    else:
                        st.warning("No facilities found in database.")
                        recs = []
                else:
                    st.warning("Database connection not available.")
                    recs = []

                # Display Cards
                if recs:
                    c1, c2, c3 = st.columns(3)
                    cols = [c1, c2, c3]
                    
                    for i, rec in enumerate(recs[:3]):  # Limit to 3
                        with cols[i % 3]:
                            st.markdown(f"""
                            <div class="card" style="text-align: center; padding: 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid rgba(0,0,0,0.05); transition: transform 0.3s ease;">
                                <div style="background: linear-gradient(135deg, #F0F2F6 0%, #FFFFFF 100%); width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                                    <img src="{rec['img']}" width="45" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));">
                                </div>
                                <h4 style="color: #142C63; font-weight: 800; margin-bottom: 5px; font-size: 1.1rem;">{rec['name']}</h4>
                                <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 15px; font-weight: 500;">{rec['type']}</p>
                                <div style="background: linear-gradient(90deg, #F0F2F6 0%, #E2E8F0 100%); border-radius: 12px; padding: 8px; margin-top: 10px; position: relative; overflow: hidden;">
                                    <div style="position: absolute; left: 0; top: 0; height: 100%; width: {rec['match']}%; background: linear-gradient(90deg, #A6D86B 0%, #8BC34A 100%); opacity: 0.3;"></div>
                                    <span style="color: #142C63; font-weight: 700; font-size: 0.9rem; position: relative; z-index: 1;">{rec['match']}% Match</span>
                                </div>
                            </div>""", unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"Analysis Error: {e}")
        else:
            st.warning("⚠️ ML Model not loaded. Please train the model first.")
    else:
        st.info("👈 Fill out your profile on the left to get personalized recommendations.")
        
        # Show real popular rides from database
        render_page_header(
            title="Popular Today",
            subtitle="Most Popular & Efficient Rides Right Now",
            lottie_url="https://lottie.host/2fbfa576-4674-447a-a642-33bdb7802528/fHbZanSbJe.lottie"
        )
        
        if supabase:
            # Get facilities with lowest wait times (most popular/efficient)
            wait_response = supabase.table("waiting_times").select("entity_description_short, wait_time_max").order("work_date", desc=True).limit(100).execute()
            wait_df = pd.DataFrame(wait_response.data)
            
            if not wait_df.empty:
                # Calculate average wait time per facility
                popular = wait_df.groupby('entity_description_short')['wait_time_max'].mean().sort_values().head(3)
                
                cards_html = '<div style="display: flex; gap: 20px; overflow-x: auto; padding-bottom: 20px;">'
                for facility, wait_time in popular.items():
                    cards_html += f"""
                    <div class="card" style="min-width: 220px; padding: 20px; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 5px solid #F57C00; background: white; margin-right: 15px;">
                        <h4 style="color: #142C63; font-size: 1rem; font-weight: 700; margin-bottom: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{facility}</h4>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="background: #FFF3E0; color: #F57C00; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">Wait: {int(wait_time)} min</span>
                        </div>
                    </div>"""
                cards_html += '</div>'
                st.markdown(cards_html, unsafe_allow_html=True)
            else:
                st.info("No wait time data available.")
        else:
            st.info("Database connection not available.")