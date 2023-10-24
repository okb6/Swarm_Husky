import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
import time

class Communication(Node):
    def __init__(self):
        super().__init__('communication')
        self.pub1 = self.create_publisher(Twist, 'h1_husky_velocity_controller/cmd_vel_unstamped', 10)
        self.pub2 = self.create_publisher(Twist, 'h2_husky_velocity_controller/cmd_vel_unstamped', 10)
        self.pub3 = self.create_publisher(Twist, 'h3_husky_velocity_controller/cmd_vel_unstamped', 10)
        self.pub4 = self.create_publisher(Twist, 'h4_husky_velocity_controller/cmd_vel_unstamped', 10)
        self.pub5 = self.create_publisher(Twist, 'h5_husky_velocity_controller/cmd_vel_unstamped', 10)
        self.pub6 = self.create_publisher(Twist, 'h6_husky_velocity_controller/cmd_vel_unstamped', 10)
        self.pub7 = self.create_publisher(Twist, 'h7_husky_velocity_controller/cmd_vel_unstamped', 10)
        self.pub8 = self.create_publisher(Twist, 'h8_husky_velocity_controller/cmd_vel_unstamped', 10)
        self.sub = self.create_subscription(Twist, 'h0_husky_velocity_controller/cmd_vel_unstamped',  self.communication_callback, 10)
        
        self.sub #prevent unused vairable warning

    def communication_callback(self, msg):
        linear_x = msg.linear.x
        linear_y = msg.linear.y 
        linear_z = msg.linear.z 
        angular_x = msg.angular.x
        angular_y = msg.angular.y 
        angular_z = msg.angular.z

        twist_msg = Twist()

        # if not linear_x == 0:
        #     print("Received Commands")

        # elif not linear_y == 0:
        #     print("Received Commands")

        # elif not linear_z == 0:
        #     print("Received Commands")
        
        # elif not angular_x == 0:
        #     print("Received Commands")
        
        # elif not angular_y == 0:
        #     print("Received Commands")
        
        # elif not angular_z == 0:
        #     print("Received Commands")
        
        twist_msg.linear.x = linear_x
        twist_msg.linear.y = linear_y
        twist_msg.linear.z = linear_z
        twist_msg.angular.x = angular_x
        twist_msg.angular.y = angular_y
        twist_msg.angular.z = -angular_z

        # time.sleep(2)
        

        self.pub1.publish(twist_msg)
        self.pub2.publish(twist_msg)
        self.pub3.publish(twist_msg)
        self.pub4.publish(twist_msg)
        self.pub5.publish(twist_msg)
        self.pub6.publish(twist_msg)
        self.pub7.publish(twist_msg)
        self.pub8.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)

    communication = Communication()

    rclpy.spin(communication)

    rclpy.shutdown()

if __name__ == '__main__':
    main()

        


