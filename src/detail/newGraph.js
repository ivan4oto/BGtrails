import Dygraph from "dygraphs";
import "./dygraphs.css";


var cleanPresets = {
  axes: {
    x: {
      drawGrid: false,
      drawAxis: false
    },
    y: {
      drawGrid: false,
      drawAxis: false
    }
  },
  rollPeriod: 7,
  labelsDiv: "",
  highlightCircleSize: 2,
  strokeWidth: 2,
  legend: "none",
  animatedZooms: false,
  colors: ["#61cdbb"]
};

var fullPresets = {
  axes: {
    x: {
      drawGrid: true,
      drawAxis: true,
      axisLineColor: "white",
      axisLineWidth: 1.5
    },
    y: {
      drawAxis: true,
      gridLineWidth: 1.5,
      gridLineColor: "#eee",
      gridLinePattern: [5, 5],
      axisLineColor: "white",
      axisLineWidth: 1
    }
  },
  rollPeriod: 10,
  highlightCircleSize: 5,
  legendFormatter: legendFormatter,
  legend: "follow",
  strokeWidth: 2,
  fillGraph: true,
  colors: ["#61cdbb"],
  visibility: [true],
  animatedZooms: true,
  hideOverlayOnMouseOut: false
};

function legendFormatter(data) {
  if (data.x == null) {
    // This happens when there's no selection and {legend: 'always'} is set.
    return +data.series
      .map(function (series) {
        return series.dashHTML + " " + series.labelHTML;
      })
      .join();
  }

  var html = "<b>" + data.xHTML + "</b>";
  data.series.forEach((series) => {
    if (!series.isVisible) return;

    var labeledData = series.labelHTML + " <b>" + series.yHTML + "</b>";

    if (series.isHighlighted) {
      labeledData = "<b>" + labeledData + "</b>";
    }

    html +=
      "<div class='dygraph-legend-row'>" +
      series.dashHTML +
      "<div>" +
      labeledData +
      "</div></div>";
  });
  return html;
}

$(function() {
    $.ajax({
        type: "GET",
        url: csvPath,
        dataType: "text",
        success: function(data) {
            $(function() {
                var g2 = new Dygraph(
                    document.getElementById("graphdiv2"), data, fullPresets
                  );
            });
        }
     });
});
