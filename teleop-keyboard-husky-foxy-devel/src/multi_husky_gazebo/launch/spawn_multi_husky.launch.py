from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

from pathlib import Path

ARGUMENTS = [
    #Get values from multi_husky_playpen.launch
    DeclareLaunchArgument('robot_name', default_value='h0'),
    DeclareLaunchArgument('tfpre', default_value='h0'),
    DeclareLaunchArgument('x', default_value='0.0'),
    DeclareLaunchArgument('y', default_value='0.0'),
    DeclareLaunchArgument('z', default_value='0.0'),
    DeclareLaunchArgument('yaw', default_value='0.0'),
    DeclareLaunchArgument('controller_space', default_value='/h0/controller_manager'),
    DeclareLaunchArgument('joint_broad', default_value='/h0/joint_state_broadcaster'),
    DeclareLaunchArgument('husk_controller', default_value='/h0/husky_velocity_controller'),
    DeclareLaunchArgument('control_path', default_value= 'control_h0.yaml')
]


def generate_launch_description():

    robot_name = LaunchConfiguration('robot_name')
    tfpre = LaunchConfiguration('tfpre')
    X = LaunchConfiguration('x')
    Y = LaunchConfiguration('y')
    Yaw = LaunchConfiguration('yaw')
    Z = LaunchConfiguration('z')
    prefix = LaunchConfiguration('prefix')
    controller_space = LaunchConfiguration('controller_space')
    joint_broad = LaunchConfiguration('joint_broad')
    husk_controller = LaunchConfiguration('husk_controller')
    control_path = LaunchConfiguration('control_path')



    config_husky_velocity_controller = PathJoinSubstitution(
        [FindPackageShare("husky_control"), "config", 'control.yaml']
    )

    # Get URDF via xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("husky_description"), "urdf", "husky.urdf.xacro"]
            ),
            " ",
            "name:=",
            robot_name,
            " ",
            "prefix:=",
            tfpre,
            " ",
            "is_sim:=true",
            " ",
            "gazebo_controllers:=",
            config_husky_velocity_controller,
        ]
    )
    robot_description = {"robot_description": robot_description_content}

    spawn_husky_velocity_controller = Node(
        package='controller_manager',
        namespace=tfpre,
        executable='spawner.py',
        arguments=[husk_controller, '-c', controller_space],
        output='screen',
    )



    node_robot_state_publisher = Node(
        package="robot_state_publisher",
        namespace=tfpre,
        executable="robot_state_publisher",
        output="screen",
        parameters=[{'use_sim_time': True}, robot_description],
    )

   
    spawn_joint_state_broadcaster = Node(
        package='controller_manager',
        namespace=tfpre,
        executable='spawner.py',
        arguments=[joint_broad, '-c', controller_space],
        output='screen',
    )

    # Make sure spawn_husky_velocity_controller starts after spawn_joint_state_broadcaster
    diffdrive_controller_spawn_callback = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_joint_state_broadcaster,
            on_exit=[spawn_husky_velocity_controller],
        )
    )

    # delayed_spawn_joint_state_broadcaster = TimerAction(
    #     period=0.5,
    #     actions = [
    #         spawn_joint_state_broadcaster,
    #     ]
    # )


    # Spawn robot
    spawn_robot = Node(
        package='gazebo_ros',
        namespace=tfpre,
        executable='spawn_entity.py',
        name=robot_name,
        arguments=['-entity',
                    robot_name,
                   '-topic',
                   'robot_description',
                    '-x',
                    X,
                    '-y',
                    Y,
                    '-z',
                    Z,],
        output='screen',
    )


    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(node_robot_state_publisher)
    ld.add_action(spawn_joint_state_broadcaster)
    ld.add_action(diffdrive_controller_spawn_callback)
    ld.add_action(spawn_robot)

    return ld