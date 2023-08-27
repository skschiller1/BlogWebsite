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

//var fuel_airports = document.getElementsByClassName("fuel-airports");
//if (fuel_airports.length > 1) {
//    var list_of_markers = [];
//
//    for (i = 0; i < fuel_airports.length; i++) {
//        alert(fuel_airports[i].innerHTML.split(","));
//        var namecalllatlong = fuel_airports[i].innerHTML.split(",");
//        let marker = L.marker([180/PI * parseFloat(namecalllatlong[2]), -180/PI * parseFloat(namecalllatlong[3])]).addTo(map);
//        list_of_markers.push(marker);
//    }
//}

const PI = Math.PI;
var x = document.getElementsByClassName("fuel-airports");
for (i = 0; i < x.length; i++) {
    if (window.getComputedStyle(x[i]).display === "none") {
        var string = x[i].innerHTML.split(",");
        let marker = L.marker([180/PI * parseFloat(string[2]), -180/PI * parseFloat(string[3])]).addTo(map);
        list_of_markers.push(marker);
    }
}


for (j = 0; j < x.length; j++) {
    list_of_markers[j].bindPopup(x[j].innerHTML.split()[0]).openPopup();
}

alert("Finished binding popups")
