#!/bin/bash

source /opt/ros/humble/setup.bash

cd /app

colcon build

source install/setup.bash

exec ros2 launch final_task_topic final_task.launch.py