from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'final_task_topic'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # 以下两行用于安装launch和config文件夹中的文件，非常重要，否则在安装后无法找到launch和config文件夹中的文件
        (os.path.join('share', package_name,'launch'), glob('launch/*.launch.py')),# 连接launch文件
        (os.path.join('share', package_name,'config'), glob('config/*.yaml')),# 连接config文件
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shang',
    maintainer_email='1426704359@qq.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'main_control_node = final_task_topic.main_control_node:main',
            'chassis_node = final_task_topic.chassis_node:main',
        ],
    },
)
