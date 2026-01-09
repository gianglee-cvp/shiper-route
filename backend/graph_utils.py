import osmnx as ox
import networkx as nx
import os
from shapely.geometry import LineString

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPH_FILE = os.path.join(SCRIPT_DIR, "hanoi_graph.graphml")

def load_graph(place_name="Hoan Kiem, Hanoi, Vietnam", dist=5000):
    """
    Load graph from file or download from OSM.
    The graph is a MultiDiGraph which properly handles:
    - One-way streets (directed edges)
    - Two-way streets (edges in both directions)
    """
    if os.path.exists(GRAPH_FILE):
        print("Loading graph from file...")
        G = ox.load_graphml(GRAPH_FILE)
    else:
        print(f"Downloading graph for {place_name}...")
        # Hoan Kiem Lake coords: 21.0285, 105.8542
        center_point = (21.0285, 105.8542) 
        
        # network_type='drive' ensures we get drivable roads
        # OSMnx automatically handles one-way streets:
        # - For one-way streets: creates a single directed edge
        # - For two-way streets: creates edges in both directions
        G = ox.graph_from_point(center_point, dist=dist, network_type='drive')
        
        print("Saving graph to file...")
        ox.save_graphml(G, GRAPH_FILE)
    
    # Add edge speeds and travel times based on road type
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)
    
    print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G



def path_to_coords(G, path):
    """
    Convert list of node IDs to list of [lat, lng] coordinates.
    Uses actual road geometry (not just straight lines between nodes).
    
    This extracts the 'geometry' attribute from each edge if available,
    which contains the actual shape of the road including curves.
    """
    if len(path) < 2:
        # Single node or empty path
        if len(path) == 1:
            node = path[0]
            return [[G.nodes[node]['y'], G.nodes[node]['x']]]
        return []
    
    coords = []
    
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        
        # Get edge data - may have multiple edges between same nodes
        edge_data = G.get_edge_data(u, v)
        
        if edge_data is None:
            # Fallback: just use node coordinates
            coords.append([G.nodes[u]['y'], G.nodes[u]['x']])
            continue
        
        # Get the first edge (key 0) - in case of parallel edges
        if 0 in edge_data:
            data = edge_data[0]
        else:
            data = list(edge_data.values())[0]
        
        # Check if edge has geometry (curved road shape)
        if 'geometry' in data:
            geom = data['geometry']
            # Handle both string (from graphml) and LineString objects
            if isinstance(geom, str):
                # Parse from WKT string (saved in graphml)
                from shapely import wkt
                geom = wkt.loads(geom)
            
            # Extract coordinates from geometry
            if isinstance(geom, LineString):
                # geom.coords gives (lng, lat) pairs, we need [lat, lng]
                for coord in geom.coords:
                    coords.append([coord[1], coord[0]])
            else:
                # Fallback to node coordinate
                coords.append([G.nodes[u]['y'], G.nodes[u]['x']])
        else:
            # No geometry, use node coordinate
            coords.append([G.nodes[u]['y'], G.nodes[u]['x']])
    
    # Add the last node
    last_node = path[-1]
    coords.append([G.nodes[last_node]['y'], G.nodes[last_node]['x']])
    
    # Remove consecutive duplicates
    cleaned_coords = [coords[0]]
    for coord in coords[1:]:
        if coord != cleaned_coords[-1]:
            cleaned_coords.append(coord)
    
    return cleaned_coords

def get_route_stats(G, path):
    """
    Calculate statistics for a route.
    Returns total distance (meters) and estimated travel time (seconds).
    """
    total_length = 0
    total_time = 0
    
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        
        edge_data = G.get_edge_data(u, v)
        if edge_data:
            if 0 in edge_data:
                data = edge_data[0]
            else:
                data = list(edge_data.values())[0]
            
            total_length += data.get('length', 0)
            total_time += data.get('travel_time', 0)
    
    return {
        'distance_meters': round(total_length, 2),
        'distance_km': round(total_length / 1000, 2),
        'travel_time_seconds': round(total_time, 2),
        'travel_time_minutes': round(total_time / 60, 2)
    }

def get_nearest_node(G, point):
    """
    Find the nearest node in the graph to a given (lat, lng) point.
    Returns (node_id, lat, lng).
    """
    # ox.distance.nearest_nodes takes (G, X, Y) where X is lng, Y is lat
    node_id = ox.distance.nearest_nodes(G, point[1], point[0])
    
    node = G.nodes[node_id]
    return node_id, node['y'], node['x']

def get_shortest_path(G, origin_point, dest_point, weight='travel_time', algorithm='dijkstra', start_node_id=None, end_node_id=None):
    """
    Find shortest path between two points.
    If start_node_id/end_node_id are provided, uses them directly.
    Otherwise functionality remains finding nearest nodes to coords.
    """
    if start_node_id is not None:
        orig_node = start_node_id
    else:
        orig_node = ox.distance.nearest_nodes(G, origin_point[1], origin_point[0])

    if end_node_id is not None:
        dest_node = end_node_id
    else:
        dest_node = ox.distance.nearest_nodes(G, dest_point[1], dest_point[0])
    
    print(f"Finding path from node {orig_node} to {dest_node} using {algorithm}")
    
    path = None
    if algorithm == 'dijkstra':
        path = nx.shortest_path(G, orig_node, dest_node, weight=weight)
    elif algorithm == 'astar':
        # A* with haversine heuristic for geographic data
        def heuristic(u, v):
            return ox.distance.great_circle(
                G.nodes[u]['y'], G.nodes[u]['x'],
                G.nodes[v]['y'], G.nodes[v]['x']
            )
        path = nx.astar_path(G, orig_node, dest_node, heuristic=heuristic, weight=weight)
    else:
        path = nx.shortest_path(G, orig_node, dest_node, weight=weight)
    
    print(f"Path found with {len(path)} nodes")
    return path
