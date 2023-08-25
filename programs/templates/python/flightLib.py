import pandas as pd


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

    def __repr__(self):
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
    df = pd.DataFrame(data=d)
    return df

