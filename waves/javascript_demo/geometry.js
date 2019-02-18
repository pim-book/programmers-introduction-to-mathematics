function innerProduct(a, b) {
  return a.x * b.x + a.y * b.y;
}

class Vector {
  constructor(x, y, arrowheadSize = 100) {
    this.x = x;
    this.y = y;
    this.arrowheadSize = arrowheadSize;
  }

  add(other) {
    return new Vector(this.x + other.x, this.y + other.y);
  }

  subtract(other) {
    return new Vector(this.x - other.x, this.y - other.y);
  }

  scale(scalar) {
    return new Vector(this.x * scalar, this.y * scalar);
  }

  toString() {
    let roundedX = Math.round(this.x * 100) / 100;
    let roundedY = Math.round(this.y * 100) / 100;
    return `(${roundedX}, ${roundedY})`;
  }

  arrowheadOffset() {
    let angleFromHorizontal = Math.atan2(this.y, this.x);
    let angleFromVertical = Math.PI / 2 - angleFromHorizontal;
    let angleDeg = parseInt((angleFromVertical * 180) / Math.PI);
    let halfLength = Math.sqrt(this.arrowheadSize) / 2;
    let arrowheadOffsetX = -halfLength * Math.cos(angleFromHorizontal);
    let arrowheadOffsetY = halfLength * Math.sin(angleFromHorizontal);
    return [arrowheadOffsetX, arrowheadOffsetY, angleDeg];
  }

  normalized() {
    let norm = this.norm();
    return new Vector(this.x / norm, this.y / norm);
  }

  norm() {
    return Math.sqrt(this.x * this.x + this.y * this.y);
  }

  project(w) {
    // project this onto the input vector w
    let normalizedW = w.normalized();
    let signedLength = innerProduct(this, normalizedW);

    return new Vector(
      normalizedW.x * signedLength,
      normalizedW.y * signedLength
    );
  }
}

module.exports = {
  Vector,
  innerProduct
};
