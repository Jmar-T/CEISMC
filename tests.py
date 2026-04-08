from move_data import* 
from dijkstra import dijkstra

#Test Case 1 (Simple)
sample_map_data = [
    [(2, 0), (1, 42)],                    # Connections for Node 0
    [(0, 42), (2, 17), (3, 21), (4, 83)], # Connections for Node 1
    [(0, 0), (1, 17), (3, 91), (4, 59)],  # Connections for Node 2
    [(1, 21), (2, 91), (4, 24)],          # Connections for Node 3
    [(1, 83), (2, 59), (3, 24)]           # Connections for Node 4
]
## variable parameters
map_to_run = office_map_data
start = 0

distances, paths = dijkstra(map_to_run, start)

# print(f"--- Trip Results starting from Node {start} ---")
# for node_id in range(len(distances)):
#     # Convert numbers to strings so we can join them with arrows
#     path_as_strings = [str(n) for n in paths[node_id]]
#     path_format = " -> ".join(path_as_strings)
#     print(f"To Node {node_id}: Route: [{path_format}] | Total Cost: {distances[node_id]}")

print(FINAL_MOVE_DATA)