import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math
import time

class MainControlNode(Node):
    def __init__(self):
        super().__init__('main_control_node')

        # 设置启动参数
        self.declare_parameter('start_point',1)
        self.declare_parameter('end_point',1)

        start_point = int(self.get_parameter('start_point').value)
        end_point = int(self.get_parameter('end_point').value)

        # 路径点坐标
        self.path_points = {
            1: (0.0, 0.0),
            2: (2.0, 0.0),
            3: (4.0, 1.0),
            4: (4.0, 3.0),
            5: (2.0, 4.0),
            6: (0.0, 4.0),
            7: (-1.0, 2.0),
            8: (-1.0, 1.0)
        }

        # 规定机器人必须沿规定环形路经顺序运动
        #1 -> 4 -> 7 -> 2 -> 5 -> 8 -> 3 -> 6 -> 1
        self.path_sequence = [1, 4, 7, 2, 5, 8, 3, 6]

        # 构建路径点序列
        start_index = self.path_sequence.index(start_point)
        end_index = self.path_sequence.index(end_point)

        if start_index == end_index:
            # 环路巡检
            self.path_to_follow = self.path_sequence[start_index:] + self.path_sequence[:start_index+1]# 从指定点出发，环形路径运动一圈回到起点
            self.get_logger().info(f'环路巡检模式: 从点 {start_point} 出发，沿路径 {self.path_to_follow} 运动一圈回到起点')
        else:
            # 指定起点与终点
            if end_index > start_index:
                self.path_to_follow = self.path_sequence[start_index:end_index + 1]
            else:
                self.path_to_follow = self.path_sequence[start_index:] + self.path_sequence[:end_index + 1]
            self.get_logger().info(f'指定路径模式: 从点 {start_point} 出发，沿路径 {self.path_to_follow} 到达点 {end_point}')

        # 机器人当前位置和时间初始化
        self.current_x, self.current_y = self.path_points[start_point]# 初始化为起点坐标
        self.last_time = time.time()# 初始化时间

        # 发布速度指令
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.05, self.timer_callback)# 控制频率20Hz

    def stop_robot(self):
        # 停止机器人运动
        stop_msg = Twist()
        stop_msg.linear.x = 0.0
        stop_msg.angular.z = 0.0
        self.publisher_.publish(stop_msg)

    def timer_callback(self):
        # 检查是否结束
        if not self.path_to_follow:
            self.stop_robot()
            self.get_logger().info("已到达终点,机器人停止运动")
            self.get_logger().info(f"最终位置: ({self.current_x:.2f}, {self.current_y:.2f})")

            self.destroy_timer(self.timer)# 关键点！消除定时器，防止继续调用回调函数

            rclpy.shutdown()# 关闭ROS2节点

            return

        now = time.time()
        dt = now - self.last_time# 时间间隔
        self.last_time = now

        target_index = self.path_to_follow[0]# 目标点索引
        target_x, target_y = self.path_points[target_index]# 目标点坐标

        dx = target_x - self.current_x
        dy = target_y - self.current_y
        distance = math.sqrt(dx**2 + dy**2)

        # 判断距离
        if distance < 0.1:  # 如果距离小于0.1米，则认为已到达目标点
            self.path_to_follow.pop(0)  # 移除已到达的点
            return

        # 计算速度指令
        speed = 1.0  # 设定线速度为1.0 m/s
        vx = speed * (dx / distance)  # 线速度在x方向的分量
        vy = speed * (dy / distance)  # 线速度在y方向的分量

        # 发布速度指令
        twist_msg = Twist()
        twist_msg.linear.x = vx
        twist_msg.linear.y = vy
        self.publisher_.publish(twist_msg)

        # 更新当前位置
        self.current_x += vx * dt
        self.current_y += vy * dt

        # 打印当前位置信息
        self.get_logger().info(f"当前位置信息: ({self.current_x:.2f}, {self.current_y:.2f}), 目标点: ({target_x:.2f}, {target_y:.2f}), 距离: {distance:.2f} m")

def main(args=None):
    rclpy.init(args=args)
    node = MainControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()