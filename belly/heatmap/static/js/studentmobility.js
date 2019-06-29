
var myMap = L.map("map", {
  center: [21.428209,-157.805603],
  zoom: 13
});

L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);
  
   //var url = "https://data.sfgov.org/resource/cuks-n6tp.json?$limit=1000";
var url = "https://a.uguu.se/ubdutAkgN1Jy_final_fixed.json"; // parsa added this


//parsa added these below
d3.json(url,function(response) {

  console.log(response);

  var heatArray = [];

  for (var i = 0; i < response.length; i++) {
    var res = response[i];
    
    
    if (location) {
      heatArray.push([res.lat,res.lon]);
    }
  }

  var heat = L.heatLayer(heatArray, {
    radius: 20,
    blur: 35
  }).addTo(myMap);

});

  