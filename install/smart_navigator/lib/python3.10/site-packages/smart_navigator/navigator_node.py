"""Navigates the TurtleBot3 to the room chosen by the decision node."""

import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


class NavigatorNode(Node):
    """Subscribes to /target_room and drives the robot there via Nav2."""

    # Approximate room coordinates for the default turtlebot3_house world.
    # These are (x, y, yaw_radians) in the *map* frame.
    ROOM_COORDS = {
        'kitchen':     ( 0.90,  2.50, 0.0),
        'bedroom':     (-2.80,  2.00, math.pi),
        'livingroom':  (-0.50, -1.00, -math.pi / 2),
    }

    def __init__(self):
        super().__init__('navigator_node')

        self.subscription = self.create_subscription(
            String, '/target_room', self.target_callback, 10
        )

        # BasicNavigator manages its own node internally, so we create it
        # once and reuse it for every goal.
        self.navigator = BasicNavigator()
        self.navigating = False

        self.get_logger().info('NavigatorNode started – waiting for /target_room')

    # ── helpers ────────────────────────────────────────────────────────
    def _make_pose(self, x: float, y: float, yaw: float) -> PoseStamped:
        """Build a PoseStamped in the map frame."""
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.navigator.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0
        # Convert yaw to quaternion (rotation about Z only).
        pose.pose.orientation.z = math.sin(yaw / 2.0)
        pose.pose.orientation.w = math.cos(yaw / 2.0)
        return pose

    # ── callback ──────────────────────────────────────────────────────
    def target_callback(self, msg: String):
        room = msg.data.strip().lower()

        if room not in self.ROOM_COORDS:
            self.get_logger().warn(f'Unknown room "{room}" – ignoring')
            return

        if self.navigating:
            self.get_logger().info(
                f'New target "{room}" received while navigating – cancelling current goal'
            )
            self.navigator.cancelTask()

        x, y, yaw = self.ROOM_COORDS[room]
        goal_pose = self._make_pose(x, y, yaw)

        self.get_logger().info(
            f'Navigating to {room} @ ({x:.2f}, {y:.2f}, yaw={yaw:.2f})'
        )
        self.navigating = True
        self.navigator.goToPose(goal_pose)

        # Spin until the task finishes (non-blocking check each iteration).
        while not self.navigator.isTaskComplete():
            feedback = self.navigator.getFeedback()
            if feedback:
                eta = feedback.estimated_time_remaining.sec
                self.get_logger().info(
                    f'  … navigating to {room}  (ETA ~{eta} s)',
                    throttle_duration_sec=3.0,
                )

        result = self.navigator.getResult()
        self.navigating = False

        if result == TaskResult.SUCCEEDED:
            self.get_logger().info(f'Arrived at {room}!')
        elif result == TaskResult.CANCELED:
            self.get_logger().warn(f'Navigation to {room} was cancelled')
        else:
            self.get_logger().error(f'Navigation to {room} failed (result={result})')


def main(args=None):
    rclpy.init(args=args)
    node = NavigatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
