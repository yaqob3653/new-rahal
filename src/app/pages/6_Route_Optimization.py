import streamlit as st
import time

if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("Please login first.")
    time.sleep(1)
    st.switch_page("main.py")
    st.stop()

import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import os
from supabase import create_client
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
st.set_page_config(page_title="Smart Route Optimizer | Rahhal", page_icon="🗺️", layout="wide")

# Custom CSS
def local_css(file_name):
    with open(file_name, encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("src/app/style.css")

st.markdown("# 🗺️ AI Route Optimizer")
st.markdown("### Find the Fastest Path Through the Park")

# --- Graph Logic ---
# We'll build a graph where nodes are attractions and edges are paths with weights (walking time + wait time)

# 1. Define Nodes (Attractions) - Mock positions for visualization
nodes = {
    "Entrance": (0, 0),
    "Hollywood Rip Ride Rockit": (2, 5),
    "Revenge of the Mummy": (5, 8),
    "Transformers": (6, 4),
    "Harry Potter Diagon Alley": (8, 9),
    "Simpsons Ride": (9, 3),
    "Men in Black": (7, 1),
    "E.T. Adventure": (4, 2)
}

# 2. Define Edges (Paths) - (Node1, Node2, Walking Time in min)
edges = [
    ("Entrance", "Hollywood Rip Ride Rockit", 5),
    ("Entrance", "E.T. Adventure", 7),
    ("Hollywood Rip Ride Rockit", "Revenge of the Mummy", 6),
    ("Hollywood Rip Ride Rockit", "Transformers", 5),
    ("Revenge of the Mummy", "Harry Potter Diagon Alley", 4),
    ("Transformers", "Simpsons Ride", 8),
    ("Simpsons Ride", "Men in Black", 3),
    ("Men in Black", "E.T. Adventure", 5),
    ("Transformers", "Revenge of the Mummy", 4),
    ("Harry Potter Diagon Alley", "Simpsons Ride", 6)
]

# 3. Get Real Wait Times
@st.cache_data(ttl=60)
def get_wait_times():
    if not supabase:
        return {node: 0 for node in nodes}
    
    # Fetch latest wait times
    response = supabase.table("waiting_times").select("entity_description_short, wait_time_max").limit(500).order("work_date", desc=True).execute()
    df = pd.DataFrame(response.data)
    
    if df.empty:
        return {node: 15 for node in nodes} # Default fallback
        
    # Map DB names to Node names (Simplified mapping for demo)
    # In production, use exact matching or a mapping table
    wait_times = {}
    for node in nodes:
        # Fuzzy match or direct match
        match = df[df['entity_description_short'].str.contains(node.split()[0], case=False, na=False)]
        if not match.empty:
            wait_times[node] = int(match['wait_time_max'].mean())
        else:
            wait_times[node] = 10 # Default if not found
            
    return wait_times

current_wait_times = get_wait_times()

# 4. Build Graph
G = nx.Graph()
for node, pos in nodes.items():
    G.add_node(node, pos=pos, wait=current_wait_times.get(node, 0))

for u, v, walk_time in edges:
    # Weight = Walking Time + Wait Time at destination
    weight = walk_time + current_wait_times.get(v, 0)
    G.add_edge(u, v, weight=weight, walk=walk_time)

# --- UI Layout ---
col_ctrl, col_map = st.columns([1, 3])

with col_ctrl:
    st.markdown("""<div class="card">
        <h4>📍 Plan Your Route</h4>""", unsafe_allow_html=True)
    
    start_point = st.selectbox("Start Point", list(nodes.keys()), index=0)
    end_point = st.selectbox("Destination", list(nodes.keys()), index=4)
    
    optimize_for = st.radio("Optimize For:", ["Fastest Time", "Least Walking", "Most Attractions"])
    
    if st.button("Calculate Route 🚀"):
        try:
            path = nx.shortest_path(G, source=start_point, target=end_point, weight='weight')
            total_time = nx.shortest_path_length(G, source=start_point, target=end_point, weight='weight')
            
            st.success(f"Route Found!")
            st.metric("Est. Total Time", f"{total_time} min")
            
            st.markdown("### 📝 Step-by-Step")
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                walk = G[u][v]['walk']
                wait = G.nodes[v]['wait']
                st.markdown(f"""<div style="background: #F0F2F6; padding: 10px; border-radius: 8px; margin-bottom: 5px; font-size: 0.9rem;">
                    <strong>{i+1}. Walk to {v}</strong><br>
                    <span style="color: #666;">🚶 {walk} min | ⏳ Wait: {wait} min</span>
                </div>""", unsafe_allow_html=True)
                
        except nx.NetworkXNoPath:
            st.error("No path found.")
            path = []
    else:
        path = []
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_map:
    st.markdown("### 🗺️ Park Navigation Map")
    
    # Plot Graph using Plotly
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)
        wait = G.nodes[node]['wait']
        node_text.append(f"{node}<br>Wait: {wait} min")
        
        # Color based on wait time
        if wait < 15: node_color.append("#A6D86B") # Green
        elif wait < 45: node_color.append("#F57C00") # Orange
        else: node_color.append("#D92B7D") # Red
        
        # Size based on selection
        if node in path:
            node_size.append(30)
        else:
            node_size.append(20)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[n if n in path else "" for n in G.nodes()], # Only show label for path
        textposition="top center",
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
            line_width=2))
            
    # Highlight Path
    path_x, path_y = [], []
    if path:
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            x0, y0 = G.nodes[u]['pos']
            x1, y1 = G.nodes[v]['pos']
            path_x.extend([x0, x1, None])
            path_y.extend([y0, y1, None])
            
    path_trace = go.Scatter(
        x=path_x, y=path_y,
        line=dict(width=4, color='#142C63', dash='dot'),
        mode='lines',
        name='Optimal Route'
    )

    fig = go.Figure(data=[edge_trace, path_trace, node_trace],
                 layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0,l=0,r=0,t=0),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                    ))
                    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""<div style="display: flex; gap: 20px; justify-content: center; margin-top: 10px;">
        <div><span style="color: #A6D86B;">●</span> Low Wait (<15m)</div>
        <div><span style="color: #F57C00;">●</span> Medium Wait (15-45m)</div>
        <div><span style="color: #D92B7D;">●</span> High Wait (>45m)</div>
    </div>""", unsafe_allow_html=True)
