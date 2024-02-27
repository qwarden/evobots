from sensor import SENSOR
from motor import MOTOR

import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os


class ROBOT:
    def __init__(self, solutionID):
        self.Id = p.loadURDF("body.urdf")
        self.solutionID = solutionID

        pyrosim.Prepare_To_Simulate(self.Id)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK(f"brains/brain{solutionID}.nndf")
        # os.system(f"rm brain{solutionID}.nndf")

    def Prepare_To_Sense(self):
        self.sensors = {}

        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.Get_Value(t)

    def Prepare_To_Act(self):
        self.motors = {}

        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self, desiredAngle)

    def Think(self):
        self.nn.Update()

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.Id, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]

        f = open(f"fitness/tmp{self.solutionID}.txt", "w")
        f.write(f"{xCoordinateOfLinkZero}")
        f.close()

        os.system(f"mv fitness/tmp{self.solutionID}.txt fitness/fitness{self.solutionID}.txt")
