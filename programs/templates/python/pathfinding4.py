import time
from programs.templates.python.functions import *

if __name__ == "__main__":
    G = [[] * 1 for i in range(5000)]
    path = []
    visited = [0]*100000
    minimum_line_distance = 100

    u, v = input("Enter starting and ending Airport Identifiers with space between:").split(" ")

    # start timing
    start_time = time.time()

    # create a database of airport objects and sort them by their distance to the destination airport
    airport_database = get_airports("airport_data/airport_data3.csv")
    ap_start, ap_end = get_start_end(u,v,airport_database)
    prelim_database = sort_and_slice(ap_start, ap_end, airport_database)

    dist = distance(ap_start, ap_end)
    points = generate_points(ap_start, ap_end, dist)
    sorted_database = db_linefilter(prelim_database,points,minimum_line_distance)

    if dist % 500 > 380:
        val = 2
    else:
        val = 1
    max_stops = int(dist // 500 + val)

    # find the connectivity of the airports, using the range of a cessna as a reference
    connectivity(sorted_database)

    # store the connectivity in a matrix used by the recursive program?
    with open("airport_data/connectivity.csv", "r") as f:
        lines = f.readlines()
        for line in lines:
            x, y = line.split(",")
            x = int(x)
            y = int(y)
            G[x].append(y)

    # run the pathfinding algorithm
    path.append(ap_start.id)
    with open("airport_data/paths.txt", 'w') as f3:
        dfs(visited, ap_start.id, ap_end.id, path, f3, max_stops, G)

    # Read path info from paths.txt; store paths as routes and compute cost and distance; plot data on map
    fuel_saved, xtra_dist = main(sorted_database, plott=False)
    end_time = time.time()

    print(f"\nTrip Distance: {round(dist,2)} miles")
    print(f"\nStarting airport: {ap_start}")
    print(f"Destination airport: {ap_end}")
    print(f"Max number of stops: {max_stops}")
    print(f"Fuel saved: ${round(fuel_saved,2)}")
    print(f"extra distance flown: {round(xtra_dist,2)} miles")
    print(end_time-start_time)
