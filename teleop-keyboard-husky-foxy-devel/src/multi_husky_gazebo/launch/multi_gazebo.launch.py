from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node




def generate_launch_description():
    
    world_file = PathJoinSubstitution(
        [FindPackageShare("husky_gazebo"),
        "worlds",
        "clearpath_playpen.world"],
    )

    multi_launch = PathJoinSubstitution(
        [FindPackageShare("multi_husky_gazebo"),
        "launch",
        "multi_husky_playpen.launch.py"],
    )

    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([multi_launch]),
        launch_arguments={'world_path': world_file}.items(),
    )

    # teleop_twist_keyboard_node = Node(
    #     package="teleop_twist_keyboard",
    #     executable="teleop_twist_keyboard",
    #     output="screen"
    # )

    ld = LaunchDescription()
    ld.add_action(gazebo_sim)
    # ld.add_action(teleop_twist_keyboard_node)

    return ld
