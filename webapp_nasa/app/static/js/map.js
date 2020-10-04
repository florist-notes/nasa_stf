// Yosemite National Park
let startlat = 37.865101;
let startlon = -119.538330;

let options = {
    center: [startlat, startlon],
    zoom: 10
}

document.getElementById('lat').value = startlat;
document.getElementById('lon').value = startlon;

let map = L.map('map', options);
let nzoom = 14;

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: 'OSM'}).addTo(map);

let myMarker = L.marker([startlat, startlon], {
    title: "Coordinates",
    alt: "Coordinates",
    draggable: true
}).addTo(map).on('dragend', function () {
    let lat = myMarker.getLatLng().lat.toFixed(8);
    let lon = myMarker.getLatLng().lng.toFixed(8);
    let czoom = map.getZoom();
    if (czoom < 18) {
        nzoom = czoom + 2;
    }
    if (nzoom > 18) {
        nzoom = 18;
    }
    if (czoom !== 18) {
        map.setView([lat, lon], nzoom);
    } else {
        map.setView([lat, lon]);
    }
    document.getElementById('lat').value = lat;
    document.getElementById('lon').value = lon;
    myMarker.bindPopup("Lat " + lat + "<br />Lon " + lon).openPopup();
});


function chooseAddr(lat1, lng1) {
    myMarker.closePopup();
    map.setView([lat1, lng1], 18);
    myMarker.setLatLng([lat1, lng1]);
    let lat = lat1.toFixed(8);
    let lon = lng1.toFixed(8);
    document.getElementById('lat').value = lat;
    document.getElementById('lon').value = lon;
    myMarker.bindPopup("Lat " + lat + "<br />Lon " + lon).openPopup();
}


function myFunction(arr) {
    let out = "<br />";
    let i;

    if (arr.length > 0) {
        for (i = 0; i < arr.length; i++) {
            out +=
                "<div class='address' " +
                "title='Show Location and Coordinates' " +
                "onclick='chooseAddr(" + arr[i].lat + ", " + arr[i].lon + "); return false;'" +
                ">" + arr[i].display_name + "</div>";
        }
        document.getElementById('results').innerHTML = out;
    } else {
        document.getElementById('results').innerHTML = "Sorry, no results...";
    }

}

function addr_search() {
    let inp = document.getElementById("addr");
    let xmlhttp = new XMLHttpRequest();
    let url = "https://nominatim.openstreetmap.org/search?format=json&limit=3&q=" + inp.value;
    xmlhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            let myArr = JSON.parse(this.responseText);
            myFunction(myArr);
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}



const backend_url_base = 'http://165.232.120.34:8000'

function get_color(score) {
    const percentage = (score - 30) / 70 * 100

	let r, g, b = 0;
	if (percentage < 50) {
		r = 255;
		g = Math.round(5.1 * percentage);
	}
	else {
		g = 255;
		r = Math.round(510 - 5.10 * percentage);
	}
	const h = r * 0x10000 + g * 0x100 + b * 0x1;
	return '#' + ('000000' + h.toString(16)).slice(-6);
}

let tiles_polygons = []
function draw_tile(lat, lon, tile) {
    let layer_removed = (!tiles_polygons.length);
    console.log(layer_removed)
    for (let tile_polygon of tiles_polygons) {
        const old_tile = tile_polygon[0]
        if (!(lat >= old_tile.lower_left.x && lat <= old_tile.upper_right.x &&
                lon >= old_tile.lower_left.y && lon <= old_tile.upper_right.y)) {
            layer_removed = true
            map.removeLayer(tile_polygon[1])
        }
    }

    if (layer_removed) {
        const latlngs = [
            [tile.lower_left.x, tile.lower_left.y],
            [tile.lower_left.x, tile.upper_right.y],
            [tile.upper_right.x, tile.upper_right.y],
            [tile.upper_right.x, tile.lower_left.y],
        ];
        const polygon = L.polygon(latlngs, {color: get_color(tile.score)}).addTo(map)
        tiles_polygons = [[tile, polygon]]
    }
}

function onMapClick(e) {
    const lat = e.latlng.lat;
    const lon = e.latlng.lng;

    fetch(`${backend_url_base}/point/${lat}/${lon}/predict`)
        .then(response => response.json().then(tiles => {
            for (let tile of tiles)
                draw_tile(lat, lon, tile)
        }))
}

map.on('click', onMapClick)
