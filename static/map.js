function MarkerFunction(x) {
    for (i = 0; i < x.length; i++) {
        if (window.getComputedStyle(x[i]).display === "none") {
            var string = x[i].innerHTML.split(",");
            let marker = L.marker([180/PI * parseFloat(string[0]), -180/PI * parseFloat(string[1])]).addTo(map);
            list_of_markers.push(marker);
        }
    }

    for (j = 0; j < x.length; j++) {
        list_of_markers[j].bindPopup(x[j].innerHTML.split()[0]).openPopup();
    }
    alert("Finished binding popups");
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

    const PI = Math.PI;
    var airports = document.getElementsByClassName("fuel-airports");
    MarkerFunction(airports)
}

