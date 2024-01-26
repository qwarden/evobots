import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

x = 0

for _ in range(5):
    y = 0
    for _ in range(5):
        z = 0.5
        size = [1, 1, 1]
        for _ in range(10):
            pyrosim.Send_Cube(name="Box", pos=[x, y, z],
                              size=size)
            z += 1
            size = [i * 0.9 for i in size]
        y += 1
    x += 1

pyrosim.End()
