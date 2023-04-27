#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import math

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
bMotor = Motor(Port.B)


# Write your program here.

# 緩動函數 cos
def easeInOutSine(x):
    return -(math.cos(math.pi * x) - 1) / 2

# 彈跳函數
def easeOutBounce(x):
    n1 = 7.5625
    d1 = 2.75
    
    if x < 1 / d1:
        return n1 * x * x
    elif x < 2 / d1:
        x -= 1.5 / d1
        return n1 * x * x + 0.75
    elif x < 2.5 / d1:
        x -= 2.25 / d1
        return n1 * x * x + 0.9375
    else:
        x -= 2.625 / d1
        return n1 * x * x + 0.984375

# 映射區間
def mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# 緩加減速
def smoothMove(time, distance, minSpeed, maxSpeed):
    i = 0
    step = time / 100 / 2
    target = bMotor.angle() + distance
    while i <= 1:
        t_angle = mapping(easeOutBounce(i), 0, 1, 0, target)
        error = t_angle - bMotor.angle()
        t_speed = error * 1.5
        bMotor.dc(t_speed)
        i += 0.01
        wait(step)
    while bMotor.angle() < target:
        bMotor.dc(20)
    bMotor.stop()
    bMotor.hold()

ev3.speaker.beep()

# 使用範例 在3秒內移動到1000度
smoothMove(6000, 2000, 10, 100)
ev3.screen.print(bMotor.angle())
wait(5000)