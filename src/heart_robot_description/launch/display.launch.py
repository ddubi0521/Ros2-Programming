import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    package_name = "heart_robot_description"

    # 패키지 경로
    pkg_path = get_package_share_directory(package_name)

    # URDF 경로
    urdf_file = "heart_robot.urdf.xacro"
    robot_desc_path = os.path.join(pkg_path, "urdf", urdf_file)

    # RViz config 경로
    rviz_config_path = os.path.join(pkg_path, "rviz", "heart_robot.rviz")

    # robot_description
    robot_description = {
        "robot_description": Command(["xacro ", robot_desc_path])
    }

    return LaunchDescription([

        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            name="joint_state_publisher_gui"
        ),

        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            parameters=[robot_description]
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["-d", rviz_config_path],  # 변경
            output="screen"
        )
    ])