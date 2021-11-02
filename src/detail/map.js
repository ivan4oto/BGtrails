// import 'mapbox-gl/dist/mapbox-gl.css';
import toGeoJSON from '@mapbox/togeojson';
import mapboxgl from 'mapbox-gl'; // or "const mapboxgl = require('mapbox-gl');"

mapboxgl.accessToken = 'pk.eyJ1IjoiaXZhbjRvdG8iLCJhIjoiY2tlMGVnbzFxM3V6NDJxbXFzZmhmZ29tcyJ9.jbuxXicfoB-ygV96MaT7pQ';




$(function () {
    // mapbox
    map.on('load', () => {
        fetch(objGpxPath)
        .then(response => response.text(), reason => {console.log('First error', reason)})
        .then(data => {
            console.log('We got the Data!')
            var domparser = new DOMParser();
            var myxml = domparser.parseFromString(data, 'text/xml');
            map.resize();
            map.addSource(objName, {
                'type': 'geojson',
                'data': toGeoJSON.gpx(myxml)
                });
            map.addLayer({
                'id': objName,
                'type': 'line',
                'source': objName,
                'layout': {
                    'line-join': 'round',
                    'line-cap': 'round'
                },
                'paint': {
                    'line-color': '#ff0000',
                    'line-width': 3
                }
            });
            map.addControl(new mapboxgl.NavigationControl());
        }, reason => {console.log('Nooo', reason)});
    });
    const marker1 = new mapboxgl.Marker()
    .setLngLat([objLat, objLon])
    .addTo(map);
    
    


})
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/outdoors-v11', // style URL
    center: [objLat, objLon], // starting position [lng, lat]
    zoom: 10 // starting zoom
});


