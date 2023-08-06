window.addEventListener("scroll", function() {
    var scrolltotop = document.scrollingElement.scrollTop;
    var target = document.getElementById("body");
    var factor = 0.95;
    var xvalue = "center";
    var yvalue = scrolltotop * factor;
    target.style.backgroundPosition = xvalue + " " + yvalue + "px";
});
