import graph_utils

print("Loading graph...")
try:
    G = graph_utils.load_graph()
    print("Graph loaded successfully.")
    
    # Coords for testing: around Hoan Kiem
    start = (21.0285, 105.8542)
    end = (21.0300, 105.8500)
    
    print(f"Testing route from {start} to {end}...")
    path_nodes = graph_utils.get_shortest_path(G, start, end)
    print("Nodes:", len(path_nodes))
    
    stats = graph_utils.get_route_stats(G, path_nodes)
    print("Stats:", stats)
    
    print("Test passed!")
except Exception as e:
    print(f"Test failed with error: {e}")
    import traceback
    traceback.print_exc()
