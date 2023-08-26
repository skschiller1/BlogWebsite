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
    for (i = 0; i < fuel_airports.length; i++) {
        alert("Inside for loop");
        alert(fuel_airports[i].innerHTML);
        var latlong = fuel_airports[i].split();
        alert("Made it after lat long");
        let marker = L.marker([parseFloat(latlong[0]), parseFloat(latlong[0])]).addTo(map);
    }
}

let eiffelMarker = L.marker([48.8584, 2.2945]).addTo(map);
// let marker1 = L.marker([]).addTo(map)

// Bind popup to the marker with a popup
// eiffelMarker.bindPopup("Eiffel Tower").openPopup();