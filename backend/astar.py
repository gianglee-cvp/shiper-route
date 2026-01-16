import heapq
import networkx as nx

def astar_path(G, source, target, heuristic, weight='length'):
    if source == target:
        return [source]
        
    count = 0 
    pq = [(0, count, source)]
    g_score = {source: 0}
    f_score = {source: heuristic(source, target)}
    parent = {}
    visited = set()
    
    while pq:
        _, _, u = heapq.heappop(pq)
        
        if u == target:
            break

        if u in visited:
            continue
        visited.add(u)
            
        for v in G[u]:
            min_weight = float('inf')
            edge_data = G[u][v]
            
            for key in edge_data:
                attr = edge_data[key]
                w = attr.get(weight, 1)
                if w < min_weight:
                    min_weight = w
            
            tentative_g_score = g_score[u] + min_weight
            
            if tentative_g_score < g_score.get(v, float('inf')):
                parent[v] = u
                g_score[v] = tentative_g_score
                f = tentative_g_score + heuristic(v, target)
                f_score[v] = f
                count += 1
                heapq.heappush(pq, (f, count, v))
                
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
