import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    #获取YAML文件的路径
    config_file_path = os.path.join(get_package_share_directory('final_task_topic'), 'config', 'params.yaml')

    return LaunchDescription([
        # 启动主控制节点，并传入参数
        Node(
            package='final_task_topic',
            executable='main_control_node',
            name='main_control_node',
            output='screen',
            parameters=[config_file_path]  # 传入YAML文件路径
        )
    ])