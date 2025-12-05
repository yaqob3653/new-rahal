import plotly.express as px
import plotly.graph_objects as go
import plotly
import json
import pandas as pd
import numpy as np

def to_html(fig):
    return fig.to_html(full_html=False, include_plotlyjs='cdn', config={'responsive': True, 'displayModeBar': False})

def to_json(fig):
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def generate_treemap(chart_df):
    if chart_df is None or chart_df.empty:
        return "{}"
    
    chart_df['work_date'] = pd.to_datetime(chart_df['work_date'])
    latest_data = chart_df.sort_values('work_date', ascending=False).drop_duplicates('entity_description_short')
    
    fig = px.treemap(
        latest_data,
        path=[px.Constant("Park Zones"), 'entity_description_short'],
        values='wait_time_max',
        color='wait_time_max',
        color_continuous_scale='Viridis',
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), paper_bgcolor='rgba(0,0,0,0)')
    return to_json(fig)

def generate_trend_area(chart_df, x_col, y_col, title=None, color='#3b82f6'):
    if chart_df is None or chart_df.empty:
        return "{}"
    
    fig = px.area(
        chart_df,
        x=x_col,
        y=y_col,
        title=title,
        color_discrete_sequence=[color]
    )
    fig.update_layout(
        margin=dict(t=30 if title else 10, l=0, r=0, b=0), 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
        font=dict(family="Outfit", color="#142C63")
    )
    if title:
        fig.update_traces(line_color=color)
        return to_html(fig) # Use HTML for Insights/Feedback
    else:
        return to_json(fig) # Use JSON for Dashboard

def generate_line_chart(df, x_col, y_col, title, x_label, y_label):
    if df is None or df.empty:
        return "{}"
    
    fig = px.line(df, x=x_col, y=y_col, title=title, labels={x_col: x_label, y_col: y_label})
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Outfit", color="#142C63"))
    fig.update_traces(line_color='#F57C00', line_width=3)
    return to_json(fig)

def generate_bar_chart(df, x_col, y_col, title, x_label, y_label, color_col=None):
    if df is None or df.empty:
        return "" # Return empty string for HTML
    
    fig = px.bar(df, x=x_col, y=y_col, title=title, labels={x_col: x_label, y_col: y_label},
                 color=color_col if color_col else y_col, 
                 color_continuous_scale='Viridis' if color_col else None)
    
    if not color_col:
         fig.update_traces(marker_color='#3b82f6')

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(family="Outfit", color="#142C63"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    )
    return to_html(fig) # Default to HTML for most pages now

def generate_pie_chart(df, names, values=None, title=None, color=None, hole=0.5):
    if df is None or df.empty:
        return ""
    
    if values:
        fig = px.pie(values=values, names=names, title=title, color=color, hole=hole, color_discrete_map={'Open': '#A6D86B', 'Closed': '#EF4444'})
    else:
        fig = px.pie(df, names=names, title=title, color=color, hole=hole, color_discrete_map={'Positive': '#A6D86B', 'Neutral': '#FFD54F', 'Negative': '#D92B7D'})
        
    fig.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit", color="#142C63"),
        margin=dict(l=20, r=20, t=60 if title else 20, b=20),
        showlegend=False if not title else True
    )
    return to_html(fig)

def generate_scatter_chart(df, x_col, y_col, color_col, size_col=None, title=None):
    if df is None or df.empty:
        return ""
        
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, size=size_col, title=title, color_continuous_scale='Viridis')
    fig.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(family="Outfit", color="#142C63"),
        margin=dict(l=50, r=20, t=60, b=50)
    )
    return to_html(fig)

def generate_heatmap(df, x_col, y_col, z_col, title):
    if df is None or df.empty:
        return ""
        
    fig = px.density_heatmap(df, x=x_col, y=y_col, z=z_col, title=title, color_continuous_scale='Viridis')
    fig.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(family="Outfit", color="#142C63"),
        margin=dict(l=50, r=20, t=60, b=50)
    )
    return to_html(fig)

def generate_histogram(df, x_col, title, color_seq=['#142C63'], nbins=30):
    if df is None or df.empty:
        return ""
        
    fig = px.histogram(df, x=x_col, nbins=nbins, title=title, color_discrete_sequence=color_seq)
    fig.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(family="Outfit", color="#142C63"),
        margin=dict(l=50, r=20, t=60, b=50)
    )
    return to_html(fig)

def generate_box_plot(df, y_col, title, color_seq=['#142C63']):
    if df is None or df.empty:
        return ""
        
    fig = px.box(df, y=y_col, title=title, color_discrete_sequence=color_seq)
    fig.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(family="Outfit", color="#142C63"),
        margin=dict(l=50, r=20, t=60, b=50)
    )
    return to_html(fig)

