# 1. Installation
### Clone package
```
cd ~
git clone https://github.com/Grossbier/simulation_multirobots.git
```
### Install dependencies
The dependencies can be installed as following link:
https://github.com/justagist/panda_simulator#readme #(The Franka ROS Interface, franka_panda_description, orocos-kinematics-dynamics have been installed in the package.)

### Build packages
```
cd ~/simulation_multirobots
catkin build
```

## 2. Usage
1.The simulation of multi manipulators in gazebo can be started by:
```
roslaunch simu multi_panda.launch
```
2.Then start the impedance control for the four robots by:
```
roslaunch simu multi_demo_task_control.launch
```
3.In the package there is a object(rectcirc2) for grasping and add it to the path in Gazebo.

4.We could grasp the object by publishing the following topic:
```
rostopic pub /panda1/franka_gripper/grasp/goal
```
5.Send a target for the object by using following command:
```
rostopic pub /object_target
```
6.The parameters for impedance control can be adjusted in the file "task_space_control.py".

For some other topcis and usages in the simulation of franka emika manipulators we could find in:
https://github.com/justagist/panda_simulator#readme
