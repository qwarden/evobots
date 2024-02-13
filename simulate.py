import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
from time import sleep

STEPS = 5000

backLegAmplitude = -np.pi/4
backLegFrequency = 20
backLegPhaseOffset = 0

frontLegAmplitude = -np.pi/6
frontLegFrequency = 20
frontLegPhaseOffset = -np.pi/3

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = np.zeros(STEPS)
frontLegSensorValues = np.zeros(STEPS)

backLegTargetAngles = \
    [backLegAmplitude * np.sin(backLegFrequency * i + backLegPhaseOffset)
     for i in np.linspace(0, 2*np.pi, STEPS)]
frontLegTargetAngles = \
    [frontLegAmplitude * np.sin(frontLegFrequency * i + frontLegPhaseOffset)
     for i in np.linspace(0, 2*np.pi, STEPS)]

# np.save("data/backLegTargetAngles.npy", backLegTargetAngles)
# np.save("data/frontLegTargetAngles.npy", frontLegTargetAngles)

for i in range(STEPS):
    p.stepSimulation()

    backLegSensorValues[i] = \
        pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = \
        pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    pyrosim.Set_Motor_For_Joint(
            bodyIndex=robotId,
            jointName="Torso_BackLeg",
            controlMode=p.POSITION_CONTROL,
            targetPosition=backLegTargetAngles[i],
            maxForce=20)
    pyrosim.Set_Motor_For_Joint(
            bodyIndex=robotId,
            jointName="Torso_FrontLeg",
            controlMode=p.POSITION_CONTROL,
            targetPosition=frontLegTargetAngles[i],
            maxForce=20)

    sleep(1/3000)

np.save("data/backLegSensorValues.npy", backLegSensorValues)
np.save("data/frontLegSensorValues.npy", frontLegSensorValues)
p.disconnect()
