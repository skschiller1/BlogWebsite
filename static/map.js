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
if (fuel_airports.length > 1) {
    var list_of_markers = [];
    var PI = Math.PI;
    for (i = 0; i < fuel_airports.length; i++) {
    alert(fuel_airports[i].innerHTML.split(","));
        var namecalllatlong = fuel_airports[i].innerHTML.split(",");
        let marker = L.marker([180/PI * parseFloat(namecalllatlong[2]), -180/PI * parseFloat(namecalllatlong[3])]).addTo(map);
        list_of_markers.push(marker);
    }
}

for (j = 0; i < fuel_airports.length; j++) {
    list_of_markers[j].bindPopup(fuel_airports[j].innerHTML.split()[0]).openPopup();
}

//var dist_airports = document.getElementsByClassName("dist-airports");
//if (dist_airports.length > 1) {
//    var list_dist_of_markers = [];
//    var PI = Math.PI;
//    for (i = 0; i < dist_airports.length; i++) {
//        var namecalllatlongdist = dist_airports[i].innerHTML.split(",");
//        let marker_dist = L.marker([180/PI * parseFloat(namecalllatlongdist[2]), -180/PI * parseFloat(namecalllatlongdist[3])]).addTo(map);
//        list_of_dist_markers.push(marker_dist);
//    }
//}
//
//for (j = 0; i < dist_airports.length; j++) {
//    list_of_dist_markers[j].bindPopup(dist_airports[j].innerHTML.split()[0]).openPopup();
//}

alert("Finished binding popups")
