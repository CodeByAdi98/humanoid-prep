joints = {"shoulder":-40.00, "elbow":32.30, "wrist":-15.01, "hip":10.23, "knee":-25.02, "ankle":1.23}
arm_joints = {"shoulder", "elbow", "wrist"}
position = (1.23, -2.54, 1.26)

for joint in joints:
    if joint in arm_joints:
        print(f"{joint:<12}{joints[joint]:>7.2f}  arm")
    else:
        print(f"{joint:<12}{joints[joint]:>7.2f}  -")

x, y, z = position
print(f"position: ({x:.2f}, {y:.2f}, {z:.2f})")