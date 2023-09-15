import numpy as np
from math import sin, cos, asin, sqrt
# import matplotlib.pyplot as plt
# import geopandas as gpd
import myblogsite.settings as settings


airport_string = str(settings.BASE_DIR) + '/' + "programs/mypy/airport_data/airport_data.csv"
connectivity_string = str(settings.BASE_DIR) + '/' + "programs/mypy/airport_data/connectivity.txt"
paths_string = str(settings.BASE_DIR) + '/' + "programs/mypy/airport_data/paths.txt"


# Start of flightLib.py
# ------------------ #
class Route:
    def __init__(self, name, fc, dc, path, airport_list):
        self.name = name
        self.fuelcost = fc
        self.distance = dc
        self.path = path
        self.airport_path = []
        for p in path:
            self.airport_path.append(airport_list[p].name)

    def __repr__(self):
        return f"[{self.path}, {self.fuelcost}, {self.distance}]"

    def __dict__(self):
        return {f"{self.name}": [self.path, self.fuelcost, self.distance]}


class Airport:
    def __init__(self, id, name, callsign, lat, long, price):
        self.id = id
        self.name = name
        self.callsign = callsign
        self.lat = lat
        self.long = long
        self.price = price
        self.distance2end = None

    def __list__(self):
        return [self.id, self.name, self.callsign, round(self.lat,5), round(self.long,5), self.price, self.distance2end]

    def __str__(self):
        return f"{self.id}: [{self.name}, {self.callsign}, {round(self.lat,5)}, {round(self.long,5)}, {self.price}, {self.distance2end}]"

    def __dict__(self):
        return {"id": self.id, "name": self.name, "callsign": self.callsign, "lat": self.lat, "long": self.long, "price": self.price, "distance2end": self.distance2end}


# color help. Helps shade the colors when plotting
def chelp(c, k, maxk):
    if maxk == 0:
        if c=="green":
            color = "green"
        elif c=="blue":
            color = "blue"
        else:
            color="black"
    else:
        if c == "green":
            color = [0, ((255-100)/maxk * (maxk-k) + 100)/255, ((50-10)/maxk * (maxk-k) + 10)/255]
        elif c == "blue":
            color = [((21-10)/maxk * (maxk-k) + 10)/255, 0, ((255-121)/maxk * (maxk-k) + 121)/255]
        else:
            color="black"
    return color


# read a string from 'paths' and convert it into a list. Kinda dumb that I'm using this but oh well
def helper(string):
    nl = string.strip("\n").split(",")
    new_list = [int(item.strip("[").strip("]")) for item in nl]
    return new_list


def to_df(airport_list):
    airports = []
    latitudes = []
    longitudes = []
    for ap in airport_list:
        airports.append(ap.name)
        latitudes.append(ap.lat)
        longitudes.append(ap.long)

    d = {"Airport": airports, "Latitude": latitudes, "Longitude": longitudes}
    # df = pd.DataFrame(data=d)
    # return df


# start of functions.py
# ------------------- #


def dfs(visited, u, v, path, f, max_stops, G):
    visited[u] = 1
    if u == v:
        # print("Path found:", path)
        f.write(f"{path}\n")
    elif len(path) > max_stops:
        pass
    else:
        for i in range(len(G[u])):
            y = G[u][i]
            if visited[y] == 0:
                visited[y] = 1
                path.append(y)
                dfs(visited, y, v, path, f, max_stops, G)
                path.pop()

    visited[u] = 0


# compute the haversine distance in miles
def distance(a1, a2):
    d = 2 * asin(sqrt(sin((a1.lat - a2.lat)/2)**2 + cos(a1.lat)*cos(a2.lat)*sin((a1.long - a2.long)/2)**2)) * 6371 / 1.852
    return d


