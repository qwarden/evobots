import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time


class SOLUTION:
    def __init__(self, myID):
        self.weights = np.random.rand(3, 2) * 2 - 1
        self.myID = myID

    def Start_Simulation(self, directOrGUI, background=True):
        self.Create_Brain()

        os.system(f"python3 simulate.py {directOrGUI} {self.myID} 2&>1 {'&' if background else ''}")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = f"fitness/fitness{self.myID}.txt"

        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        fitnessFile = open(fitnessFileName, "r")
        self.fitness = float(fitnessFile.readline())
        fitnessFile.close()

        # os.system(f"rm {fitnessFileName}")

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brains/brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse(
                        sourceNeuronName=currentRow,
                        targetNeuronName=currentColumn+3,
                        weight=self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, 2)
        randomColumn = random.randint(0, 1)

        self.weights[randomRow][randomColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
        self.myID = ID
