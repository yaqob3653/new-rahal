import streamlit as st
import time

if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("Please login first.")
    time.sleep(1)
    st.switch_page("main.py")
    st.stop()


# Page Config
st.set_page_config(page_title="Documentation | Rahhal", page_icon="📚", layout="wide")

# Custom CSS
def local_css(file_name):
    with open(file_name, encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("src/app/style.css")

st.title("📚 Project Documentation")
st.markdown("### Rahhal Analytics System Architecture & Guide")

# --- System Architecture ---
st.header("🏗️ System Architecture")
st.markdown("""
The system follows a modern **Data Engineering & Data Science Pipeline**:
""")

# Mermaid Diagram
st.markdown("""
```mermaid
graph LR
    A[Raw Data Sources] -->|ETL Pipeline| B(Supabase Database)
    B -->|Query| C{AI Models}
    C -->|Training| D[Saved Models .pkl]
    B -->|Live Data| E[Streamlit App]
    D -->|Inference| E
    E -->|Visuals| F[End User / Admin]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#bfb,stroke:#333,stroke-width:2px
    style E fill:#f57c00,stroke:#333,stroke-width:4px,color:white
```
""")

st.markdown("""
<div class="card">
    <h4>1. Data Layer (Supabase)</h4>
    <p>We use <strong>PostgreSQL</strong> hosted on Supabase as our central data warehouse. It stores:</p>
    <ul>
        <li><strong>Attendance:</strong> Historical park visits.</li>
        <li><strong>Waiting Times:</strong> Real-time ride queue data.</li>
        <li><strong>Visitors:</strong> Demographic and preference profiles.</li>
        <li><strong>Reviews:</strong> Text feedback for NLP analysis.</li>
    </ul>
</div>

<div class="card" style="margin-top: 20px;">
    <h4>2. AI & Machine Learning Layer</h4>
    <p>Three specialized models power the intelligence:</p>
    <ul>
        <li><strong>Crowd Prediction (Prophet):</strong> Time-series forecasting for attendance.</li>
        <li><strong>Recommendation Engine (K-Means):</strong> Unsupervised clustering for visitor segmentation.</li>
        <li><strong>Sentiment Analysis (VADER):</strong> NLP lexicon-based scoring for feedback.</li>
    </ul>
</div>

<div class="card" style="margin-top: 20px;">
    <h4>3. Application Layer (Streamlit)</h4>
    <p>A responsive web application that serves as the interface for both Visitors (Recommendations) and Management (Analytics).</p>
</div>
""", unsafe_allow_html=True)

# --- Tech Stack ---
st.header("🛠️ Technology Stack")
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.image("https://img.icons8.com/color/96/python--v1.png", width=60)
    st.caption("Python 3.9+")
with c2:
    st.image("https://img.icons8.com/color/96/streamlit.png", width=60)
    st.caption("Streamlit")
with c3:
    st.image("https://img.icons8.com/color/96/postgreesql.png", width=60)
    st.caption("Supabase (SQL)")
with c4:
    st.image("https://img.icons8.com/color/96/pandas.png", width=60)
    st.caption("Pandas & Plotly")
with c5:
    st.image("https://img.icons8.com/nolan/96/brain.png", width=60)
    st.caption("Scikit-Learn")

# --- Features Guide ---
st.header("🚀 Features Guide")
st.markdown("""
| Module | Description | Target Audience |
| :--- | :--- | :--- |
| **🏠 Home** | High-level KPI dashboard. | Management |
| **🎯 Recommendations** | Personalized ride suggestions based on age, weight, and thrill preference. | Visitors |
| **📊 Crowd Prediction** | 7-day attendance forecast and hourly heatmaps. | Operations |
| **😊 Sentiment** | Analysis of guest reviews and feedback trends. | Marketing |
| **🎡 Facility Analysis** | Real-time status and efficiency metrics for rides. | Operations |
| **🔍 EDA** | Deep dive into raw data distributions. | Data Analysts |
| **🗺️ Route Optimizer** | Smart pathfinding to minimize walking and waiting. | Visitors |
""")

# --- Team ---
st.markdown("## 👥 Development Team")
st.info("Graduation Project - Computer Engineering Department")