# function to solve for the longitude, given a guess for latitude
def solve(d,a1,a2):
    a3lat = (a1.lat + a2.lat) / 2
    error = 1000
    increment = 0.01
    a3long = 1.30
    while error > 0.0001:
        d1 = 2 * asin(sqrt(
            sin((a3lat - a1.lat) / 2) ** 2 + cos(a1.lat) * cos(a3lat) * sin((a3long - a1.long) / 2) ** 2)) * 6371 / 1.852
        d2 = 2 * asin(sqrt(
            sin((a2.lat - a3lat) / 2) ** 2 + cos(a3lat) * cos(a2.lat) * sin((a2.long - a3long) / 2) ** 2)) * 6371 / 1.852
        new_error = (d1 + d2) - d
        if new_error < error:
            pass
        else:
            increment = increment * -0.25
        a3long += increment
        error = new_error
        print(error, a3long)
    return a3long


def generate_points(a1, a2, dist):
    delta = dist / 6371 * 1.852  # convert to radians
    f = np.linspace(0,1,20)
    a = np.sin((1-f)*delta) / np.sin(delta)
    b = np.sin(f*delta) / np.sin(delta)
    x = a * np.cos(a1.lat) * np.cos(a1.long) + b * np.cos(a2.lat) * np.cos(a2.long)
    y = a * np.cos(a1.lat) * np.sin(a1.long) + b * np.cos(a2.lat) * np.sin(a2.long)
    z = a * np.sin(a1.lat) + b * np.sin(a2.lat)
    new_lat = np.arctan2(z,np.sqrt(x**2 + y**2))
    new_long = np.arctan2(y,x)
    line_db = []
    for i, p in enumerate(f):
        line_db.append(Airport(None,f"line_airport_{i+1}",None,new_lat[i],new_long[i],None))

    return line_db


def connectivity(airport_list,range):
    with open(connectivity_string, "w") as f:
        for a in airport_list:
            for ap in airport_list:
                if a.id < ap.id:
                    if 0.01 < distance(a, ap) < range:
                        f.write(f"{a.id},{ap.id}\n")


def get_airports(filename, fuel_type):
    with open(filename, 'r') as f:
        lines = f.readlines()
        ap_list = []
        for i, line in enumerate(lines):
            if filename == airport_string and i == 0:
                continue
            l = line.split(",")

            name, callsign, lat1, lat2, lat3, NS = l[0], l[1], l[2], l[3], l[4], l[5]
            long1, long2, long3, EW = l[6], l[7], l[8], l[9]
            city, state, country, access, month, year, control_tower = l[10], l[11], l[12], l[13], l[14], l[15], l[16]
            p1, p2, p3, p4, p5, p6 = l[17], l[18], l[19], l[20], l[21], l[22]
            lat = float(lat1) + float(lat2) / 60 + float(lat3) / 3600
            lat_radians = np.deg2rad(lat)
            long = float(long1) + float(long2) / 60 + float(long3) / 3600
            long_radians = np.deg2rad(long)

            LL100 = [p1, p3, p5]
            LL100 = [float(e) for e in LL100 if '.' in e]
            JETA = [p2, p4, p6]
            JETA = [float(e) for e in JETA if '.' in e]

            if fuel_type == "100ll":
                if len(LL100) > 0:
                    price = min(e for e in LL100 if isinstance(e, float))
                else:
                    price = 'na'
            elif fuel_type == "jeta":
                if len(JETA) > 0:
                    price = min(e for e in JETA if isinstance(e, float))
                else:
                    price = 'na'

            # append every airport to the list, but set the price of airports without fuel to 'na'
            airport = Airport(i,name,callsign,lat_radians,long_radians,price)
            ap_list.append(airport)
    return ap_list


# calculate the fuel cost and distance travelled
def cost_function(ap_list, path, mpg):
    c = 0
    dist = 0
    for i, p in enumerate(path):
        if i < len(path) - 1:
            d = distance(ap_list[path[i+1]], ap_list[path[i]])
            f = d / mpg
            try:
                c += f * ap_list[path[i+1]].price
            except TypeError:
                c += 100000
            dist += d

    return c, dist


