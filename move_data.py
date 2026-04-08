## Move Data (Directed Map of Office)
# Format: (From_Node, To_Node): (Distance_Inches, Heading_Degrees)
DIRECTED_MOVE_DATA = {
    (0, 1): (7, 0),
    (1, 2): (3, 90),
    (1, 3): (8, 270),
    (3, 4): (7, 180),
    (3, 5): (2, 270),
    (5, 6): (5, 0),
    (6, 7): (3, 270),
    (6, 8): (6, 0), 
    (8, 9): (9, 90),
    (9, 10): (3, 0),
    (9, 11): (4, 90),
    (11, 1): (11, 180)
}

n = 12 #Number of locations of map
office_map_data = [[] for i in range(n)]

##Undirected Move Data
FINAL_MOVE_DATA = {}

for key,val in DIRECTED_MOVE_DATA.items():
    start,finish = key
    distance, direction = val
    FINAL_MOVE_DATA[key] = val
    FINAL_MOVE_DATA[(finish, start)] = (distance, (direction + 180)%360)
    office_map_data[start].append((finish, distance))
    office_map_data[finish].append((start, distance))