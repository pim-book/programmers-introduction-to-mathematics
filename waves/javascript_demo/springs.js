import { Vector } from "./geometry";

let displayScaling = 1;

class Bead {
  constructor(x, y, id, mass = 20) {
    this.id = id;
    this.mass = mass;
    this.position = new Vector(x, y);
    this.velocity = new Vector(0, 0);
    this.acceleration = new Vector(0, 0);
    this.force = new Vector(0, 0);
  }

  displayForce() {
    return this.position.add(this.force.scale(displayScaling));
  }

  simulateStep() {
    this.acceleration = this.force.scale(1.0 / this.mass);
    this.velocity = this.velocity.add(this.acceleration);
    this.position = this.position.add(this.velocity);
    // try just updating the vertical component of position
    // this.position = this.position.add(new Vector(0, this.velocity.y));
  }

  toString() {
    return `${this.id}: (p: ${this.position}, v: ${this.velocity}, a: ${
      this.acceleration
    })`;
  }
}

class SpringForce {
  constructor(bead1, bead2, equilibriumLength, springConstant = 1) {
    let displacementVector = bead2.position.subtract(bead1.position);
    this.distance = displacementVector.norm();
    this.forceMagnitude =
      springConstant * Math.max(0, this.distance - equilibriumLength);
    this.forceOnBead1 = displacementVector
      .normalized()
      .scale(this.forceMagnitude);
    this.forceOnBead2 = displacementVector
      .normalized()
      .scale(-this.forceMagnitude);
  }
}

class System {
  // Coordinate system has (0,0) in the center.
  constructor(width, numBeads = 10, equilibriumLength = 5) {
    this.beads = [];
    this.distanceBetween = 150;
    this.equilibriumLength = equilibriumLength;
    let leftEndpoint = [-width / 2 + 25, 0];
    // add two extra "special" beads for the two ends of the string
    for (let i = 0; i < numBeads + 2; i++) {
      this.beads.push(
        new Bead(
          leftEndpoint[0] + i * this.distanceBetween,
          leftEndpoint[1],
          "bead" + i
        )
      );
    }
  }

  updateForces() {
    this.forces = {}; // dictionary index -> [force]
    for (let i = 0; i < this.beads.length - 1; i++) {
      if (i == 0) {
        this.forces[i] = [];
      }
      this.forces[i + 1] = [];

      let jointForce = new SpringForce(
        this.beads[i],
        this.beads[i + 1],
        this.equilibriumLength
      );

      this.forces[i].push(jointForce.forceOnBead1);
      this.forces[i + 1].push(jointForce.forceOnBead2);
    }

    for (let i = 1; i < this.beads.length - 1; i++) {
      let finalForce = new Vector(0, 0);
      for (let force of this.forces[i]) {
        finalForce = finalForce.add(force);
      }
      this.beads[i].force = finalForce;
    }
  }

  updateBeads() {
    // Don't update endpoints
    for (let i = 1; i < this.beads.length - 1; i++) {
      this.beads[i].simulateStep();
    }
  }

  simulateStep() {
    this.updateForces();
    this.updateBeads();
  }
}

module.exports = {
  System
};
