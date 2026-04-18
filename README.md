# Smart Nav Bot

> An autonomous ground robot that navigates intelligently using a **Decision Tree Algorithm** — making real-time decisions based on sensor data to explore and avoid obstacles without human intervention.

---

## Intro

**Smart Nav Bot** is a ROS 2-based autonomous navigation robot that uses a Decision Tree algorithm to make traversal decisions. The robot continuously reads from its sensors, evaluates environmental conditions through a structured decision tree, and chooses the optimal action — whether to move forward, turn, stop, or reroute.

This project is built on top of a standard ROS 2 workspace and is designed for simulation and real-world deployment on an Unmanned Ground Vehicle (UGV).

---

## Decision Tree Algorithm

The core intelligence of Smart Nav Bot is a **Decision Tree** — a hierarchical model that maps sensor inputs to navigation actions.

```
                    [Obstacle Detected?]
                    /                  \
                  YES                   NO
                  |                     |
        [Distance < Threshold?]    [Move Forward]
          /            \
        YES              NO
        |                |
  [Turn Direction?]  [Slow Down]
   /         \
LEFT         RIGHT
 |             |
[Turn Left]  [Turn Right]
```

### How It Works

1. **Sensor Input** — LiDAR / ultrasonic / camera data is collected each cycle
2. **Feature Extraction** — Raw sensor data is processed into meaningful features (obstacle distance, direction, speed)
3. **Tree Traversal** — The decision tree evaluates conditions from root to leaf
4. **Action Output** — The leaf node returns a navigation command (`forward`, `turn_left`, `turn_right`, `stop`, `reverse`)
5. **Command Publishing** — The action is published as a `geometry_msgs/Twist` message to `/cmd_vel`

---

## Structure

```
smart_nav_bot/
├── src/                    # ROS 2 packages (source code)
│   └── smart_nav_bot/
│       ├── decision_tree/  # Decision tree logic
│       ├── sensors/        # Sensor interface nodes
│       ├── navigation/     # Navigation controller
│       └── utils/          # Helper utilities
├── build/                  # Colcon build artifacts
├── install/                # Installed package files
├── log/                    # Build and runtime logs
├── LICENSE
└── README.md
```

---

## Requirements

| Dependency | Version |
|---|---|
| ROS 2 | Humble / Iron |
| Python | 3.8+ |
| scikit-learn | Latest |
| numpy | Latest |
| geometry_msgs | ROS 2 standard |
| sensor_msgs | ROS 2 standard |

---

## for starters

### 1. Clone the Repository

```bash
git clone https://github.com/jeagerb00b/smart_nav_bot.git
cd smart_nav_bot
```

### 2. Install Dependencies

```bash
pip install scikit-learn numpy
rosdep install --from-paths src --ignore-src -r -y
```

### 3. Build the Workspace

```bash
colcon build
source install/setup.bash
```

### 4. Run the Bot

```bash
ros2 launch smart_nav_bot navigation.launch.py
```

---

## ROS 2 Topics

| Topic | Type | Description |
|---|---|---|
| `/cmd_vel` | `geometry_msgs/Twist` | Velocity commands output |
| `/scan` | `sensor_msgs/LaserScan` | LiDAR input |
| `/odom` | `nav_msgs/Odometry` | Odometry data |
| `/decision_tree/state` | `std_msgs/String` | Current decision state |

---

## Tech Stack

- **ROS 2** — Robot middleware framework
- **Python** — Core logic and decision tree implementation
- **scikit-learn** — Decision tree model (optional ML-based variant)
- **LiDAR / Ultrasonic Sensors** — Environment perception
- **geometry_msgs** — Velocity command interface

---

## Author

**Sarfaras** — Robotics Engineering Student  
GitHub: [@jeagerb00b](https://github.com/jeagerb00b)

---

## License

This project is licensed under the **Apache 2.0 License** — see the [LICENSE](LICENSE) file for details.
