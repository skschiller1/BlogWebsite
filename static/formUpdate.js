
function formUpdate() {
    var a = document.getElementById("id_aircraft").value;
    document.getElementById("id_cruise").value = planes[a][0];
    document.getElementById("id_fuel_burn").value = planes[a][1];
    document.getElementById("id_fuel_capacity").value = planes[a][2];
    document.getElementById("id_fuel_type").value = planes[a][3];

    return 0;
}

// get value of aircraft field
var mySelect = document.getElementById("id_aircraft");

// create a callable dictionary
var piperCub = [75, 5.5, 12.0, "100ll"];
var cessna172 = [122, 8.0, 43.0, "100ll"];
var piperPA28 = [120, 10.0, 36.0, "100ll"];
var cirrusSR20 = [155, 11.0, 60.0, "100ll"];
var cessna182 = [150, 14.0, 92.0, "100ll"];
var beechBonanza = [169, 15.0, 74.0, "100ll"];
var beechBaron = [202, 30.0, 194.0, "100ll"];
var airbusA320 = [453, 777.6, 7061.0, "jeta"];
var gulfstreamG650 = [516, 409.0, 6429.0, "jeta"];

var planes = [];
planes.push(piperCub, cessna172, piperPA28, cirrusSR20, cessna182, beechBonanza, beechBaron, airbusA320, gulfstreamG650);

window.onload = formUpdate();

mySelect.addEventListener("change", formUpdate);