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
    algo = data.get('algorithm', 'dijkstra') # 'dijkstra' or 'astar'
    
    if not start or not end:
        return jsonify({"error": "Missing start or end coordinates"}), 400

    try:
        path_nodes = graph_utils.get_shortest_path(G, tuple(start), tuple(end), algorithm=algo)
        path_coords = graph_utils.path_to_coords(G, path_nodes)
        stats = graph_utils.get_route_stats(G, path_nodes)
        
        return jsonify({
            "path": path_coords,
            "algorithm": algo,
            "stats": stats
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
