import constants as c

import numpy as np
import pybullet as p
import pyrosim.pyrosim as pyrosim


class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.amplitude = c.amplitude
        self.frequency = c.frequency
        if self.jointName == "Torso_BackLeg":
            self.frequency = c.frequency / 2
        self.offset = c.offset
        self.force = c.maxForce
        self.values = \
            [self.amplitude * np.sin(self.frequency * i + self.offset)
             for i in np.linspace(0, 2*np.pi, c.steps)]

    def Set_Value(self, robot, t):
        pyrosim.Set_Motor_For_Joint(
                bodyIndex=robot.Id,
                jointName=self.jointName,
                controlMode=p.POSITION_CONTROL,
                targetPosition=self.values[t],
                maxForce=self.force)

    def Save_Values(self):
        np.save(f"data/{self.jointName}MotorValues.npy", self.values)
