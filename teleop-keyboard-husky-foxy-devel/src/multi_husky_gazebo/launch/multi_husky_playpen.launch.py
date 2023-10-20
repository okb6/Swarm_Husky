
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, SetEnvironmentVariable, RegisterEventHandler, TimerAction
from launch.substitutions import EnvironmentVariable, LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
from launch.event_handlers import OnProcessExit
from pathlib import Path

ARGUMENTS = [
    DeclareLaunchArgument('world_path', default_value='',
                          description='The world path, by default is empty.world'),
    
    DeclareLaunchArgument(
        'laser_enabled',
        default_value='false',
        description='sets laser enabled variable'
    ),

    DeclareLaunchArgument(
        'kinect_enabled',
        default_value='false',
        description='sets kinect enabled variable'
    ),

    DeclareLaunchArgument(
        'multimaster',
        default_value='false',
        description='sets multimaster variable'
    ),
]


def generate_launch_description():

    #LAUNCH GAZEBO SERVER/CLIENT

    gz_resource_path = SetEnvironmentVariable(name='GAZEBO_MODEL_PATH', value=[
                                                EnvironmentVariable('GAZEBO_MODEL_PATH',
                                                                    default_value=''),
                                                '/usr/share/gazebo-11/models/:',
                                                str(Path(get_package_share_directory('husky_description')).
                                                    parent.resolve())])

    # Launch args
    world_path = LaunchConfiguration('world_path')
    laser_enabled = LaunchConfiguration('laser_enabled')
    kinect_enabled = LaunchConfiguration('kinect_enabled')
    multimaster = LaunchConfiguration('multimaster')

    # Gazebo server
    gzserver = ExecuteProcess(
        cmd=['gzserver',
             '-s', 'libgazebo_ros_init.so',
             '-s', 'libgazebo_ros_factory.so',
             world_path],
        output='screen',
    )

    # Gazebo client
    gzclient = ExecuteProcess(
        cmd=['gzclient'],
        output='screen',
        # condition=IfCondition(LaunchConfiguration('gui')),
    )

    #LAUNCH MULTI ROBOT
    robot_spawner = PathJoinSubstitution(
        [FindPackageShare("multi_husky_gazebo"),
        "launch",
        "spawn_multi_husky.launch.py"],
    )

    spawn_h0 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([robot_spawner]),
        launch_arguments={
            'robot_name': 'h0',
            'tfpre': 'h0',
            'x': '0.0',
            'y': '0.0',
            'yaw': '0.0',
            'laser_enabled': laser_enabled,
            'kinect_enabled': kinect_enabled,
            'controller_space': '/h0/controller_manager',
            'joint_broad': 'h0_joint_state_broadcaster',
            'husk_controller': 'h0_husky_velocity_controller'
        }.items(),
    )

    spawn_h1 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([robot_spawner]),
        launch_arguments={
            'robot_name': 'h1',
            'tfpre': 'h1',
            'x': '0.0',
            'y': '-4.0',
            'z': '0.0',
            'yaw': '0.0',
            'laser_enabled': laser_enabled,
            'kinect_enabled': kinect_enabled,
            'controller_space': '/h1/controller_manager',
            'joint_broad': 'h1_joint_state_broadcaster',
            'husk_controller': 'h1_husky_velocity_controller'
        }.items(),
    )

    spawn_h3 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([robot_spawner]),
        launch_arguments={
            'robot_name': 'h3',
            'tfpre': 'h3',
            'x': '0.0',
            'y': '-6.0',
            'z': '0.0',
            'yaw': '0.0',
            'laser_enabled': laser_enabled,
            'kinect_enabled': kinect_enabled,
            'controller_space': '/h3/controller_manager',
            'joint_broad': 'h3_joint_state_broadcaster',
            'husk_controller': 'h3_husky_velocity_controller'
        }.items(),
    )

    spawn_h4 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([robot_spawner]),
        launch_arguments={
            'robot_name': 'h4',
            'tfpre': 'h4',
            'x': '0.0',
            'y': '-8.0',
            'z': '0.0',
            'yaw': '0.0',
            'laser_enabled': laser_enabled,
            'kinect_enabled': kinect_enabled,
            'controller_space': '/h4/controller_manager',
            'joint_broad': 'h4_joint_state_broadcaster',
            'husk_controller': 'h4_husky_velocity_controller'
        }.items(),
    )

    spawn_h8 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([robot_spawner]),
        launch_arguments={
            'robot_name': 'h8',
            'tfpre': 'h8',
            'x': '0.0',
            'y': '-2.0',
            'yaw': '0.0',
            'laser_enabled': laser_enabled,
            'kinect_enabled': kinect_enabled,
            'controller_space': '/h8/controller_manager',
            'joint_broad': 'h8_joint_state_broadcaster',
            'husk_controller': 'h8_husky_velocity_controller'
        }.items(),
    )


    delayed_second_robot = TimerAction(
        period=20.0,
        actions = [
            spawn_h1,
        ]
    )

    delayed_third_robot = TimerAction(
        period=30.0,
        actions = [
            spawn_h3,
        ]
    )
    
    delayed_fourth_robot = TimerAction(
        period=40.0,
        actions = [
            spawn_h4,
        ]
    )
    
    delayed_eighth_robot = TimerAction(
        period=90.0,
        actions = [
            spawn_h8,
        ]
    )




    # # Launch husky_control/control.launch.py which is just robot_localization.
    # launch_husky_control_h1 = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(PathJoinSubstitution(
    #     [FindPackageShare("husky_control"), 'launch', 'control.launch.py'])),
    #     launch_arguments={
    #         'robot_name': 'h1',
    #         'tfpre': 'h1',
    #         'controller_space': '/h1/ekf_node',
    #     }.items(),
    # )

    # # Launch husky_control/control.launch.py which is just robot_localization.
    # launch_husky_control_h0 = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(PathJoinSubstitution(
    #     [FindPackageShare("husky_control"), 'launch', 'control.launch.py'])),
    #     launch_arguments={
    #         'robot_name': 'h0',
    #         'tfpre': 'h0',
    #         'controller_space': '/h1/ekf_node',
    #     }.items(),
    # )

    # delayed_second_localization = TimerAction(
    #     period=10.0,
    #     actions = [
    #         launch_husky_control_h1,
    #     ]
    # )   

    # # Launch huskyUse ROS 2 tools like ros2 topic list, ros2 node list, and ros2 service list to inspect and confirm that th_control/teleop_base.launch.py which is various ways to tele-op
    # # the robot but does not include the joystick. Also, has a twist mux.
    # launch_husky_teleop_base_h1 = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(PathJoinSubstitution(
    #     [FindPackageShare("husky_control"), 'launch', 'teleop_base.launch.py'])),
    #     launch_arguments={
    #         'robot_name': 'h1',
    #         'tfpre': 'h1',
    #     }.items(),
    # )

    # launch_husky_teleop_base_h0 = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(PathJoinSubstitution(
    #     [FindPackageShare("husky_control"), 'launch', 'teleop_base.launch.py'])),
    #     launch_arguments={
    #         'robot_name': 'h1',
    #         'tfpre': 'h1',
    #     }.items(),
    # )

    # delayed_second_teleop = TimerAction(
    #     period=10.0,
    #     actions = [
    #         launch_husky_teleop_base_h1,
    #     ]
    # )   



    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(gz_resource_path)
    ld.add_action(gzserver)
    ld.add_action(gzclient)
    ld.add_action(spawn_h0)
    # ld.add_action(spawn_h1)
    ld.add_action(delayed_second_robot)
    ld.add_action(delayed_third_robot)
    ld.add_action(delayed_fourth_robot)
    ld.add_action(delayed_eighth_robot)
    # ld.add_action(launch_husky_control_h0)
    # ld.add_action(delayed_second_localization)
    # ld.add_action(launch_husky_teleop_base_h0)
    # ld.add_action(delayed_second_teleop)

    return ld
