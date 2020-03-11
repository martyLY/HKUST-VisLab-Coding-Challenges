/*var tooltip = d3.select("body")
.append("div")
.attr("class", "tooltip")
.style("visibility", "hidden")
.text("a simple tooltip");
*/
//console.log(filter);
var data = filter;

data.links.forEach(link => {
  var i = 0;
  data.nodes.forEach(node => {
    if (link.source == node.id) {
      link.source = i;
    }
    i++;
  })    
  var j = 0;
  data.nodes.forEach(node => {
    if (link.target == node.id) {
      link.target = j;
    }
    j++;
  })
  //console.log(link.source, link.target);
})
//console.log(data)

  //SVG的尺寸
var width = 600,    height = 600;

//定义力布局
var force = d3.layout.force()
    .size([width, height])
    .linkStrength(0.2)
    .linkDistance(100)
    .charge(-150)
    //.gravity();


//绘制一个svg
var force_svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

var n = data.nodes.length;
data.nodes.forEach(function(d, i) {
  d.x = d.y =10+ width / n* i;
});

//加载数据，启动力布局
force.nodes(data.nodes)
     .links(data.links)
     .start();
     
//绘制连接线
var link = force_svg.selectAll(".link")
    .data(data.links)
  .enter().append("line")
    .attr("stroke", "#ccc")
    .attr("stroke-width", 0.5);

//绘制节点
var node = force_svg.selectAll(".node")
    .data(data.nodes)
  .enter().append("circle")
    .attr("fill", function(d,i){ return color(i);})
    .attr("r", function(d) {
      return 5+d.weight/2;
    })
  .attr("stroke","white")
  .attr("stroke-width",1)
  .style("opacity", 0.8)
  .on("mouseover", function(d) {
    d3.select(this).style("opacity", 1).attr("stroke", "black");
  })
  .on("mouseout", function() {
    d3.select(this).style("opacity", 0.8).attr("stroke", "white");
  })
  .on("click", function(d,p) {
    console.log(p);
    node.each(function(d) {
      d3.select(this).style("opacity", 0.8).attr("stroke", "white");
    })
    d3.select(this).style("opacity", 1).attr("stroke", "black");

    d3.selectAll(".row text").classed("active", function(d, i) { return i == p; });
    d3.selectAll(".column text").classed("active", function(d, i) { return i == p; });
    d3.selectAll(".row")
      .each(function(d, i) {
        if (i == p) {
          d3.select(this).selectAll("rect").style("fill", "red")//.style("stroke-opacity", 1);
        } else {
          d3.select(this).selectAll("rect")
          .each(function(d) {
            if (d.x == p) {
              d3.select(this).style("fill", "red")
            } else {
              d3.select(this).style("fill", "black")
            }
          })
          
          //d3.selectAll("circle").style("fill", "black")
        }
      })
  });

//按照力布局的节拍移动线和点的位置，直到收敛
force.on("tick", function() {
  link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  node.attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; });
});
//})