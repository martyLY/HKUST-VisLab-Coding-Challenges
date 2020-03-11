//定义颜色比例尺
var color=d3.scale.category20c();

var matrix_data = filter;

var margin = {top: 80, right: 0, bottom: 10, left: 80},
    matrix_width = 500,
    matrix_height = 500;

var x = d3.scale.ordinal().rangeBands([0, matrix_width]),
    z = d3.scale.linear().domain([0, 4]).clamp(true),
    c = d3.scale.category10().domain(d3.range(10));

var matrix_svg = d3.select("body").append("svg")
    .attr("width", matrix_width + margin.left + margin.right)
    .attr("height", matrix_height + margin.top + margin.bottom)
    .style("margin-left", "20px")
  .append("g")
    .attr("transform", "translate(80,80)");

matrix_data.links.forEach(link => {
  var i = 0;
  matrix_data.nodes.forEach(node => {
    if (link.source == node.id) {
      link.source = i;
    }
    i++;
  })    
  var j = 0;
  matrix_data.nodes.forEach(node => {
    if (link.target == node.id) {
      link.target = j;
    }
    j++;
  })
  //console.log(link.source, link.target);
})

  var matrix = [],
      nodes = matrix_data.nodes,
      n = nodes.length;

  // Compute index per node.
  nodes.forEach(function(node, i) {
    node.index = i;
    node.count = 0;
    matrix[i] = d3.range(n).map(function(j) { return {x: j, y: i, z: 0}; });
  });

//console.log("links",matrix_data.links)
  // Convert links to matrix; count character occurrences.
  matrix_data.links.forEach(function(link) {
    matrix[link.source][link.target].z += 1;
    matrix[link.target][link.source].z += 1;
    matrix[link.source][link.source].z += 1;
    matrix[link.target][link.target].z += 1;
    nodes[link.source].count += 1;
    nodes[link.target].count += 1;
  });

  // Precompute the orders.
  var orders = {
    name: d3.range(n).sort(function(a, b) { return d3.ascending(nodes[a].dept, nodes[b].dept); }),
    count: d3.range(n).sort(function(a, b) { return nodes[b].count - nodes[a].count; }),
    //group: d3.range(n).sort(function(a, b) { return nodes[b].group - nodes[a].group; })
  };

  // The default sort order.
  x.domain(orders.name);

  matrix_svg.append("rect")
      .attr("class", "background")
      .attr("width", matrix_width)
      .attr("height", matrix_height);

  var row = matrix_svg.selectAll(".row")
      .data(matrix)
    .enter().append("g")
      .attr("class", "row")
      .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
      .each(row);

  row.append("line")
      .attr("x2", matrix_width)
      .style("stroke", "#fff");

  row.append("text")
      .attr("x", -6)
      .attr("y", x.rangeBand() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "end")
      .text(function(d, i) { return nodes[i].itsc; });

  var column = matrix_svg.selectAll(".column")
      .data(matrix)
    .enter().append("g")
      .attr("class", "column")
      .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });

  column.append("line")
      .attr("x1", -matrix_width)
      .style("stroke", "#fff");

  column.append("text")
      .attr("x", 6)
      .attr("y", x.rangeBand() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "start")
      .text(function(d, i) { return nodes[i].itsc; });

  function row(row) {
    var cell = d3.select(this).selectAll(".cell")
        .data(row.filter(function(d) { return d.z; }))
      .enter().append("rect")
        .attr("class", "cell")
        .attr("x", function(d) { return x(d.x); })
        .attr("width", x.rangeBand())
        .attr("height", x.rangeBand())
        .style("fill-opacity", function(d) { return z(d.z); })
        //.style("fill", function(d,i) { return color(i); })
        .on("mouseover", function(p) {
          d3.select(this).style("fill", "red");
          d3.selectAll(".row text").classed("active", function(d, i) { return i == p.y; });
          d3.selectAll(".column text").classed("active", function(d, i) { return i == p.x; });
        })
        .on("mouseout", function() {
          d3.select(this).style("fill", "black");
          d3.selectAll("text").classed("active", false);
        })
        .on("click", function(p) {
          console.log(p.x, p.y);
          d3.selectAll("circle")
            .each(function(d, i) {
              if (i == p.x || i == p.y) {
                d3.select(this).style("opacity", 1).attr("stroke", "red");
              } else {
                d3.select(this).style("opacity", 0.8).attr("stroke", "white");
              }
            })
        });
  }

  function mouseover(p) {
    //d3.selectAll(".row text").classed("active", function(d, i) { return i == p.y; });
    var row = d3.selectAll(".row text")
      .each(function(d, i) {
        if (i == p.y) {
          d3.select(this).style("fill", "blue");
        } else {
          d3.select(this).style("fill", "black")
        }
      })
    d3.selectAll(".column text").classed("active", function(d, i) { return i == p.x; });
  }

  function mouseout() {
    d3.selectAll("text").classed("active", false);
  }

  d3.select("#order").on("change", function() {
    //clearTimeout(timeout);
    order(this.value);
  });

  function order(value) {
    x.domain(orders[value]);

    var t = matrix_svg.transition().duration(2500);

    t.selectAll(".row")
        .delay(function(d, i) { return x(i) * 4; })
        .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
      .selectAll(".cell")
        .delay(function(d) { return x(d.x) * 4; })
        .attr("x", function(d) { return x(d.x); });

    t.selectAll(".column")
        .delay(function(d, i) { return x(i) * 4; })
        .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });
  }

  /*var timeout = setTimeout(function() {
    order("group");
    d3.select("#order").property("selectedIndex", 2).node().focus();
  }, 5000);*/

