from backend import graph_utils
import osmnx as ox

print("Loading graph...")
G = graph_utils.load_graph()
print("Graph loaded.")

# Lat, Lng for some point in Hanoi (e.g. near Hoan Kiem)
test_point = (21.0285, 105.8542)

print(f"Test point: {test_point}")
nearest_lat, nearest_lng = graph_utils.get_nearest_node(G, test_point)
print(f"Nearest node coords: {nearest_lat}, {nearest_lng}")

# Check if they really are different (if we pick a point slightly off a node)
off_point = (21.0286, 105.8543)
print(f"Off point: {off_point}")
n_lat, n_lng = graph_utils.get_nearest_node(G, off_point)
print(f"Nearest to off point: {n_lat}, {n_lng}")

if n_lat == off_point[0] and n_lng == off_point[1]:
    print("FAIL: Nearest node is exactly the same as input point (unlikely unless we clicked exactly on a node)")
else:
    print("SUCCESS: Result is snapped to a node")
