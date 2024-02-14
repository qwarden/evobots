from world import WORLD
from robot import ROBOT
import constants as c

import pybullet as p
import pybullet_data
from time import sleep


class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)

        self.world = WORLD()
        self.robot = ROBOT()

    def __del__(self):
        p.disconnect()

    def Run(self):
        for t in range(c.steps):
            p.stepSimulation()

            self.robot.Sense(t)
            self.robot.Act(t)

            sleep(c.sleep)
