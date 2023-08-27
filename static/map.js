function MarkerFunction(x, map, color) {
    var myIcon = L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [38, 95],
        iconAnchor: [22, 94],
        popupAnchor: [-3, -76],
        shadowSize: [68, 95],
        shadowAnchor: [22, 94]
    });

    const PI = Math.PI;
    var marker_list = [];
    for (i = 0; i < x.length; i++) {
        if (window.getComputedStyle(x[i]).display === "none") {
            var string = x[i].innerHTML.split(",");
            if (color === "green") {
                var marker = L.marker([180/PI * parseFloat(string[0]), -180/PI * parseFloat(string[1])], {icon: myIcon}).addTo(map);
            } else {
                var marker = L.marker([180/PI * parseFloat(string[0]), -180/PI * parseFloat(string[1])]).addTo(map);
            }
            marker_list.push(marker);
        }
    }

    for (j = 0; j < x.length; j++) {
        marker_list[j].bindPopup(x[j].innerHTML.split()[0]).openPopup();
    }
}

window.onload = (event) => {
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

    var fairports = document.getElementsByClassName("fuel-airports");
    var dairports = document.getElementsByClassName("dist-airports");
    MarkerFunction(fairports, map, 'green');
    MarkerFunction(dairports, map, 'blue');
}

