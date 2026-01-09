from flask import Flask, jsonify, request
from flask_cors import CORS
import graph_utils
import os

app = Flask(__name__)
CORS(app)

print("Initializing Graph...")
# Load the graph globally on startup
G = graph_utils.load_graph()
print("Graph Loaded!")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/route', methods=['POST'])
def get_route():
    data = request.json
    start = data.get('start') # [lat, lng]
    end = data.get('end')     # [lat, lng]
    start_node_id = data.get('startNodeId')
    end_node_id = data.get('endNodeId')
    
    algo = data.get('algorithm', 'dijkstra') # 'dijkstra' or 'astar'
    
    if (not start or not end) and (not start_node_id or not end_node_id):
        # Allow if we at least have coordinates.
        # Ideally we want node IDs, but fallbacks are good.
        if not start or not end:
             return jsonify({"error": "Missing start or end coordinates"}), 400

    try:
        path_nodes = graph_utils.get_shortest_path(
            G, 
            tuple(start) if start else None, 
            tuple(end) if end else None, 
            algorithm=algo,
            start_node_id=start_node_id,
            end_node_id=end_node_id
        )
        path_coords = graph_utils.path_to_coords(G, path_nodes)
        stats = graph_utils.get_route_stats(G, path_nodes)
        
        return jsonify({
            "path": path_coords,
            "algorithm": algo,
            "stats": stats
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nearest-node', methods=['POST'])
def get_nearest_node_endpoint():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    
    if lat is None or lng is None:
        return jsonify({"error": "Missing lat or lng"}), 400

    try:
        node_id, nearest_lat, nearest_lng = graph_utils.get_nearest_node(G, (lat, lng))
        return jsonify({
            "id": node_id,
            "lat": nearest_lat,
            "lng": nearest_lng
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
