// Initialize the map
const map = L.map('map')

// Get the tile layer from OpenStreetMaps
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {

// Specify the maximum zoom of the map
maxZoom: 19,

// Set the attribution for OpenStreetMaps
attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Set the view of the map
// with the latitude, longitude and the zoom value
map.setView([38.6280, -96.3344], 4);

// Set the map view to the user's location
// Uncomment below to set map according to user location
// map.locate({setView: true, maxZoom: 16});

// Show a marker at the position of the Eiffel Tower

var fuel_airports = document.getElementsByClassName("fuel-airports");
alert("Made it past fuel_airports");
if (fuel_airports.length > 1) {
    var list_of_markers = [];
    var PI = Math.PI;
    for (i = 0; i < fuel_airports.length; i++) {
        alert(fuel_airports[i].innerHTML);
        var namecalllatlong = fuel_airports[i].innerHTML.split(",");
        let marker = L.marker([PI/180 * parseFloat(namecalllatlong[2]), PI/180 * parseFloat(namecalllatlong[3])]).addTo(map);

        list_of_markers.push(marker);
    }
}
alert("Finished appending markers")
for (j = 0; i < fuel_airports.length; j++) {
    list_of_markers[j].bindPopup(fuel_airports[j].innerHTML.split()[0]).openPopup();
}
alert("Finished binding popups")

let eiffelMarker = L.marker([48.8584, 2.2945]).addTo(map);
// let marker1 = L.marker([]).addTo(map)

// Bind popup to the marker with a popup
//