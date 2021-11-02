
console.log(client)

client({ accessToken: 'pk.eyJ1IjoiaXZhbjRvdG8iLCJhIjoiY2tlMGVnbzFxM3V6NDJxbXFzZmhmZ29tcyJ9.jbuxXicfoB-ygV96MaT7pQ' });



// var uploadedFile = $('#form-file').prop('files');

// var geojson = tj()
// var tolerance = 0.001

// var geojsonFile, simplified;

// uploadedFile.text().then(value => { parseUploadedFile(value)});

// function parseUploadedFile(value) {
//     geojsonFile = toGeoJSON.gpx(value)
//     simplified = simplify(geojson, tolerance)
// }

// staticClient.getStaticImage({
//     ownerId: 'mapbox',
//     styleId: 'streets-v11',
//     width: 200,
//     height: 300,
//     position: {
//       coordinates: [objLat, objLon],
//       zoom: 3
//     },
//     overlays: [
//       // GeoJson object for overlay
//       {
//         geoJson: {
//           geojsonFile
//         }
//       }
//     ]
//   })
//     .send()
//     .then(response => {
//       const image = response.body;
//       console.log(image)
//     });