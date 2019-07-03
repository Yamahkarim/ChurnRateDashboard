console.log("Hello World");


// Plot the default route once the page loads
/*var defaultURL = "/emoji_char";
d3.json(defaultURL).then(function(data) {
  var data = [data];
  var layout = { margin: { t: 30, b: 100 } };
  Plotly.plot("bar", data, layout);
});*/

//var defaultURL = "/emoji_char";

var defaultURL = "/default";
d3.json(defaultURL).then(function(data) {
  console.log("[JavaScript] Json Data")
  console.log(data)
  var dates = data.x;
  var counts = data.y;

  console.log(dates)
  console.log(counts)

  var data = [data];
  var layout = { margin: { t: 30, b:100 } };
  Plotly.plot("bar", data, layout)
});




// Update Bar Chart
function updatePlotly(newdata) {
  Plotly.restyle("bar", "x", [newdata.x]);
  Plotly.restyle("bar", "y", [newdata.y]);
}

// Extract Drop Down Data From HTML
function getData(route) {
  console.log(route);
  d3.json(`/${route}`).then(function(data) {
    console.log("newdata", data);
    updatePlotly(data);
  });
}

