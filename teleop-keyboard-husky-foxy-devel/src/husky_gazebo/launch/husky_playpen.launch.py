# from launch import LaunchDescription
# from launch.actions import IncludeLaunchDescription, GroupAction, DeclareLaunchArgument, SetEnvironmentVariable, ExecuteProcess
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
# from launch.substitutions import Command, EnvironmentVariable, FindExecutable, LaunchConfiguration, PathJoinSubstitution
# from launch_ros.substitutions import FindPackageShare
# from launch_ros.actions import Node, PushRosNamespace
# from ament_index_python.packages import get_package_share_directory

# from pathlib import Path

# ARGUMENTS = [
#     DeclareLaunchArgument('world_path', default_value='',
#                           description='The world path, by default is empty.world'),
# ]

# def generate_launch_description():
    
#     #add namespace for second machine/robot
#     husky_2_ns = LaunchConfiguration('husky_2_ns')
#     husky_2_ns_launch_arg = DeclareLaunchArgument(
#         'husky_2_ns',
#         default_value='husky_2'
#     )
    
#     world_file = PathJoinSubstitution(
#         [FindPackageShare("husky_gazebo"),
#         "worlds",
#         "clearpath_playpen.world"],
#     )

#     gazebo_launch = PathJoinSubstitution(
#         [FindPackageShare("husky_gazebo"),
#         "launch",
#         "gazebo.launch.py"],
#     )

#     gazebo_sim = GroupAction(
#         actions=[
#             PushRosNamespace(husky_2_ns),
#             IncludeLaunchDescription(
#                 PythonLaunchDescriptionSource([gazebo_launch]),
#                 launch_arguments={'world_path': world_file}.items(),
#             ),
#         ]
#     )
    
#     gz_resource_path = SetEnvironmentVariable(name='GAZEBO_MODEL_PATH', value=[
#                                                 EnvironmentVariable('GAZEBO_MODEL_PATH',
#                                                                     default_value=''),
#                                                 '/usr/share/gazebo-11/models/:',
#                                                 str(Path(get_package_share_directory('husky_description')).
#                                                     parent.resolve())])
   
#     # world_path = LaunchConfiguration('world_path')
#     # Gazebo server
#     gzserver = ExecuteProcess(
#         cmd=['gzserver',
#              '-s', 'libgazebo_ros_init.so',
#              '-s', 'libgazebo_ros_factory.so',
#              world_file],
#         output='screen',
#     )

#     # Gazebo client
#     gzclient = ExecuteProcess(
#         cmd=['gzclient'],
#         output='screen',
#         # condition=IfCondition(LaunchConfiguration('gui')),
#     )

#     # teleop_twist_keyboard_node = Node(
#     #     package="teleop_twist_keyboard",
#     #     executable="teleop_twist_keyboard",
#     #     output="screen"
#     # )

#     ld = LaunchDescription(ARGUMENTS)
#     ld.add_action(husky_2_ns_launch_arg)
#     ld.add_action(gazebo_sim)
#     # ld.add_action(teleop_twist_keyboard_node)
#     ld.add_action(gzserver)
#     ld.add_action(gz_resource_path)
#     ld.add_action(gzclient)
#     return ld


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

    gazebo_launch = PathJoinSubstitution(
        [FindPackageShare("husky_gazebo"),
        "launch",
        "gazebo.launch.py"],
    )

    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([gazebo_launch]),
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
