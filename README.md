# humanoid-prep

Working repository for a 20-week self-directed preparation programme, ahead of an R&D
robotics role focused on humanoid platforms for industrial use.

## Why this exists

The target role involves researching humanoid robot applications on the AgiBot G2
platform and implementing them for industrial use cases, using NVIDIA Omniverse,
Isaac Sim, Isaac Lab, and Genie Sim.

My background is mechanical and structural design, with working FEA knowledge. The gap
is software: Python, ROS 2, and the simulation stack. This repository is where I close
it — in public, with everything committed as I go, rather than as private notes that
prove nothing.

## Scope

| Weeks | Focus |
|---    |---    |
| 1     | Git and GitHub |
| 2–3   | Python: core language, then the class-and-callback shape ROS 2 uses |
| 4–9   | ROS 2 Jazzy — nodes, TF, URDF, RViz, Gazebo, MoveIt 2, ros2_control |
| 10–11 | NumPy and robot kinematics; payload envelope tool |
| 12–13 | OpenUSD and Isaac Sim |
| 14–15 | Reference test cell design and its digital twin |
| 16–17 | Genie Sim on the AgiBot G2 |
| 20    | Use-case dossier for a beverage and packaging line |

## Layout

- `logs/` — weekly write-ups. What I built, what I learned, what broke and how I fixed it.
- `setup/` — machine setup runbooks. Written after doing each setup once, so the next
  machine takes minutes instead of hours.

## Principles

**Build, don't study.** 
Every phase produces something that lands here.

**Rebuild from scratch.** 
After each course section, close the course and rebuild the
result with my own names. Slower, and it's the difference between recognising code and being able to write it.

**Mechanical depth is the point.** 
The scarce profile isn't another ML engineer — it's
someone who can look at a demo and say *this won't hold at 1.5 kg at full extension, here's the torque maths, and here's what the test cell needs to look like.* The software
here is in service of that, not a replacement for it.