import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)
        timer_period = 0.1 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()        
        msg.name=['shoulder_pan_joint','shoulder_lift_joint','elbow_joint','wrist_1_joint','wrist_2_joint','wrist_3_joint']
        msg.position=[-1.9564861129902873,-2.7513469288007624,-2.7513469288007624,-2.7513469288007624,1.988810796106495,-1.557829068023615]
        msg.velocity=[]
        msg.effort=[]
        self.publisher_.publish(msg)
        self.get_logger().info('I heard: "%s"' % msg)

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

#I heard: "sensor_msgs.msg.JointState(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1742491112, nanosec=990390848), frame_id=''), name=['robotiq_85_right_knuckle_joint', 'robotiq_85_left_inner_knuckle_joint', 'robotiq_85_right_inner_knuckle_joint', 'robotiq_85_left_finger_tip_joint', 'robotiq_85_right_finger_tip_joint', 'joint_1', 'robotiq_85_left_knuckle_joint', 'joint_2', 'joint_4', 'joint_5', 'joint_3', 'joint_6', 'joint_7'], position=[-0.7929, 0.7929, -0.7929, -0.7929, 0.7929, 0.0, 0.7929, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], velocity=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], effort=[nan, nan, nan, nan, nan, 0.0, nan, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])"
#I heard: "sensor_msgs.msg.JointState(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=0, nanosec=0), frame_id=''), name=['robotiq_85_right_knuckle_joint', 'robotiq_85_left_inner_knuckle_joint', 'robotiq_85_right_inner_knuckle_joint', 'robotiq_85_left_finger_tip_joint', 'robotiq_85_right_finger_tip_joint', 'joint_1', 'robotiq_85_left_knuckle_joint', 'joint_2', 'joint_4', 'joint_5', 'joint_3', 'joint_6', 'joint_7'], position=[-0.7929, 0.7929, -0.7929, -0.7929, 0.7929, 0.0, 0.7929, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], velocity=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], effort=[nan, nan, nan, nan, nan, 0.0, nan, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])"