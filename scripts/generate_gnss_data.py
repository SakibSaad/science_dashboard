import time
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix

class GNSSPublisherNode(Node):
    def __init__(self):
        super().__init__('nav_sat_publisher')
        self.publisher = self.create_publisher(NavSatFix, '/nav_sat', 10)
        self.get_logger().info("GNSS publisher node is ready.")
        self.gps_msg = NavSatFix()
        self.gps_msg.latitude = 23.798797
        self.gps_msg.longitude = 90.449151

    def run(self):
        while rclpy.ok():
            # Generating GPS coordinates 
            self.gps_msg.latitude = float("{:.7f}".format(self.gps_msg.latitude))
            self.gps_msg.longitude = float("{:.7f}".format(self.gps_msg.longitude))

            self.publisher.publish(self.gps_msg)
            self.get_logger().info(f"Published GNSS: {self.gps_msg.latitude}, {self.gps_msg.longitude}")

            self.gps_msg.latitude += 0.00001
            self.gps_msg.longitude += 0.000001

            
            time.sleep(1)

def main(args=None):
    rclpy.init(args=args)
    node = GNSSPublisherNode()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()