def get_start_end(u,v, db):
    for line in db:
        if u in line.callsign:
            start = line
        if v in line.callsign:
            end = line
    try:
        return start, end
    except Exception as e:
        raise Exception("start or end airport not found in airport database. Check spelling and availability of airport.")


def sort_and_slice(u,v,db):
    remove_list = []
    for ap in db:
        if type(ap.price) == str:
            remove_list.append(ap)
    for ap in remove_list:
        db.remove(ap)
    for ap in db:
        ap.distance2end = distance(ap, v)
    db.sort(key=lambda x: x.distance2end, reverse=True)
    db_sliced = db[db.index(u):]
    return db_sliced


def db_linefilter(db, line_db, min_distance):
    remove_list = []
    for ap in db:
        remove_flag_list = []
        for lap in line_db:
            if distance(ap, lap) < min_distance:  # if within distance, mark as keep
                remove_flag_list.append(1)
            else:
                remove_flag_list.append(0)
        if 1 not in remove_flag_list:
            remove_list.append(ap)
    for ap in remove_list:
        db.remove(ap)
    return db


# return all the airports that have fuel less than the 1st standard deviation
def standard_deviation(db, num):
    samples = []
    for ap in db:
        samples.append(ap.price)
    mean = np.average(samples)
    sig = np.std(samples)
    remove_list = []
    for i, ap in enumerate(db):
        if ap.price > mean + num * sig and i != 0 and i != len(db) - 1:
            remove_list.append(ap)
    for ap in remove_list:
        db.remove(ap)
    for i, ap in enumerate(db):  # compute the new airport IDs. Not 100% sure I need to do this
        ap.id = i
    return db


def processing(db, fuel_mileage, fuel_type):
    route_list = []
    with open(paths_string, "r") as f2:
        lines = f2.readlines()
        for i, line in enumerate(lines):
            new_line = helper(line)
            fc, dc = cost_function(db, new_line, fuel_mileage, fuel_type)
            route_list.append(Route(f"Route{i}", fc, dc, new_line, db))

        if len(route_list) > 5:
            maxk = 5
        else:
            maxk = len(route_list)
            if maxk == 0:
                # raise Exception("No routes found. Try expanding 'max_stops', or increasing 'minimum_line_distance'")
                return -1

        # find the top 5 (or whatever maxk is) routes for both distance and fuel savings, and plot them
        for k in range(maxk):
            minfuel_list = sorted(route_list, key=lambda x: x.fuelcost)
            mindist_list = sorted(route_list, key=lambda x: x.distance)
            route_minfuel = minfuel_list[k]
            route_mindistance = mindist_list[k]

            latd = []
            longd = []
            for loc in route_mindistance.path:
                latd.append(np.rad2deg(db[int(loc)].lat))
                longd.append(np.rad2deg(db[int(loc)].long))
                ap = db[loc]

            latf = []
            longf = []
            for loc in route_minfuel.path:
                latf.append(np.rad2deg(db[int(loc)].lat))
                longf.append(np.rad2deg(db[int(loc)].long))
                ap = db[loc]

        # data output section! WHOOP!
        print("\nTop 5 Shortest Routes")
        for item in mindist_list[:5]:
            print(item.name, "$" + str(round(item.fuelcost, 2)), " ", round(item.distance, 2), f"miles.   {item.path}")

        print("\nTop 5 Cheapest Fuel Routes")
        for item in minfuel_list[:5]:
            print(item.name, "$" + str(round(item.fuelcost, 2)), " ", round(item.distance, 2), f"miles.   {item.path}")

        print("\nAirports visited:")
        for apid in minfuel_list[0].path:
            print(db[apid])

        fuel_savings = mindist_list[0].fuelcost - minfuel_list[0].fuelcost
        extra_distance = minfuel_list[0].distance - mindist_list[0].distance
        return fuel_savings, extra_distance, mindist_list[:5], minfuel_list[:5]


# Start of pathfinding4.py
# ----------------- #

