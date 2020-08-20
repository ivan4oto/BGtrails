const lat = document.querySelector('#lat').getAttribute("href")
const lon = document.querySelector('#lon').getAttribute("href")


console.log(lat)
console.log(lon)

var mymap = L.map('mapid').setView([lat, lon], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
maxZoom: 17,
id: 'mapbox/outdoors-v11',
tileSize: 512,
zoomOffset: -1,
accessToken: 'pk.eyJ1IjoiaXZhbjRvdG8iLCJhIjoiY2tlMGVnbzFxM3V6NDJxbXFzZmhmZ29tcyJ9.jbuxXicfoB-ygV96MaT7pQ'
}).addTo(mymap);

const gpxfile = document.querySelector('#thegpx').getAttribute("href")

new L.GPX(gpxfile, {async: true}).on('loaded', function(e) {
map.fitBounds(e.target.getBounds());
}).addTo(mymap);
