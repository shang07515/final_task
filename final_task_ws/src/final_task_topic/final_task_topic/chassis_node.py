import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class ChassisNode(Node):
    def __init__(self):
        super().__init__('chassis_node')
        self.subscription_ = self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 10)
        self.get_logger().info('底盘节点已启动，等待接收速度指令...')

    def cmd_vel_callback(self, msg):
        # 接收主控制节点发来的速度指令
        vx = min(msg.linear.x, 2.0) # 限制线速度在2.0 m/s以内
        vy = min(msg.linear.y, 2.0) # 限制线速度在2.0 m/s以内

        # 执行停止操作
        if vx == 0.0 and vy == 0.0:
            self.get_logger().info('接收到停止指令，底盘停止运动。')
        #else:
            #self.get_logger().info(f'接收到速度指令: vx={vx:.2f} m/s, vy={vy:.2f} m/s')
            # 在这里可以添加底盘运动控制的代码，例如调用底盘驱动接口

def main(args=None):
    rclpy.init(args=args)
    chassis_node = ChassisNode()
    rclpy.spin(chassis_node)
    chassis_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()