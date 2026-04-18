"""Simulates task conditions and publishes them to /task_conditions."""

import json
import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TaskInputNode(Node):
    """Generates random task conditions at a fixed interval.

    The encoding matches the project CSV dataset:
        Time_of_Day : 0=morning  1=afternoon  2=evening  3=night
        Task_Type   : 0=delivery 1=charging   2=cleaning
        Room_Status : 0=low      1=medium     2=high
    """

    TIME_LABELS = {0: 'morning', 1: 'afternoon', 2: 'evening', 3: 'night'}
    TASK_LABELS = {0: 'delivery', 1: 'charging', 2: 'cleaning'}
    STATUS_LABELS = {0: 'low', 1: 'medium', 2: 'high'}

    def __init__(self):
        super().__init__('task_input_node')
        self.publisher_ = self.create_publisher(String, '/task_conditions', 10)
        self.timer = self.create_timer(5.0, self.publish_conditions)
        self.get_logger().info('TaskInputNode started – publishing every 5 s')

    def publish_conditions(self):
        time_of_day = random.randint(0, 3)
        task_type = random.randint(0, 2)
        room_status = random.randint(0, 2)

        data = {
            'Time_of_Day': time_of_day,
            'Task_Type': task_type,
            'Room_Status': room_status,
        }

        msg = String()
        msg.data = json.dumps(data)
        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Published conditions: '
            f'Time={self.TIME_LABELS[time_of_day]}, '
            f'Task={self.TASK_LABELS[task_type]}, '
            f'Status={self.STATUS_LABELS[room_status]}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = TaskInputNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
