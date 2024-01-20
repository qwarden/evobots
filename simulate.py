import pybullet as p
from time import sleep

physicsClient = p.connect(p.GUI)

for i in range(1000):
    p.stepSimulation()
    sleep(1/200)
    print(i)

p.disconnect()
