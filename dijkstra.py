import heapq
def dijkstra(graph, start_node):
    """
    Compute Dijkstra's algorithm
    Finds the quickest way to get from a starting 
    node to every other location.
    
    :param graph: A list where each index is a 'current_node" and contains its nieghboring connections.
    :param start_node: The 'current_node' we are starting our journey from.
    :return: A list of shortest distances and the actual paths to take.
    """

    #1 Setup:
    #Assume every current_node has a "infinite" distance between them, until we find a path.
    total_distances = [float("inf")] * len(graph)
    total_distances[start_node] = 0
    
    visited_nodes = set()
    travel_paths = [[] for _ in range(len(graph))]

    #2 The Priority Queue (The 'To-Vsit' List)
    # We store tuples of (current_total_distance, current_node, previous_node)
    # The heapq keeps the smallest distance at the very top.
    unvisited_queue = [(0, start_node, None)]
    
    while unvisited_queue:
        #Pick the node with the shortest distanced discovered so far
        current_distance, current_node, parent_node = heapq.heappop(unvisited_queue)
        
        #if we've already visited this node, then we have
        #already found a shorter path to it, so we skip it.
        if current_node in visited_nodes:
            continue

        #Mark this node as 'visited' and update the distance
        visited_nodes.add(current_node)
        total_distances[current_node] = current_distance
        #Build the path list (e.g., [0, 2, 3] meants start at 0, go to 2, then to 3)
        if parent_node is None:
            travel_paths[current_node] = [start_node]
        else:
            travel_paths[current_node] = travel_paths[parent_node] + [current_node]

        #3 Check Neighbors:
        # Look at all nodes connected to the current one
        for neighbor, weight in graph[current_node]:
            if neighbor not in visited_nodes:
                #Calculate: "Distance to current_node" + "Distance to neighbor"
                new_distance = current_distance + weight 
                heapq.heappush(unvisited_queue, (new_distance, neighbor, current_node))
    return total_distances, travel_paths

# --- Example Usage ---
# Think of this as a map of 5 nodes (0 to 4) and the 'cost' (time/miles) to travel between them.
#          [0]
#         /   \
#        /     \
#     42/       \0
#      /         \
#     /           \
#   [1]-----------[2]
#    |\    17     /|
#    | \         / |
#    |  \_______/  |
#    |   /     \   |
#  21| 83/     \59 |91
#    |  /       \  |
#    | /         \ |
#    |/           \|
#   [3]-----------[4]
#          24
map_data = [
    [(2, 0), (1, 42)],                    # Connections for Node 0
    [(0, 42), (2, 17), (3, 21), (4, 83)], # Connections for Node 1
    [(0, 0), (1, 17), (3, 91), (4, 59)],  # Connections for Node 2
    [(1, 21), (2, 91), (4, 24)],          # Connections for Node 3
    [(1, 83), (2, 59), (3, 24)]           # Connections for Node 4
]
start = 0
distances, paths = dijkstra(map_data, start)

print(f"--- Trip Results starting from Node {start} ---")
for node_id in range(len(distances)):
    # Convert numbers to strings so we can join them with arrows
    path_as_strings = [str(n) for n in paths[node_id]]
    path_format = " -> ".join(path_as_strings)
    print(f"To Node {node_id}: Route: [{path_format}] | Total Cost: {distances[node_id]}")

