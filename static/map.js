function MarkerFunction(x, y, map, color) {
    if ( x.length < 1 ) return 0;

    // create a green icon
    var myIcon = L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 40],
        iconAnchor: [13, 41],
        popupAnchor: [0, -34],
        shadowSize: [45, 53],
        shadowAnchor: [12, 54]
    });

    // add markers to an array and also add to map
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

    for (j = 0; j < y.length; j++) {
        marker_list[j].bindPopup(y[j].innerHTML).openPopup();
    }

    return 1;
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
    map.setView([38.6280, -96.3344], 3);

    var fairports = document.getElementsByClassName("fuel-airports");
    var fairports_data = document.getElementsByClassName("fuel-airports-data");
    var dairports = document.getElementsByClassName("dist-airports");
    var dairports_data = document.getElementsByClassName("dist-airports-data");
    let test_val = MarkerFunction(fairports, fairports_data, map, 'green');
    let _ = MarkerFunction(dairports, dairports_data, map, 'blue');

    if ( test_val === 0 ) document.getElementById("fuel-data").style.display='none';
    else if ( test_val === 1 ) document.getElementById("fuel-data").style.display='visible';

}

