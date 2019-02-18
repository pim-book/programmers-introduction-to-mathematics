import * as d3 from "d3";
import { System } from "./springs";

let width = 1000;
let height = 600;
let svg = d3
  .select("body")
  .insert("svg", ":first-child")
  .attr("width", width)
  .attr("height", height);

let originX = width / 2;
let originY = height / 2;

let arrowheadSize = 40;
let vectorColor = "#333";
let vectorStroke = 2;

let stringColor = "#ccc";
let stringWidth = 1;

let beadRadius = 10;
let beadColor = "#ccc";
let beadStroke = 2;
let beadStrokeColor = "#333";

function fromCartesianX(x) {
  return originX + x;
}
function fromCartesianY(y) {
  return originY - y;
}

function createVectorsSVG(beads) {
  let vectorContainers = svg
    .selectAll(".forces")
    .data(beads)
    .enter()
    .append("g");
  let vectors = vectorContainers
    .append("line")
    .attr("x1", function(d) {
      return fromCartesianX(d.position.x);
    })
    .attr("y1", function(d) {
      return fromCartesianY(d.position.y);
    })
    .attr("x2", function(d) {
      return fromCartesianX(d.displayForce().x);
    })
    .attr("y2", function(d) {
      return fromCartesianY(d.displayForce().y);
    });

  let triangleSymbol = d3
    .symbol()
    .size(arrowheadSize)
    .type(d3.symbolTriangle);
  let arrowheads = vectorContainers
    .append("g")
    .append("path")
    .attr("d", triangleSymbol);

  arrowheads.attr("transform", function(d) {
    let offset = d.acceleration.arrowheadOffset();
    let displayForce = d.displayForce();
    let displayX = fromCartesianX(displayForce.x) + offset[0];
    let displayY = fromCartesianY(displayForce.y) + offset[1];
    let rotationFromVertical = offset[2];
    return (
      "translate(" +
      displayX +
      " " +
      displayY +
      ") " +
      "rotate(" +
      rotationFromVertical +
      ")"
    );
  });
  return { vectors: vectors, arrowheads: arrowheads };
}

function vectorsStyle(vectorSVG) {
  vectorSVG.vectors
    .attr("stroke", vectorColor)
    .attr("stroke-width", vectorStroke);

  vectorSVG.arrowheads.style("fill", vectorColor);
}

function createStringsSVG(beads) {
  let beadPairs = [];
  for (let i = 0; i < beads.length - 1; i++) {
    beadPairs.push([beads[i], beads[i + 1]]);
  }

  let stringContainers = svg
    .selectAll(".string")
    .data(beadPairs)
    .enter()
    .append("g");
  let strings = stringContainers.append("line");
  strings
    .attr("x1", function(d) {
      return fromCartesianX(d[0].position.x);
    })
    .attr("y1", function(d) {
      return fromCartesianY(d[0].position.y);
    })
    .attr("x2", function(d) {
      return fromCartesianX(d[1].position.x);
    })
    .attr("y2", function(d) {
      return fromCartesianY(d[1].position.y);
    });

  return strings;
}

function stringsStyle(stringsSVG) {
  stringsSVG.attr("stroke", stringColor).attr("stroke-width", stringWidth);
}

function createBeadsSVG(beads) {
  let circleContainers = svg
    .selectAll(".point")
    .data(beads)
    .enter()
    .append("g");
  let circles = circleContainers.append("circle");
  circles
    .attr("cx", function(d) {
      return fromCartesianX(d.position.x);
    })
    .attr("cy", function(d) {
      return fromCartesianY(d.position.y);
    })
    .attr("r", beadRadius)
    .attr("id", function(d) {
      return d.id;
    });

  return circles;
}

function beadsStyle(beadsSVG) {
  beadsSVG
    .attr("fill", beadColor)
    .attr("stroke", beadStrokeColor)
    .attr("stroke-width", beadStroke);
  return beadsSVG;
}

