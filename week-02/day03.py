def to_radians(degrees):
    return degrees*3.14159/180

def is_within_limits(degrees, limit=90.0):
    return abs(degrees) <= limit

#result = is_within_limits(30)
#print(result)

joints = {"shoulder":-40.00, "elbow":32.30, "wrist":-15.01, "hip":-120.00, "knee":-25.02, "ankle":1.23}

joints_in_radians = {name:to_radians(degrees) for name, degrees in joints.items()}
#print(joints_in_radians)


# now check the angles in the 'joints' against the function 'is_within_limits' & print the one which is false

#joints_fail_withinlimits = {name:degrees for name, degrees in joints.items() if is_within_limits(degrees) == False}
#name_out_of_limit_joints = [name for name, degrees in joints_fail_withinlimits.items()]
#print([name for name, degrees in joints_fail_withinlimits.items()])

#print([name for name, degrees in joints.items() if not is_within_limits(degrees)])

for name, angles_inradians in joints_in_radians.items():
    print(f"{name:<12}{angles_inradians:>7.3f} rad")

print(f"Out of limits: {[name for name, degrees in joints.items() if not is_within_limits(degrees)]}")

print(f"Default limit (90): {is_within_limits(-40.0)}")
print(f"Tighter limit (30): {is_within_limits(-40.0, 30.0)}")