
import Dygraph from 'dygraphs';

$(function() {
    var g2 = new Dygraph(
        document.getElementById("graphdiv2"),
        csvPath, // path to CSV file
        {}          // options
      );
});
