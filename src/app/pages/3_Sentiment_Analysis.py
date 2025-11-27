import streamlit as st
import time

if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("Please login first.")
    time.sleep(1)
    st.switch_page("main.py")
    st.stop()

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def init_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# Page Config
st.set_page_config(page_title="Sentiment Analysis | Rahhal", page_icon="😊", layout="wide")

# Custom CSS
def local_css(file_name):
    with open(file_name, encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("src/app/style.css")

st.markdown("# 😊 Sentiment Analysis & Feedback")
st.markdown("### Understanding Visitor Emotions via NLP")

# --- Real Data Loading ---
@st.cache_data(ttl=60)
def load_reviews():
    if not supabase:
        return pd.DataFrame()
    
    # Fetch reviews from Supabase
    # Note: Schema has 'year_month' (VARCHAR), not 'review_date'
    response = supabase.table("reviews").select("*").order("year_month", desc=True).limit(500).execute()
    df = pd.DataFrame(response.data)
    
    if df.empty:
        return pd.DataFrame()

    # Rename columns to match UI logic if needed, or adjust UI logic
    # DB columns: review_id, rating, year_month, reviewer_location, review_text, branch, sentiment_score
    
    # Ensure date format (year_month is like "2019-4" or "2019.4" depending on data, usually "YYYY-MM")
    # We'll try to parse it flexibly
    df['Date'] = pd.to_datetime(df['year_month'], errors='coerce')
    
    # If parsing failed (NaT), fill with today or some default
    df['Date'] = df['Date'].fillna(pd.Timestamp.now())
    
    df['Review'] = df['review_text']
    
    # Handle None/NaN values in sentiment_score
    df['Score'] = df['sentiment_score'].fillna(0.0)
    
    # Create Sentiment label from Score if not present in DB
    if 'sentiment_label' not in df.columns:
        def get_label(score):
            if score >= 0.05: return 'Positive'
            elif score <= -0.05: return 'Negative'
            else: return 'Neutral'
        df['Sentiment'] = df['Score'].apply(get_label)
    else:
        df['Sentiment'] = df['sentiment_label']
    
    return df

reviews_data = load_reviews()

if reviews_data.empty:
    st.warning("No reviews found in the database.")
    st.stop()

# Calculate Metrics
avg_sentiment = reviews_data['Score'].mean()
positive_pct = (reviews_data['Sentiment'] == 'Positive').mean() * 100
negative_pct = (reviews_data['Sentiment'] == 'Negative').mean() * 100

# --- Dashboard Layout ---

# 1. Top KPI Cards
k1, k2, k3 = st.columns(3)

with k1:
    st.markdown(f"""<div class="card" style="border-left-color: #A6D86B; text-align: center;">
        <h4>Overall Sentiment Score</h4>
        <h1 style="color: #A6D86B; font-size: 3rem; margin: 0;">{avg_sentiment:.2f}</h1>
        <p>Scale: -1.0 to +1.0</p>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""<div class="card" style="border-left-color: #142C63; text-align: center;">
        <h4>Positive Reviews</h4>
        <h1 style="color: #142C63; font-size: 3rem; margin: 0;">{positive_pct:.0f}%</h1>
        <p>Visitors are happy!</p>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""<div class="card" style="border-left-color: #D92B7D; text-align: center;">
        <h4>Negative Feedback</h4>
        <h1 style="color: #D92B7D; font-size: 3rem; margin: 0;">{negative_pct:.0f}%</h1>
        <p>Areas for improvement</p>
    </div>""", unsafe_allow_html=True)

# 2. Charts Row
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### 📈 Sentiment Trend Over Time")
    # Generate some trend data
    trend_dates = pd.date_range(start='2023-01-01', periods=30)
    trend_scores = [0.5 + 0.3 * np.sin(i/5) + np.random.normal(0, 0.1) for i in range(30)]
    df_trend = pd.DataFrame({'Date': trend_dates, 'Sentiment Score': trend_scores})
    
    fig_trend = px.area(df_trend, x='Date', y='Sentiment Score', 
                        line_shape='spline', color_discrete_sequence=['#F57C00'])
    fig_trend.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit", size=12, color="#142C63"),
        yaxis=dict(range=[-1, 1], gridcolor='#E0E0E0'),
        xaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with c2:
    st.markdown("### 🍩 Sentiment Distribution")
    fig_pie = px.pie(reviews_data, names='Sentiment', 
                       color='Sentiment',
                       color_discrete_map={'Positive': '#A6D86B', 'Neutral': '#FFD54F', 'Negative': '#D92B7D'},
                       hole=0.6)
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit", size=12, color="#142C63"),
        showlegend=False
    )
    # Add text in center
    fig_pie.add_annotation(text="Voice", x=0.5, y=0.55, font_size=20, showarrow=False)
    fig_pie.add_annotation(text="of Guest", x=0.5, y=0.45, font_size=14, showarrow=False)
    
    st.plotly_chart(fig_pie, use_container_width=True)

# 3. Word Cloud & Recent Reviews
r1, r2 = st.columns([1, 1])

with r1:
    st.markdown("### ☁️ Common Keywords")
    # CSS Tag Cloud
    tags = [
        ("Queue", 5), ("FastPass", 4), ("Food", 4), ("Staff", 3), 
        ("Clean", 3), ("Expensive", 2), ("Fun", 5), ("Family", 4),
        ("Parking", 2), ("Show", 3), ("Hot", 2), ("Wait", 5)
    ]
    
    tag_html = '<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; padding: 20px;">'
    for word, weight in tags:
        size = 1 + (weight * 0.2)
        color = "#142C63" if weight > 3 else "#F57C00"
        if weight < 3: color = "#D92B7D"
        tag_html += f'<span style="font-size: {size}rem; color: {color}; background: #F0F2F6; padding: 5px 15px; border-radius: 20px; font-weight: bold;">{word}</span>'
    tag_html += '</div>'
    
    st.markdown(f'<div class="card">{tag_html}</div>', unsafe_allow_html=True)

with r2:
    st.markdown("### 💬 Recent Feedback")
    for i, row in reviews_data.head(3).iterrows():
        sentiment_color = "#A6D86B" if row['Sentiment'] == 'Positive' else "#D92B7D"
        if row['Sentiment'] == 'Neutral': sentiment_color = "#FFD54F"
        
        st.markdown(f"""<div class="card" style="padding: 15px; margin-bottom: 10px; border-left: 5px solid {sentiment_color};">
            <p style="font-style: italic;">"{row['Review']}"</p>
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #666;">
                <span>{row['Date'].strftime('%Y-%m-%d')}</span>
                <span style="font-weight: bold; color: {sentiment_color};">{row['Sentiment']}</span>
            </div>
        </div>""", unsafe_allow_html=True)
