"""Launch all three Smart Navigator nodes."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='smart_navigator',
            executable='input_node',
            name='task_input_node',
            output='screen',
        ),
        Node(
            package='smart_navigator',
            executable='decision_node',
            name='decision_node',
            output='screen',
        ),
        Node(
            package='smart_navigator',
            executable='navigator_node',
            name='navigator_node',
            output='screen',
        ),
    ])
