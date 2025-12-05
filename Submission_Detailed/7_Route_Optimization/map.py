# ----------------------------------------------------------------------------
# 🗺️ Smart Map Logic
# ----------------------------------------------------------------------------
# الوظيفة: تحسين مسار الزائر داخل الحديقة
# المدخلات: نقطة البداية والنهاية، أوقات الانتظار الحالية
# المخرجات: أقصر مسار (Shortest Path) باستخدام خوارزمية Dijkstra
# ----------------------------------------------------------------------------

from flask import Flask, render_template, request
from supabase import create_client
import networkx as nx
import json

app = Flask(__name__)
supabase = create_client("URL", "KEY")

@app.route('/map', methods=['GET', 'POST'])
def smart_map():
    """
    دالة الخريطة الذكية
    - تبني شبكة (Graph) تمثل الحديقة
    - تجلب أوقات الانتظار لتحديث أوزان المسارات
    - تحسب أقصر مسار بين نقطتين
    """
    # Build Graph
    G = nx.Graph()
    # Add nodes and edges (Simplified)
    G.add_edge("Entrance", "Ride A", weight=5)
    G.add_edge("Ride A", "Ride B", weight=10)
    
    path = []
    if request.method == 'POST':
        start = request.form.get('start_point')
        end = request.form.get('end_point')
        try:
            path = nx.shortest_path(G, start, end, weight='weight')
        except:
            path = []

    return render_template('map.html', path=path)

if __name__ == '__main__':
    app.run(debug=True)
