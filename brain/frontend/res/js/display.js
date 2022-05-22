var colors = {"done":"green","hinted_done":"lightgreen","lock":"grey","todo":"orange","hinted_todo":"yellow"}


var width = 560,
    height = 560,
    radius = 12;

var svg = d3.select("#d3js-tree").append("svg")
    .attr("width", width)
    .attr("height", height);

var link = svg.selectAll(".link"),
    node = svg.selectAll(".node");

svg.append('defs').append('marker')
    .attr('id', 'arrowhead')
    .attr('viewBox', '-0 -5 10 10')
    .attr('refX', 20)
    .attr('refY', 0)
    .attr('orient', 'auto')
    .attr('markerWidth', 5)
    .attr('markerHeight', 5)
    .attr('xoverflow', 'visible')
    .append('svg:path')
    .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
    .style('stroke','none');

var force = d3.layout.force()
    .size([width, height])
    .charge(-400)
    .linkDistance(40)
    .on("tick", tick);

var drag = force.drag()
    .on("dragstart", dragstart);

d3.json("http://127.0.0.1:8080/tasks/graph", function (error, graph) {
    if (error) throw error;
    update(graph.links, graph.nodes);
})

function update(links, nodes) {

    force
        .nodes(nodes)
        .links(links)
        .start();

    link = link
        .data(links)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr('marker-end','url(#arrowhead)')

    node = node
        .data(nodes)
        .enter()
        .append("circle")
        .attr("class", "node")
        .attr("r", radius)
        .call(drag)
        .style("fill", function (d, i) {return colors[d.status];})

}

function tick() {
    link
        .attr("x1", function (d) {return d.source.x;})
        .attr("y1", function (d) {return d.source.y;})
        .attr("x2", function (d) {return d.target.x;})
        .attr("y2", function (d) {return d.target.y;});

    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
}
  
  function dragstart(d) {   
    let response = fetch("http://127.0.0.1:8080/task/" + d.id);

    fetch("http://127.0.0.1:8080/task/" + d.id)
        .then( r => r.json())
        .then( json => {
            console.log(json)
            document.getElementById("taskTitle").innerHTML = "" + d.id + "-" +  json[0]
            document.getElementById("taskDesc").innerHTML = json[1]
            document.getElementById("taskValidate").onclick = function(){getvalidate( d.id )}
            document.getElementById("taskHint").onclick = function(){getclue( d.id )}
        })
  }

  function getclue(id) {
    fetch("http://127.0.0.1:8080/task/" + id + "/clue")
    .then( r => r.json())
    .then( txt => {
        console.log("clue", txt, id)
        document.getElementById("taskHintValue").innerHTML = txt

        updatecolor()
    })
  }
  function getvalidate(id) {
    fetch("http://127.0.0.1:8080/task/" + id + "/verify")
    .then( r => r.json())
    .then( txt => {
        console.log("validate", txt, id)
        document.getElementById("taskValidateValue").innerHTML = txt[1]
        if (txt[0] == true)
            document.getElementById("taskValidateValue").style = 'color:green'
        else
            document.getElementById("taskValidateValue").style = 'color:red'

        updatecolor()
    })
  }


function updatecolor(){
    fetch("http://127.0.0.1:8080/tasks/graph")
    .then( r => r.json())
    .then( json => {
        
        node.style("fill", function (d, i) {return colors[json.nodes.filter(n => n.id == d.id)[0].status];})
    })
}