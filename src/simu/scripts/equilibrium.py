#! /usr/bin/env python
import rospy
import tf
from tf import transformations
from tf import TransformerROS
import geometry_msgs
from rostopic import get_topic_type
import quaternion
import numpy as np
from geometry_msgs.msg import  PoseStamped, TransformStamped, Transform
import tf2_ros
from franka_core_msgs.msg import EndPointState, JointCommand, RobotState
from simu.msg import obj_target

class EquiliCal():
    
    def __init__(self):
        
        rospy.init_node('equilibrium_pose_publisher')
        rospy.loginfo("This node is to calculate the equilibrium pose of end effektor and publish the pose")
        self.tf_ros_1 = TransformerROS()
        self.config()
        self.equili_pose = PoseStamped()
        self.equili_pub = rospy.Publisher("panda_simulator/equili_pose",PoseStamped,queue_size=1)        
        # init the matrix of target
        self.target_matrix = np.eye(4)
        self.obj_target = rospy.Subscriber("/object_target",obj_target,self.target_state,queue_size=1)
        self.equili_cal_pub()
        rospy.spin()

    def config(self):
        # get the name of base link and leader robot
        self.base_name = rospy.get_param('~base_name')
        self.leader_name = rospy.get_param('~leader_name')
        # trandformation from virtual leader to object frame and from object to end frame
        self.leader_obj = rospy.get_param('~leader_obj')
        self.obj_end = rospy.get_param('~obj_end')
        self.tip_state_compensation = np.matrix([[-0.707,0.707,0,0],[-0.707,-0.707,0,0],[0,0,1,0],[0,0,0,1]])
    
    def target_state(self,msg):
        # set the target
        self.target_ori_matrix = transformations.euler_matrix(msg.roll,msg.pitch,msg.yaw)
        self.target_matrix[:3,:3] = self.target_ori_matrix[:3,:3]
        self.target_matrix[0,3] = msg.x
        self.target_matrix[1,3] = msg.y
        self.target_matrix[2,3] = msg.z

    def equili_cal_pub(self):     
        listener_1 = tf.TransformListener()
        rate = rospy.Rate(10.0)
        while not rospy.is_shutdown():
            
            # if the base is mobile base, you need to change the link name 
            try:
                (trans1,rot1) = listener_1.lookupTransform(self.base_name, self.leader_name, rospy.Time(0))
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue
            self.base_transformation_matrix = self.tf_ros_1.fromTranslationRotation(trans1,rot1)
            self.leader_object_matrix = np.reshape(self.leader_obj,(4,-1))
            self.obj_end_matrix = np.reshape(self.obj_end,(4,-1))
            # calculate the equlibrium pose
            equili_pose_matrix = np.dot(np.dot(np.dot(np.dot(self.base_transformation_matrix,self.leader_object_matrix),self.target_matrix),self.obj_end_matrix),self.tip_state_compensation)
            position = equili_pose_matrix[:3,3]
            orientation = quaternion.from_rotation_matrix(equili_pose_matrix[:3,:3])
            # publish the equilibrium pose
            self.equili_pose.pose.position.x = position[0]
            self.equili_pose.pose.position.y = position[1]
            self.equili_pose.pose.position.z = position[2]
            self.equili_pose.pose.orientation = orientation
            self.equili_pub.publish(self.equili_pose)
            rate.sleep()

        
if __name__ == '__main__':
    EquiliCal()


