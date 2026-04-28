from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PythonExpression


def generate_launch_description():
    # 1. Set robot description (xacro)
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("heart_robot_description"), "urdf", "heart_robot.urdf.xacro"]
            ),
        ]
    )
    robot_description = {
        "robot_description": robot_description_content
    }

    # 2. Set controller yaml path
    controller_yaml = PathJoinSubstitution(
        [FindPackageShare("heart_robot_description"), "config", "controller.yaml"]
    )

    # 3. Include Gazebo launch file
    gazebo_launch_file = PathJoinSubstitution(
        [FindPackageShare("gazebo_ros"), "launch", "gazebo.launch.py"]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments={
        "gui": "true",
        "extra_gazebo_args": PythonExpression(["'--ros-args --params-file ' + '", controller_yaml, "'"])
    }.items()
    )

    # 4. Robot state publisher
    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[robot_description, {"use_sim_time": True}]
    )

    # 5. Spawn robot into Gazebo
    spawn = TimerAction(
        period=3.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    "ros2", "run", "gazebo_ros", "spawn_entity.py",
                    "-entity", "heart_robot",
                    "-topic", "robot_description",
                    "-z", "0.28"
                ],
                output="screen"
            )
        ]
    )

    # 7. Load controllers
    joint_state_broadcaster = ExecuteProcess(
        cmd=[
            "ros2", "control", "load_controller",
            "--set-state", "active",
            "joint_state_broadcaster"
        ],
        output="screen"
    )

    arm_controller = ExecuteProcess(
        cmd=[
            "ros2", "control", "load_controller",
            "--set-state", "active",
            "arm_controller"
        ],
        output="screen"
    )

    load_controllers = TimerAction(
        period=10.0,
        actions=[
            joint_state_broadcaster,
            arm_controller
        ]
    )

    # 8. Return all nodes/actions
    nodes = [
        rsp,
        gazebo,
        spawn,
        load_controllers
    ]

    return LaunchDescription(nodes)