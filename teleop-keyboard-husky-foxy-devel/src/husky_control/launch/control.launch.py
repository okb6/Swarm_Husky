from launch import LaunchContext, LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import EnvironmentVariable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

ARGUMENTS = [
    #Get values from multi_husky_playpen.launch
    DeclareLaunchArgument('tfpre', default_value='h0'),

]


def generate_launch_description():
    tfpre = LaunchConfiguration('tfpre')
    lc = LaunchContext()
    ld = LaunchDescription(ARGUMENTS)

    config_husky_ekf = PathJoinSubstitution(
        [FindPackageShare('husky_control'),
        'config',
        'localization.yaml'],
    )

    node_ekf = Node(
        package='robot_localization',
        namespace=tfpre,
        executable='ekf_node',
        name='ekf_node',
        output='screen',
        parameters=[config_husky_ekf],
        )
    ld.add_action(node_ekf)

    primary_imu_enable = EnvironmentVariable('CPR_IMU', default_value='false')

    if (primary_imu_enable.perform(lc)) == 'true':
        config_imu_filter = PathJoinSubstitution(
            [FindPackageShare('husky_control'),
            'config',
            'imu_filter.yaml'],
        )
        node_imu_filter = Node(
            package='imu_filter_madgwick',
            namespace=tfpre,
            executable='imu_filter_madgwick_node',
            name='imu_filter',
            output='screen',
            parameters=[config_imu_filter]
        )

        ld.add_action(node_imu_filter)


    return ld