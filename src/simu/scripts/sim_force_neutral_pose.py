#!/usr/bin/env python3

import rospy
from franka_core_msgs.msg import JointCommand
from franka_gripper.msg import MoveActionGoal

if __name__ == "__main__":
    
    rospy.init_node("force_neutral_pose_startup")

    pub = rospy.Publisher('panda_simulator/motion_controller/arm/joint_commands',
        JointCommand,
        tcp_nodelay=True,
        queue_size=1)
    pub_gripper = rospy.Publisher('franka_gripper/move/goal',MoveActionGoal,tcp_nodelay=True,queue_size=1)
    ini_pos = rospy.get_param('~initial_pose')
    ini_gripper_width = rospy.get_param('~initial_gripper_width')
    command_msg = JointCommand()
    command_msg.names = ["panda_joint%d" % (idx) for idx in range(1, 8)]
    command_msg.position = ini_pos
    command_msg.mode = JointCommand.POSITION_MODE
    gripper_msg = MoveActionGoal()
    gripper_msg.goal.width = ini_gripper_width

    
    rospy.sleep(0.5)
    start = rospy.Time.now().to_sec()

    rospy.loginfo("Attempting to force robot to neutral pose...")
    rospy.sleep(0.5)
    
    while not rospy.is_shutdown() and (rospy.Time.now().to_sec() - start < 1.):
        # print rospy.Time.now()
        command_msg.header.stamp = rospy.Time.now()
        pub.publish(command_msg)
        pub_gripper.publish(gripper_msg)

    rospy.loginfo("Robot forced to neutral pose. Complete!")
