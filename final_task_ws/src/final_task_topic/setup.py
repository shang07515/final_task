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