function createSystemSVG(system) {
  let beadsSVG = createBeadsSVG(system.beads);
  beadsStyle(beadsSVG);

  let vectorsSVG = createVectorsSVG(system.beads);
  vectorsStyle(vectorsSVG);

  let stringsSVG = createStringsSVG(system.beads);
  stringsStyle(stringsSVG);

  return { beads: beadsSVG, forces: vectorsSVG, strings: stringsSVG };
}

function updatePositions(systemSVG) {
  let { beads, forces, strings } = systemSVG;

  beads
    .attr("cx", function(d) {
      return fromCartesianX(d.position.x);
    })
    .attr("cy", function(d) {
      return fromCartesianY(d.position.y);
    });

  forces.vectors
    .attr("x1", function(d) {
      return fromCartesianX(d.position.x);
    })
    .attr("y1", function(d) {
      return fromCartesianY(d.position.y);
    })
    .attr("x2", function(d) {
      return fromCartesianX(d.displayForce().x);
    })
    .attr("y2", function(d) {
      return fromCartesianY(d.displayForce().y);
    });

  strings
    .attr("x1", function(d) {
      return fromCartesianX(d[0].position.x);
    })
    .attr("y1", function(d) {
      return fromCartesianY(d[0].position.y);
    })
    .attr("x2", function(d) {
      return fromCartesianX(d[1].position.x);
    })
    .attr("y2", function(d) {
      return fromCartesianY(d[1].position.y);
    });

  forces.arrowheads.attr("transform", function(d) {
    let offset = d.acceleration.arrowheadOffset();
    let displayForce = d.displayForce();
    let displayX = fromCartesianX(displayForce.x) + offset[0];
    let displayY = fromCartesianY(displayForce.y) + offset[1];
    let rotationFromVertical = offset[2];
    return (
      "translate(" +
      displayX +
      " " +
      displayY +
      ") " +
      "rotate(" +
      rotationFromVertical +
      ")"
    );
  });
}

function resetPositions(displacements) {
  for (let i = 0; i < displacements.length; i++) {
    system.beads[i + 1].position.y = displacements[i];
    system.beads[i + 1].velocity.x = 0;
    system.beads[i + 1].velocity.y = 0;
    system.beads[i + 1].acceleration.x = 0;
    system.beads[i + 1].acceleration.y = 0;
  }

  if (timer) {
    window.clearInterval(timer);
  }
  timer = window.setInterval(function() {
    system.simulateStep();
    updatePositions(systemSVG);
  }, 1000 / 40);
}

function resetPositionsButton() {
  let inputNodes = d3.selectAll("input").nodes();
  let displacements = [];
  for (let node of inputNodes) {
    displacements.push(parseInt(node.value));
  }
  resetPositions(displacements);
}

function resetInputs(values) {
  let inputNodes = d3.selectAll("input").nodes();
  for (let i = 0; i < values.length; i++) {
    inputNodes[i].value = values[i];
  }
  resetPositions(values);
}

var system = new System(width, 5);
var timer = null; // timer that controls system evolution
var systemSVG = createSystemSVG(system);
var initialDisplacements = [0, 50, 0, 0, 0];

var eigs = [
  [29, 50, 58, 50, 29],
  [-50, -50, 0, 50, 50],
  [58, 0, -58, 0, 58],
  [-50, 50, 0, -50, 50],
  [-29, 50, -58, 50, -29]
];

function initialize() {
  d3.select("#reset_positions").on("click", resetPositionsButton);
  d3.select("#eig1").on("click", () => resetInputs(eigs[0]));
  d3.select("#eig2").on("click", () => resetInputs(eigs[1]));
  d3.select("#eig3").on("click", () => resetInputs(eigs[2]));
  d3.select("#eig4").on("click", () => resetInputs(eigs[3]));
  d3.select("#eig5").on("click", () => resetInputs(eigs[4]));
  resetPositions(initialDisplacements);
}

window.d3 = d3;
window.onload = initialize;
