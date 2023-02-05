#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Font

# Create your objects here.
ev3 = EV3Brick()


# Write your program here.

print("Initializing process...")

# False = Lamp is Off
# True = Lamp is On
lampStatus=False

# False = Remote control is disabled
# True = Remote control is enabled
remoteControl=True
remoteChannel=2

# Initialize motors
PowerSwitchMotor=Motor(Port.D)

# Initialize sensors
infraredSensor = InfraredSensor(Port.S4)

# Initialize color
ev3.light.on(Color.RED)

print("Initialization complete ✅")
print("Remote control : " + str(remoteControl))
if remoteControl == True:
    print("Remote channel : " + str(remoteChannel))
print("")
print("Lamp Usage:")
print("Press the center button to turn on/off the lamp.")
print("Press the up button to enable/disable remote control.")
if remoteControl == True:
    print("")
    print("Remote Control Usage:")
    print("Press the beacon button on the remote control to turn on the lamp.")
    print("If remote control is enabled, the lamp will turn off automatically when the beacon button is released.")
    print("If remote control is enabled, the center button will be disabled.")

def offLamp():
    PowerSwitchMotor.run_angle(250, -360)
    PowerSwitchMotor.stop()
    return;

def onLamp():
    PowerSwitchMotor.run_angle(250, 360)
    PowerSwitchMotor.stop()
    return;

def drawScreen (remote, Lamp):
    ev3.screen.clear()
    ev3.screen.set_font(Font(size=20))
    ev3.screen.print("Remote control:", "On" if remote == True else "Off")
    if remote == True:
        ev3.screen.print("Remote channel : ", str(remoteChannel))
    ev3.screen.print("Lamp : ", "On" if Lamp == True else "Off")
    return;

drawScreen(remoteControl, lampStatus)
while True:
    if Button.CENTER in ev3.buttons.pressed() and remoteControl == False:
        if lampStatus == True:
            offLamp()
            lampStatus=False
            ev3.light.on(Color.RED)
            drawScreen(remoteControl, lampStatus)
        elif lampStatus == False:
            onLamp()
            lampStatus=True
            ev3.light.on(Color.GREEN)
            drawScreen(remoteControl, lampStatus)
    if Button.UP in ev3.buttons.pressed():
        if remoteControl == True:
            remoteControl=False
            drawScreen(remoteControl, lampStatus)
        elif remoteControl == False:
            remoteControl=True
            drawScreen(remoteControl, lampStatus)
    if remoteControl == True and Button.BEACON in infraredSensor.buttons(remoteChannel) and lampStatus == False:
        onLamp()
        lampStatus=True
        ev3.light.on(Color.GREEN)
        drawScreen(remoteControl, lampStatus)
    elif remoteControl == True and Button.BEACON not in infraredSensor.buttons(remoteChannel) and lampStatus == True:
        offLamp()
        lampStatus=False
        ev3.light.on(Color.RED)
        drawScreen(remoteControl, lampStatus)