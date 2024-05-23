#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        # Right Motors
        self.leftFront = wpilib.Spark(0)
        self.leftRear = wpilib.Spark(2)
        self.leftGroup = wpilib.MotorControllerGroup(self.leftFront, self.leftRear)
        
        # Left Motors
        self.rightFront = wpilib.Spark(1)
        self.rightRear = wpilib.Spark(3)
        self.rightGroup = wpilib.MotorControllerGroup(self.rightFront, self.rightRear)

        # Assemble Drive Train
        self.robotDrive = wpilib.drive.DifferentialDrive(
            self.leftGroup, self.rightGroup
        )
        
        self.timer = wpilib.Timer()

        # We need to invert one side of the drivetrain so that positive voltages
        # result in both sides moving forward. Depending on how your robot's
        # gearbox is constructed, you might have to invert the left side instead.
        self.rightGroup.setInverted(True)
       
       #Initialize Controller
        self.controller = wpilib.XboxController(0)
        

    def autonomousInit(self):
         """This function is run once each time the robot enters autonomous mode."""
         self.timer.restart()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous.

        # Drive for two seconds
        if self.timer.get() < 2.0:
            # Drive forwards half speed, make sure to turn input squaring off
            self.robotDrive.arcadeDrive(0.5, 0, squareInputs=False)
        else:
            self.robotDrive.stopMotor()  # Stop robot
        """

    def teleopInit(self):
        """This function is called once each time the robot enters teleoperated mode."""

    def teleopPeriodic(self):
        """This function is called periodically during teleoperated mode."""
        #Use Y Axis data to control corresponding side of robot
        self.robotDrive.tankDrive(
            -self.controller.getLeftY(), -self.controller.getRightY()
        )


    def testInit(self):
        """This function is called once each time the robot enters test mode."""

    def testPeriodic(self):
        """This function is called periodically during test mode."""


if __name__ == "__main__":
    wpilib.run(MyRobot)