def generate_custom_trend(daily, x_col, y_col, title):
    if daily is None or daily.empty:
        return ""
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily[x_col], y=daily[y_col],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#F97316', width=3),
        fillcolor='rgba(249, 115, 22, 0.2)',
        name='Attendance'
    ))
    fig.update_layout(
        title=title,
        height=350,
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(family="Outfit", color="#142C63"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
        margin=dict(l=50, r=20, t=60, b=50)
    )
    return to_html(fig)

def generate_health_charts(df_cv, df_vis, df_rev):
    cv_html = res_html = clus_html = ""
    
    # 1. Crowd
    if not df_cv.empty:
        fig_cv = go.Figure()
        fig_cv.add_trace(go.Scatter(x=df_cv['ds'], y=df_cv['y'], mode='markers', name='Actual Data', marker=dict(color='#A6D86B', size=8, opacity=0.8)))
        fig_cv.add_trace(go.Scatter(x=df_cv['ds'], y=df_cv['yhat'], mode='lines', name='Model Prediction', line=dict(color='#142C63', width=3)))
        fig_cv.update_layout(
            title="Model Performance: Actual vs Predicted",
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(family="Outfit", color="#142C63"),
            xaxis=dict(title="Date", showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            yaxis=dict(title="Attendance", showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=20, t=60, b=40)
        )
        cv_html = to_html(fig_cv)
        
        df_cv['residual'] = df_cv['y'] - df_cv['yhat']
        fig_res = px.histogram(df_cv, x='residual', nbins=20, title="Error Distribution (Residuals)", color_discrete_sequence=['#F57C00'])
        fig_res.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Outfit", color="#142C63"))
        res_html = to_html(fig_res)

    # 2. Rec
    if not df_vis.empty:
        fig_clus = px.scatter(df_vis, x='age', y='weight_kg', color='accompanied_with',
                              title="Visitor Demographics & Group Type",
                              color_continuous_scale='Viridis')
        fig_clus.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Outfit", color="#142C63"))
        clus_html = to_html(fig_clus)

    return cv_html, res_html, clus_html

def generate_map_json(nodes, edges, wait_times, path):
    import networkx as nx
    
    G = nx.Graph()
    for node, pos in nodes.items():
        G.add_node(node, pos=pos, wait=wait_times.get(node, 0))
    
    for u, v, walk_time in edges:
        weight = walk_time + wait_times.get(v, 0)
        G.add_edge(u, v, weight=weight, walk=walk_time)
        
    # Generate Plotly Map
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = {
        'x': edge_x, 'y': edge_y,
        'line': {'width': 1, 'color': '#888'},
        'hoverinfo': 'none',
        'mode': 'lines',
        'type': 'scatter'
    }
    
    # Highlight Path
    path_x, path_y = [], []
    if path:
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            x0, y0 = G.nodes[u]['pos']
            x1, y1 = G.nodes[v]['pos']
            path_x.extend([x0, x1, None])
            path_y.extend([y0, y1, None])
    
    path_trace = {
        'x': path_x, 'y': path_y,
        'line': {'width': 4, 'color': '#142C63', 'dash': 'dot'},
        'mode': 'lines',
        'name': 'Optimal Route',
        'type': 'scatter'
    }
    
    # Nodes
    node_x, node_y, node_text, node_color, node_size = [], [], [], [], []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        wait = G.nodes[node]['wait']
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node}<br>Wait: {wait} min")
        
        if wait < 15:
            node_color.append("#A6D86B")
        elif wait < 45:
            node_color.append("#F57C00")
        else:
            node_color.append("#D92B7D")
        
        node_size.append(30 if node in path else 20)
    
    node_trace = {
        'x': node_x, 'y': node_y,
        'mode': 'markers+text',
        'hoverinfo': 'text',
        'text': [n if n in path else "" for n in G.nodes()],
        'hovertext': node_text,
        'textposition': "top center",
        'marker': {
            'showscale': False,
            'color': node_color,
            'size': node_size,
            'line_width': 2
        },
        'type': 'scatter'
    }
    
    map_data = {
        'data': [edge_trace, path_trace, node_trace],
        'layout': {
            'showlegend': False,
            'hovermode': 'closest',
            'margin': {'b': 0, 'l': 0, 'r': 0, 't': 0},
            'xaxis': {'showgrid': False, 'zeroline': False, 'showticklabels': False},
            'yaxis': {'showgrid': False, 'zeroline': False, 'showticklabels': False},
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)'
        }
    }
    
    return json.dumps(map_data)

def generate_forecast_chart(forecast_df):
    if forecast_df is None or forecast_df.empty:
        return "{}"
        
    fig = go.Figure()
    
    # Confidence Interval
    if 'yhat_upper' in forecast_df.columns and 'yhat_lower' in forecast_df.columns:
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'], y=forecast_df['yhat_upper'],
            mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'], y=forecast_df['yhat_lower'],
            mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(245, 124, 0, 0.2)',
            showlegend=False, hoverinfo='skip'
        ))

    # Main Line
    fig.add_trace(go.Scatter(
        x=forecast_df['ds'], y=forecast_df['yhat'],
        mode='lines+markers', name='Prediction',
        line=dict(color='#142C63', width=4),
        marker=dict(size=10, color='#D92B7D')
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit", size=14, color="#142C63"),
        xaxis=dict(showgrid=False, title="Date"),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title="Predicted Attendance"),
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode="x unified"
    )
    return to_json(fig)

def generate_heatmap_chart(heatmap_df):
    if heatmap_df is None or heatmap_df.empty:
        return "{}"
        
    fig = px.density_heatmap(
        heatmap_df, x='Hour', y='Day', z='Crowd Level',
        color_continuous_scale=['#E3F2FD', '#142C63'], # Light blue to Dark Blue
        labels={'Crowd Level': 'Density'}
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit", size=12, color="#142C63"),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return to_json(fig)

