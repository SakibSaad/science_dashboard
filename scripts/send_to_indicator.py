import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class IndicatorPublisherNode(Node):
    def __init__(self):
        super().__init__('indicator_publisher')
        self.publisher = self.create_publisher(String, '/indicator', 10)
        self.get_logger().info("Indicator publisher node is ready.")
        self.gnss = 0

    def run(self):
        while rclpy.ok():
            print("Autonomous = 'a'\nManual = 'm'\nPoint Reached = 'p'\n")
            user_input = input("choice => ")
            if user_input == 'm':
                message = "Blue -> Manual Mode"
            elif user_input == 'a':
                message = "RED -> Autonomous Mode"
            elif user_input == 'p':
                message = f"Point Reached: {self.gnss}"
                self.gnss += 1
            else:
                self.get_logger().warning("Invalid input. Please enter 'm' or 'a'.")
                continue

            msg = String()
            msg.data = message
            self.publisher.publish(msg)
            self.get_logger().info(f"Published: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = IndicatorPublisherNode()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
