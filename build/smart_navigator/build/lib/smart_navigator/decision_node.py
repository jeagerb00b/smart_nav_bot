"""Predicts which room the robot should visit using a Decision Tree.

Trains on a CSV dataset installed with the package.
"""

import csv
import json
import os

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from ament_index_python.packages import get_package_share_directory
from sklearn.tree import DecisionTreeClassifier  # type: ignore


# ── label encoding maps (must match input_node.py) ────────────────────
TIME_MAP = {'morning': 0, 'afternoon': 1, 'evening': 2, 'night': 3}
TASK_MAP = {'delivery': 0, 'charging': 1, 'cleaning': 2}
STATUS_MAP = {'low': 0, 'medium': 1, 'high': 2}


class DecisionNode(Node):
    """Subscribes to /task_conditions, predicts a room, publishes to /target_room."""

    def __init__(self):
        super().__init__('decision_node')

        # ── publishers / subscribers ──────────────────────────────────
        self.publisher_ = self.create_publisher(String, '/target_room', 10)
        self.subscription = self.create_subscription(
            String, '/task_conditions', self.conditions_callback, 10
        )

        # ── load and train on the CSV dataset ─────────────────────────
        self.model = DecisionTreeClassifier(random_state=42)
        self._train_from_csv()

    # ── training ──────────────────────────────────────────────────────
    def _train_from_csv(self):
        """Load data/dataset.csv from the installed package share dir."""
        share_dir = get_package_share_directory('smart_navigator')
        csv_path = os.path.join(share_dir, 'data', 'dataset.csv')

        X_train = []
        y_train = []

        with open(csv_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                time_val = TIME_MAP[row['Time of Day'].strip().lower()]
                task_val = TASK_MAP[row['Task Type'].strip().lower()]
                status_val = STATUS_MAP[row['Room status'].strip().lower()]
                target = row['Target Room'].strip().lower()

                X_train.append([time_val, task_val, status_val])
                y_train.append(target)

        self.model.fit(X_train, y_train)
        self.get_logger().info(
            f'DecisionNode started – model trained on {len(y_train)} samples from {csv_path}'
        )

    # ── callback ──────────────────────────────────────────────────────
    def conditions_callback(self, msg: String):
        try:
            data = json.loads(msg.data)
            features = [[
                data['Time_of_Day'],
                data['Task_Type'],
                data['Room_Status'],
            ]]
        except (json.JSONDecodeError, KeyError) as exc:
            self.get_logger().error(f'Bad payload on /task_conditions: {exc}')
            return

        prediction = self.model.predict(features)[0]

        out = String()
        out.data = prediction
        self.publisher_.publish(out)
        self.get_logger().info(f'Predicted target room: {prediction}')


def main(args=None):
    rclpy.init(args=args)
    node = DecisionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
