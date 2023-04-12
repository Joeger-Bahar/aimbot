# Library imports
from vex import *

def redLight() {
  FL.setBrake(brake);
  FR.setBrake(brake);
  ML.setBrake(brake);
  MR.setBrake(brake);
  RL.setBrake(brake);
  RR.setBrake(brake);
}
def greenLight() {
  FL.setBrake(coast);
  FR.setBrake(coast);
  ML.setBrake(coast);
  MR.setBrake(coast);
  RL.setBrake(coast);
  RR.setBrake(coast);
}

def Brake() {
  redLight();
  greenLight();
}
DEGREES_TO_PIXELS = 5.2666

"""Complicated aim bot"""

colors = [REDY, BLUEY]
xCoords = [158, 158, 158, 158, 158, 158, 158, 158]
xCoordsIndex = 0

def visionPID(xCoord):
  kp = 0.18, err, pidout

  err = 158 - xCoord;
  pidout = (err * DEGREES_TO_PIXELS) * kp

  FL.spinFor(reverse, pidout, deg, false)
  ML.spinFor(reverse, pidout, deg, false)
  RL.spinFor(reverse, pidout, deg, false)
  FR.spinFor(fwd, pidout, deg, false)
  MR.spinFor(fwd, pidout, deg, false)
  RR.spinFor(fwd, pidout, deg)

  Brake()

# Gets an average from a list of numbers
def getAverage(list):
  sum = 0
  for i in list:
      sum += i
  return sum / len(sum)

void GetVisionCoords() {
  for item in colors:
    Vision.takeSnapshot(item)
    if Vision.largestObject.exists:
        xCoords[xCoordsIndex % 8] = Vision.largestObject.centerX
    else:
        xCoords[xCoordsIndex % 8] = 158
    xCoordsIndex += 1

def aimbot():
  for i in range(3):
    visionPID(getAverage(xCoords))
    for i in range(8):
      GetVisionCoords()
    wait(10, msec)

"""End of complicated aimbot"""

"""Simple aimbot"""

def visionAim() {
  OKError = 15
  visionCenter = 158
  x = visionCenter

  FL.setVelocity(100, pct)
  FR.setVelocity(100, pct)
  RL.setVelocity(100, pct)
  RR.setVelocity(100, pct)

  Vision.takeSnapshot(REDY)
  while Vision.largestObject.exists and Controller1.ButtonX.pressing():
    Vision.takeSnapshot(REDY)
    x = Vision.largestObject.centerX
    if x < (visionCenter - OKError):
      FR.spin(fwd)
      RR.spin(fwd)
      FL.spin(reverse)
      RL.spin(reverse)
    Brake()
    if x > (visionCenter + OKError):
      FR.spin(reverse)
      RR.spin(reverse)
      FL.spin(fwd)
      RL.spin(fwd)
    Brake()