def main(u,v,aircraft_range, aircraft_mpg, fuel_type, aircraft_cruise, sigma):
    G = [[] * 1 for i in range(5000)]
    path = []
    visited = [0]*100000
    minimum_line_distance = 100

    # start timing

    # create a database of airport objects and sort them by their distance to the destination airport
    airport_database = get_airports(airport_string, fuel_type)
    ap_start, ap_end = get_start_end(u,v,airport_database)
    prelim_database = sort_and_slice(ap_start, ap_end, airport_database)

    dist = distance(ap_start, ap_end)
    points = generate_points(ap_start, ap_end, dist)
    sorted_database = db_linefilter(prelim_database,points,minimum_line_distance)
    sorted_reduced_database = standard_deviation(sorted_database, sigma)

    # find the connectivity of the airports, using the range of a cessna as a reference
    connectivity(sorted_reduced_database,aircraft_range)

    # store the connectivity in a matrix used by the recursive program?
    with open(connectivity_string, "r") as f:
        lines = f.readlines()
        for line in lines:
            x, y = line.split(",")
            x = int(x)
            y = int(y)
            G[x].append(y)

    max_stops = int(dist // aircraft_range + 1)
    print(dist, aircraft_range, max_stops)

    # run the pathfinding algorithm
    path.append(ap_start.id)
    with open(paths_string, 'w') as f3:
        dfs(visited, ap_start.id, ap_end.id, path, f3, max_stops, G)

    # Read path info from paths.txt; store paths as routes and compute cost and distance
    try:
        fuel_saved, xtra_dist, min_dist, min_fuel = processing(sorted_reduced_database, aircraft_mpg, fuel_type)
    except:
        max_stops += 1
        path = []
        path.append(ap_start.id)
        with open(paths_string, 'w') as f3:
            dfs(visited, ap_start.id, ap_end.id, path, f3, max_stops, G)
        try:
            fuel_saved, xtra_dist, min_dist, min_fuel = processing(sorted_reduced_database, aircraft_mpg, fuel_type)
        except:
            raise Exception("No Routes found. Try increasing 'max_stops' or 'minimum_line_distance'.")
            # max_stops += 1
            # path = []
            # path.append(ap_start.id)
            # with open(paths_string, 'w') as f3:
            #     dfs(visited, ap_start.id, ap_end.id, path, f3, max_stops, G)
            # try:
            #     fuel_saved, xtra_dist, min_dist, min_fuel = processing(sorted_reduced_database, aircraft_mpg, fuel_type)
            # except:
            #     max_stops += 2
            #     path = []
            #     path.append(ap_start.id)
            #     with open(paths_string, 'w') as f3:
            #         dfs(visited, ap_start.id, ap_end.id, path, f3, max_stops, G)
            #     fuel_saved, xtra_dist, min_dist, min_fuel = processing(sorted_reduced_database, aircraft_mpg, fuel_type)

    # if len(min_dist) == 1:
    #     max_stops += 1
    #     path = []
    #     path.append(ap_start.id)
    #     with open(paths_string, 'w') as f3:
    #         dfs(visited, ap_start.id, ap_end.id, path, f3, max_stops, G)
    #     fuel_saved, xtra_dist, min_dist, min_fuel = processing(sorted_database, aircraft_mpg, fuel_type)


    airports_d = []
    airports_f = []
    for i, item in enumerate(min_dist):
        if i == 0:
            for apid in item.path:
                airports_d.append(sorted_reduced_database[apid].__list__())
    for i, item in enumerate(min_fuel):
        if i == 0:
            for apid in item.path:
                airports_f.append(sorted_reduced_database[apid].__list__())

    return_list = [round(fuel_saved,2), round(xtra_dist,2), airports_f, airports_d,
                   [round(min_fuel[0].fuelcost,2), round(min_fuel[0].distance,2)],
                   [round(min_dist[0].fuelcost,2), round(min_dist[0].distance,2)],
                   round(min_fuel[0].distance / aircraft_cruise,2),
                   round(min_dist[0].distance / aircraft_cruise,2)]
    return return_list
