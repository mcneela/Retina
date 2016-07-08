Plotly.d3.csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv', function(err, rows){
var mainPlot = document.getElementById('mainPlot');
var YEAR = 2007;
var continents = ['Asia', 'Europe', 'Africa', 'Oceania', 'Americas'];
var POP_TO_PX_SIZE = 2e5;
var myLayer = new Layer('beans');
function unpack(rows, key) {
  return rows.map(function(row) { return row[key]; });
}

var data = continents.map(function(continent) {
  var rowsFiltered = rows.filter(function(row) {
      return (row.continent === continent) && (+row.year === YEAR);
  });
  return {
      mode: 'markers',
      name: continent,
      x: unpack(rowsFiltered, 'lifeExp'),
      y: unpack(rowsFiltered, 'gdpPercap'),
      text: unpack(rowsFiltered, 'country'),
      marker: {
          sizemode: 'area',
          size: unpack(rowsFiltered, 'pop'),
          sizeref: POP_TO_PX_SIZE
      }
  };
});
var layout = {
  xaxis: {title: 'Life Expectancy'},
  yaxis: {title: 'GDP per Capita', type: 'log'},
  margin: {t: 20},
  hovermode: 'closest'
};
myLayer.add_trace(data);
Plotly.plot(mainPlot, data, layout, {showLink: false});
debugger
});

