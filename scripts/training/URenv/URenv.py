import gymnasium as gym
import numpy as np
import math
import rclpy
import logging
from gymnasium import error, spaces, utils
from gymnasium.utils import seeding
from rclpy.node import Node
from sensor_msgs.msg import JointState
from threading import Thread

class JointPublisherNode(Node):
    def __init__(self):
        super().__init__('joint_publisher')
        timer_period = 0.1 # seconds
        self.joints_state=[0.0,0.0,0.0,0.0,0.0,0.0]
        self.publisher_=self.create_publisher(JointState, 'joint_states', 10)
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg=JointState()
        msg.header.stamp=self.get_clock().now().to_msg()        
        msg.name=['shoulder_pan_joint',
                  'shoulder_lift_joint',
                  'elbow_joint',
                  'wrist_1_joint',
                  'wrist_2_joint',
                  'wrist_3_joint']
        msg.position=self.joints_state
        msg.velocity=[]
        msg.effort=[]
        self.publisher_.publish(msg)
        #self.get_logger().info('Publish: "%s"' % msg)

    def publish(self,joints_state):
        self.joints_state=joints_state

class URenv(gym.Env):
    def __init__(self):
        # init logger
        self.logger=logging.getLogger(__name__)
        # Set confi variables
        mov_step=3
        self.target_threshold=0.25
        # Set Observation & Action spaces
        self.action_space=spaces.Box(-mov_step, mov_step, [6,], dtype=np.float32) # joints adjust in deegres 
        self.observation_space=spaces.Box(-6.133, 6.133, [6,], dtype=np.float64) # joints state
        # Set Target Pose
        self.target_pose=[-3.188,5.812,-1.760,0.188,2.221,2.922]
        # Init Ros Python 
        rclpy.init(args=None)
        # Start a Publisher Node
        self.joint_publisher=JointPublisherNode()
        # Spin a node in a separate thread
        t1=Thread(target=self.spinNode)
        t1.start()
    def spinNode(self):
        # Spin publisher
        rclpy.spin(self.joint_publisher)

    def step(self, action):
        # Set new position to publish
        j_lim=[
            6.133,
            6.133,
            2.992,
            6.133,
            6.133,
            3.142
        ]
        for i in range(6):
            # set new value for joint
            self.joints_state[i]+=action[i]*math.pi/180
            # seize value within joint limit
            if self.joints_state[i]<-j_lim[i]:
                self.joints_state[i]=-j_lim[i]
            elif self.joints_state[i]>j_lim[i]:
                self.joints_state[i]=j_lim[i]
        # Publish new position
        self.joint_publisher.publish(self.joints_state)
        # Calculate reward
        reward=0
        for i in range(6):
            reward+=math.pow(self.target_pose[i]-self.joints_state[i],2)
        reward=-math.sqrt(reward)
        # Increase step counter
        self.step_counter+=1
        # Check if episode has finished
        terminated=False
        if self.step_counter==1000:
            terminated=True
            #self.logger.info('Episode terminated: "%s"' % reward)
        # Set remaining return variables
        truncated=False
        info={}
        #self.logger.info('Joins State: "%s"' % self.joints_state)
        return np.array(self.joints_state), reward, terminated, truncated, info
    def reset(self,seed=None,options=None):
        # Set inital pose
        self.joints_state=[0.0,0.0,0.0,0.0,0.0,0.0]
        # Publish initial pose
        self.joint_publisher.publish(self.joints_state)
        # reset step counter
        self.step_counter=0
        return np.array(self.joints_state), {}
    def close(self):
        self.joint_publisher.destroy_node()
        rclpy.shutdown()