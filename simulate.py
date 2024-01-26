import pybullet as p
from time import sleep

physicsClient = p.connect(p.GUI)

p.loadSDF("box.sdf")

for i in range(1000):
    p.stepSimulation()
    sleep(1/200)
    print(i)

p.disconnect()
