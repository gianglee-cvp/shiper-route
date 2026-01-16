import heapq
import networkx as nx

def dijkstra_path(G, source, target, weight='length'):
    if source == target:
        return [source]
    
    pq = [(0, source)]
    dist = {source: 0}
    parent = {}
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        
        if u in visited:
            continue
        visited.add(u)
        
        if u == target:
            break
            
        if d > dist.get(u, float('inf')):
             continue

        for v in G[u]:
            min_weight = float('inf')
            edge_data = G[u][v]
            
            for key in edge_data:
                attr = edge_data[key]
                w = attr.get(weight, 1)
                if w < min_weight:
                    min_weight = w
            
            if dist.get(u, float('inf')) + min_weight < dist.get(v, float('inf')):
                dist[v] = dist[u] + min_weight
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
                
    if target not in parent:
        raise nx.NetworkXNoPath(f"Node {target} not reachable from {source}")
        
    path = []
    curr = target
    while curr != source:
        path.append(curr)
        curr = parent[curr]
    path.append(source)
    path.reverse()
    return path
