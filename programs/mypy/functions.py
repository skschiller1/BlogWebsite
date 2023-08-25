import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sin, cos, asin, sqrt
import geopandas as gpd
from flightLib import Route, Airport, chelp, helper


def dfs(visited, u, v, path, f, max_stops, G):
    visited[u] = 1
    if u == v:
        print("Path found:", path)
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
    d = 2 * asin(sqrt(sin((a1.lat - a2.lat)/2)**2 + cos(a1.lat)*cos(a2.lat)*sin((a1.long - a2.long)/2)**2)) * 6371 / 1.609
    return d


# function to solve for the longitude, given a guess for latitude
def solve(d,a1,a2):
    a3lat = (a1.lat + a2.lat) / 2
    error = 1000
    increment = 0.01
    a3long = 1.30
    while error > 0.0001:
        d1 = 2 * asin(sqrt(
            sin((a3lat - a1.lat) / 2) ** 2 + cos(a1.lat) * cos(a3lat) * sin((a3long - a1.long) / 2) ** 2)) * 6371 / 1.609
        d2 = 2 * asin(sqrt(
            sin((a2.lat - a3lat) / 2) ** 2 + cos(a3lat) * cos(a2.lat) * sin((a2.long - a3long) / 2) ** 2)) * 6371 / 1.609
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
    delta = dist / 6371 * 1.609  # convert to radians
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


def connectivity(airport_list):
    with open("airport_data/connectivity.csv", "w") as f:
        for a in airport_list:
            for ap in airport_list:
                if a.id < ap.id:
                    if 0.01 < distance(a, ap) < 513:
                        f.write(f"{a.id},{ap.id}\n")


def get_airports(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        ap_list = []
        for i, line in enumerate(lines):
            if filename == "airport_data/airport_data3.csv" and i == 0:
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
            if len(LL100) > 0:
                LL100price = min(e for e in LL100 if isinstance(e, float))
            else:
                LL100price = 'na'

            # append every airport to the list, but set the price of airports without fuel to 'na'
            airport = Airport(i,name,callsign,lat_radians,long_radians,LL100price)
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
    return start, end


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
    for i, ap in enumerate(db_sliced):
        ap.id = i
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
    for i, ap in enumerate(db):
        ap.id = i
    return db


def main(db, plott):
    route_list = []
    with open("airport_data/paths.txt", "r") as f2:
        lines = f2.readlines()
        for i, line in enumerate(lines):
            new_line = helper(line)
            fc, dc = cost_function(db, new_line, 17.1)
            route_list.append(Route(f"Route{i}", fc, dc, new_line, db))

        fig, (ax1, ax2) = plt.subplots(1, 2)

        if len(route_list) > 5:
            maxk = 5
        else:
            maxk = len(route_list)
            if maxk == 0:
                raise Exception("No routes found. Try expanding 'max_stops', or increasing 'minimum_line_distance'")
        if plott:
            world = gpd.read_file("ne_10m_admin_0_states/ne_10m_admin_1_states_provinces.shp")
            ax = world.plot(color="white", edgecolor="black")

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
                if plott:
                    ax1.annotate(ap.name, [np.rad2deg(ap.long), np.rad2deg(ap.lat)])
                    ax1.scatter(np.rad2deg(ap.long), np.rad2deg(ap.lat), color="black", s=8)

            latf = []
            longf = []
            for loc in route_minfuel.path:
                latf.append(np.rad2deg(db[int(loc)].lat))
                longf.append(np.rad2deg(db[int(loc)].long))
                ap = db[loc]
                if plott:
                    ax2.annotate(f"{ap.name}", [np.rad2deg(ap.long), np.rad2deg(ap.lat)])
                    ax2.scatter(np.rad2deg(ap.long), np.rad2deg(ap.lat), color="black", s=8)

            # convert airport geocordinates into a geopandas dataframes to plot routes on world map!
            if k == 0:
                dist_d = {"Airport": route_mindistance.airport_path, "Latitude": latd, "Longitude": longd}
                dist_df = pd.DataFrame(data=dist_d)
                fuel_d = {"Airport": route_minfuel.airport_path, "Latitude": latf, "Longitude": longf}
                fuel_df = pd.DataFrame(data=fuel_d)
                ap_dist = gpd.GeoDataFrame(dist_df, geometry=gpd.points_from_xy(-dist_df.Longitude, dist_df.Latitude),
                                           crs="EPSG:4326")
                ap_fuel = gpd.GeoDataFrame(fuel_df, geometry=gpd.points_from_xy(-fuel_df.Longitude, fuel_df.Latitude),
                                           crs="EPSG:4326")
                if plott:
                    ad = ap_dist.plot(ax=ax, color="blue", markersize=5)
                    af = ap_fuel.plot(ax=ax, color="green", markersize=5)

            if plott:
                ax1.plot(longd, latd, color=chelp("blue", k, maxk - 1), label=f"d{k + 1}")
                ax2.plot(longf, latf, color=chelp("green", k, maxk - 1), label=f"f{k + 1}")

        # ax.set_xlim([min(dist_df.Longitude) * .9, max(dist_df.Longitude) * 1.1])
        # ax.set_ylim([min(dist_df.Latitude) * .9, max(dist_df.Latitude) * 1.1])
        if plott:
            ax1.invert_xaxis()
            ax2.invert_xaxis()
            ax1.set_title("Minimized distance routes")
            ax2.set_title("Minimized fuel cost routes")
            ax1.legend()
            ax2.legend()
            plt.show()

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
        return fuel_savings, extra_distance