#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib

kLEDBuffer = 60


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.arduino = wpilib.SerialPort(9600, wpilib.SerialPort.Port.kUSB1)
        # PWM Port 9
        # Must be a PWM header, not MXP or DIO
        self.led = wpilib.AddressableLED(9)

        # LED Data
        self.ledData = [wpilib.AddressableLED.LEDData() for _ in range(kLEDBuffer)]

        # Store what the last hue of the first pixel is
        self.rainbowFirstPixelHue = 0

        # Default to a length of 60, start empty output
        # Length is expensive to set, so only set it once, then just update data
        self.led.setLength(kLEDBuffer)

        # Set the data
        self.led.setData(self.ledData)
        self.led.start()

        self.signature_timer = wpilib.Timer()
        self.signature_timer.start()

    def robotPeriodic(self):
        #Set Leds
        self.led.setData(self.ledData)

        #Check for incoming data from arduino
        if self.arduino.getBytesReceived() > 0:
            #Store Data in arduinoData variable
            arduinoData = self.readString(self.arduino)
            #If arduino sends "Y" turn LEDs green and restart timer
            if arduinoData == "Y": 
             for i in range(len(self.ledData)):
                 self.ledData[i].setRGB(64, 255, 0)
                 self.signature_timer.restart()
            #If arduino sends "N" and timer has elasped .15 seconds (for visual protection) turn LEDs red
            if self.signature_timer.hasElapsed(.15) and arduinoData == "N":
                for i in range(len(self.ledData)):
                    self.ledData[i].setRGB(255, 0, 0)
        #set LEDs again
        self.led.setData(self.ledData)
         
        
        
    def readString(self, port) -> str:
        # Function to read a string from the serial port
        sz = port.getBytesReceived()
        buf = bytearray(sz)
        sz = port.read(buf)
        return buf[:sz].decode("ascii")

    
    # def rainbow(self):
    #     # For every pixel
    #     for i in range(kLEDBuffer):
    #         # Calculate the hue - hue is easier for rainbows because the color
    #         # shape is a circle so only one value needs to precess
    #         hue = (self.rainbowFirstPixelHue + (i * 180 / kLEDBuffer)) % 180

    #         # Set the value
    #         self.ledData[i].setHSV(int(hue), 255, 128)

    #     # Increase by to make the rainbow "move"
    #     self.rainbowFirstPixelHue += 3

    #     # Check bounds
    #     self.rainbowFirstPixelHue %= 180


if __name__ == "__main__":
    wpilib.run(MyRobot)