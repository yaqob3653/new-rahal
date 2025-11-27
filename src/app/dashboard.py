import streamlit as st
import plotly.express as px
import streamlit.components.v1 as components
import requests
import pandas as pd
from src.app.data_service import get_dashboard_metrics, get_chart_data
from src.app.login_page import logout

def show_dashboard():
    """
    Renders the main dashboard content (Metrics, Charts, Sidebar).
    """
    # Reset Sidebar to visible and remove login background
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: block; }
        .stApp { background-image: none; background-color: #F0F2F6; }
    </style>
    """, unsafe_allow_html=True)
    
    # Use st.logo for the sidebar top placement
    st.logo("https://ideogram.ai/assets/image/lossless/response/2N9JG3TjTGWI9PV2FmBThg", icon_image="https://ideogram.ai/assets/image/lossless/response/SIaHZQRVTVu5xEbSAO3jRA")

    # Sidebar Styling & Content
    with st.sidebar:
        # Custom CSS for Sidebar
        st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                background-color: #0f172a;
                border-right: 1px solid #1e293b;
            }
            [data-testid="stSidebar"] * {
                color: #e2e8f0;
            }
            .profile-card {
                background-color: #1e293b;
                padding: 15px;
                border-radius: 12px;
                border: 1px solid #334155;
                margin-bottom: 20px;
            }
            .profile-role {
                color: #3b82f6 !important;
                font-size: 0.8rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            .profile-email {
                font-size: 0.9rem;
                color: #94a3b8 !important;
                word-break: break-all;
            }
            /* Style the Logout Button to be red/warning style */
            div.stButton > button:first-child {
                background-color: rgba(239, 68, 68, 0.1) !important;
                color: #ef4444 !important;
                border: 1px solid #ef4444 !important;
                font-weight: 600;
                transition: all 0.3s;
            }
            div.stButton > button:first-child:hover {
                background-color: #ef4444 !important;
                color: white !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # User Profile Card
        user_email = "N/A"
        if st.session_state.get('user'):
            user = st.session_state['user']
            if hasattr(user, 'email'):
                user_email = user.email
            elif isinstance(user, dict):
                user_email = user.get('email', 'N/A')

        st.markdown(f"""
        <div class="profile-card">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                <div style="background: #3b82f6; width: 8px; height: 8px; border-radius: 50%;"></div>
                <span style="font-weight: 600; color: white;">{st.session_state['role']}</span>
            </div>
            <div class="profile-email">{user_email}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("📌 Navigate using the menu above.")
        
        # Spacer to push logout to bottom (visual spacing)
        st.markdown("<br>" * 4, unsafe_allow_html=True)
        
        if st.button("🚪 Sign Out", use_container_width=True):
            logout()

    # Dashboard Content
    if st.session_state['role'] == "Admin":
        
        # Fetch dashboard metrics
        total_visitors, system_health, avg_wait, capacity_pct, data_date = get_dashboard_metrics()
        
        # Calculate predicted peak
        try:
            import joblib
            import os
            model_path = "src/models/crowd_model.pkl"
            if os.path.exists(model_path):
                m = joblib.load(model_path)
                future = m.make_future_dataframe(periods=1)
                forecast = m.predict(future)
                peak_hour = 17  # Default 5 PM
                peak_time = f"{peak_hour:02d}:00"
                capacity_pct = min(85, int((forecast.iloc[-1]['yhat'] / 20000) * 100))
            else:
                peak_time = "N/A"
                capacity_pct = int(capacity_pct) if capacity_pct else 0
        except:
            peak_time = "N/A"
            capacity_pct = int(capacity_pct) if capacity_pct else 0

        # --- Animated Background (Particles) ---
        st.markdown("""
        <style>
        /* Particles Background Container */
        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1; /* Behind everything */
            background-color: #f8fafc; /* Light background matching app */
        }
        </style>
        
        <div id="particles-js"></div>
        
        <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
        <script>
            particlesJS("particles-js", {
                "particles": {
                    "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
                    "color": { "value": "#3b82f6" }, /* Blue particles */
                    "shape": { "type": "circle" },
                    "opacity": { "value": 0.5, "random": false },
                    "size": { "value": 3, "random": true },
                    "line_linked": {
                    }
                },
                "retina_detect": true
            });
        </script>
        """, unsafe_allow_html=True)

        # Header with Animation (AT THE TOP)
        col_head1, col_head2 = st.columns([1, 4])
        with col_head1:
             # New optimized dotLottie animation
             lottie_html = """
                <script src="https://unpkg.com/@lottiefiles/dotlottie-wc@0.8.5/dist/dotlottie-wc.js" type="module"></script>
                <dotlottie-wc 
                    src="https://lottie.host/b857e09f-37cc-4774-920b-71adf0a2f6da/xeJUh29Z4p.lottie" 
                    style="width: 220px; height: 220px;" 
                    autoplay 
                    loop>
                </dotlottie-wc>
             """
             components.html(lottie_html, height=230)
             
        with col_head2:
            st.markdown("""
            <h1 style="margin: 0; padding-top: 30px;">📡 Live Operations Center</h1>
            <p style="color: #64748b; margin: 0;">Real-time Park Monitoring & AI Analytics</p>
            """, unsafe_allow_html=True)
        
        st.markdown("---")

        # Metrics Row with colorful border-left design
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card delay-1" style="border-left: 4px solid #F57C00;">
                <div class="metric-label">Total Visitors</div>
                <div id="counter-visitors" class="metric-value">{total_visitors:,}</div>
                <div class="metric-sub" style="color: #64748b;">
                    📅 Data from: {data_date}
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" data-width="75" style="background: #F57C00;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            health_color = "#10b981" if system_health > 90 else "#f59e0b" if system_health > 70 else "#ef4444"
            st.markdown(f"""
            <div class="metric-card delay-2" style="border-left: 4px solid {health_color};">
                <div class="metric-label">System Health</div>
                <div id="counter-health" class="metric-value">{system_health:.1f}%</div>
                <div class="metric-sub" style="color: {health_color};">
                    Operational Facilities
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" data-width="{system_health}" style="background: {health_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-card delay-3" style="border-left: 4px solid #3b82f6;">
                <div class="metric-label">Avg Wait Time</div>
                <div id="counter-wait" class="metric-value">{avg_wait} min</div>
                <div class="metric-sub" style="color: #3b82f6;">
                    ⏱️ Park-wide Average
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" data-width="{min(100, avg_wait * 2)}" style="background: #3b82f6;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="metric-card delay-4" style="border-left: 4px solid #6366f1;">
                <div class="metric-label">Predicted Peak</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #0f172a; margin: 10px 0;">{peak_time}</div>
                <div class="metric-sub" style="color: #6366f1;">
                    📊 ~{capacity_pct}% Capacity
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" data-width="{capacity_pct}" style="background: #6366f1;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)


        # Custom CSS & JS for Advanced Animations
        st.markdown("""
        <style>
        /* Card Entrance Animation */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .metric-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s ease;
            opacity: 0; /* Hidden initially */
            animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 30px rgba(0,0,0,0.1);
            border-color: rgba(59, 130, 246, 0.3);
        }
        
        /* Staggered Delays */
        .delay-1 { animation-delay: 0.1s; }
        .delay-2 { animation-delay: 0.3s; }
        .delay-3 { animation-delay: 0.5s; }
        .delay-4 { animation-delay: 0.7s; }
        
        /* Progress Bar */
        .progress-bg {
            background: #f1f5f9;
            height: 6px;
            border-radius: 3px;
            margin-top: 15px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            width: 0; /* Start at 0 */
            border-radius: 3px;
            transition: width 2s cubic-bezier(0.2, 0.8, 0.2, 1);
        }
        
        /* Typography */
        .metric-value {
            font-size: 2.2rem;
            font-weight: 800;
            color: #0f172a;
            margin: 10px 0;
            font-variant-numeric: tabular-nums;
            letter-spacing: -1px;
        }
        
        .metric-label {
            color: #64748b;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-sub {
            font-size: 0.8rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        /* Floating Icon in Header */
        .floating-icon {
            animation: float 3s ease-in-out infinite;
        }
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        
        /* Pulse Effect */
        .pulse-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 0 rgba(16, 185, 129, 0.4);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
            100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }
        </style>
        
        <script>
        function animateValue(id, start, end, duration, isFloat) {
            const obj = document.getElementById(id);
            if (!obj) return;
            
            let startTimestamp = null;
            const step = (timestamp) => {
                if (!startTimestamp) startTimestamp = timestamp;
                const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                const easeProgress = 1 - Math.pow(1 - progress, 3); // Cubic ease out
                let currentVal = easeProgress * (end - start) + start;
                
                if (isFloat) {
                    obj.innerHTML = currentVal.toFixed(1) + "%";
                } else {
                    obj.innerHTML = Math.floor(currentVal).toLocaleString();
                }
                
                if (progress < 1) {
                    window.requestAnimationFrame(step);
                } else {
                    if (isFloat) obj.innerHTML = end.toFixed(1) + "%";
                    else obj.innerHTML = end.toLocaleString();
                }
            };
            window.requestAnimationFrame(step);
        }

        // Trigger animations
        setTimeout(() => {
            // Animate Numbers
            animateValue("counter-visitors", 0, {total_visitors}, 2000, false);
            animateValue("counter-health", 0, {system_health}, 2000, true);
            animateValue("counter-wait", 0, {avg_wait}, 2000, false);
            animateValue("counter-peak", 0, {capacity_pct}, 2000, true); 
            
            // Animate Progress Bars
            const bars = document.querySelectorAll('.progress-fill');
            bars.forEach(bar => {
                bar.style.width = bar.getAttribute('data-width') + "%";
            });
        }, 500);
        </script>
        """, unsafe_allow_html=True)
        
        # Refresh Button
        col_ref1, col_ref2 = st.columns([6, 1])
        with col_ref2:
            if st.button("🔄 Refresh", help="Reload data and replay animations"):
                st.rerun()

        # --- Advanced Analytics Section ---
        st.markdown("### 📊 Real-time Operational Analytics")
        
        chart_data = get_chart_data()
        
        if chart_data is not None and not chart_data.empty:
            
            # Prepare Data
            chart_data['work_date'] = pd.to_datetime(chart_data['work_date'])
            latest_data = chart_data.sort_values('work_date', ascending=False).drop_duplicates('entity_description_short')
            
            # --- Chart 1: Facility Status Treemap ---
            # This gives a bird's-eye view of all rides, sized by wait time
            fig_treemap = px.treemap(
                latest_data,
                path=[px.Constant("Park Zones"), 'entity_description_short'],
                values='wait_time_max',
                color='wait_time_max',
                color_continuous_scale='RdYlGn_r', # Red for high wait, Green for low
                title='<b>🎡 Facility Load Heatmap</b>'
            )
            
            fig_treemap.update_layout(
                margin=dict(t=50, l=25, r=25, b=25),
                height=400,
                font=dict(family="Inter, sans-serif"),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
            )
            
            # --- Chart 2: Activity Trend (Area Chart) ---
            # Group by hour to show trend
            chart_data['hour'] = chart_data['work_date'].dt.hour
            hourly_trend = chart_data.groupby('hour')['wait_time_max'].mean().reset_index()
            
            fig_trend = px.area(
                hourly_trend,
                x='hour',
                y='wait_time_max',
                title='<b>📈 Park Activity Trend (Hourly)</b>',
                labels={'hour': 'Hour of Day', 'wait_time_max': 'Avg Wait (min)'},
                color_discrete_sequence=['#3b82f6']
            )
            
            fig_trend.update_layout(
                margin=dict(t=50, l=25, r=25, b=25),
                height=400,
                font=dict(family="Inter, sans-serif"),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
            )
            
            # Layout Charts
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div style="background: white; padding: 15px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
                st.plotly_chart(fig_treemap, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with c2:
                st.markdown('<div style="background: white; padding: 15px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
                st.plotly_chart(fig_trend, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
        else:
            st.info("Waiting for real-time data stream...")

        # Navigation Hints
        st.info("💡 **Pro Tip:** Use the sidebar menu to access detailed reports for Crowd Prediction, Sentiment Analysis, and Facility Operations.")

    else:
        st.title("Welcome to Rahhal Analytics")
        st.markdown("### Smart Park Experience Optimization System")

        st.info(
            "**Revolutionizing Theme Park Experiences**\n\n"
            "Leveraging advanced Machine Learning and Real-time Data Analytics to provide personalized recommendations, "
            "predict crowd levels, and optimize park operations."
        )
        
        c1, c2 = st.columns(2)
        with c1:
            st.image("https://images.unsplash.com/photo-1505761671935-60b3a7427bad?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", use_container_width=True, caption="Explore Magic")
        with c2:
            st.markdown("#### Today's Forecast")
            st.info("Sunny, 25°C. Perfect for water rides!")
            st.markdown("#### Tip of the Day")
            st.success("Visit 'Harry Potter' area before 11 AM to avoid long lines.")
            
        st.markdown("### Quick Access Modules")
        q1, q2, q3 = st.columns(3)

        with q1:
            st.info("**Smart Recommendations**\n\nGet personalized ride suggestions based on your profile.")

        with q2:
            st.info("**Crowd Prediction**\n\nForecast park attendance and ride wait times.")

        with q3:
            st.info("**Route Optimizer**\n\nFind the fastest path through the park.")
