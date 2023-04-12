int xCoordsIndex = 0;
vision::signature colors[2] = {BLUEY, REDY};
int xCoords[8] = {158, 158, 158, 158, 158, 158, 158, 158};
void redLight() {
  FL.setBrake(brake);
  FR.setBrake(brake);
  ML.setBrake(brake);
  MR.setBrake(brake);
  RL.setBrake(brake);
  RR.setBrake(brake);
}
void greenLight() {
  FL.setBrake(coast);
  FR.setBrake(coast);
  ML.setBrake(coast);
  MR.setBrake(coast);
  RL.setBrake(coast);
  RR.setBrake(coast);
}
void Brake() {
  redLight();
  greenLight();
}
void visionAim(const int visionCenter = 158, const int OKError = 15) {
  double x;

  FL.setVelocity(100, pct);
  FR.setVelocity(100, pct);
  RL.setVelocity(100, pct);
  RR.setVelocity(100, pct);

  Vision.takeSnapshot(REDY);
  while (Vision.largestObject.exists && Controller1.ButtonX.pressing()) {
    Vision.takeSnapshot(REDY);
    x = Vision.largestObject.centerX; // Gets center x value of object
    if (x < (visionCenter - OKError)) {
      FR.spin(fwd);
      RR.spin(fwd);
      FL.spin(vex::reverse);
      RL.spin(vex::reverse);
    }
    Brake();
    if (x > (visionCenter + OKError)) {
      FR.spin(vex::reverse);
      RR.spin(vex::reverse);
      FL.spin(fwd);
      RL.spin(fwd);
    }
    Brake();
  }
}
void visionPID(const int xCoord) {
  double kp = 0.18, err, pidout;

  err = 158 - xCoord;
  pidout = (err * DEGREES_TO_PIXELS) * kp;

  FL.spinFor(vex::reverse, pidout, deg, false);
  ML.spinFor(vex::reverse, pidout, deg, false);
  RL.spinFor(vex::reverse, pidout, deg, false);
  FR.spinFor(fwd, pidout, deg, false);
  MR.spinFor(fwd, pidout, deg, false);
  RR.spinFor(fwd, pidout, deg);

  Brake();
}

int getAverage(const int (*list)[8]) {
  int sum = 0;
  for (int i : (*list)) { sum += i; }
  return sum / 8;
}
void GetVisionCoords() {
  for (vision::signature item : colors) {
    Vision.takeSnapshot(item);
    xCoords[xCoordsIndex % 8] = Vision.largestObject.exists ? 
                                Vision.largestObject.centerX : 158;
    xCoordsIndex++;
  }
}
