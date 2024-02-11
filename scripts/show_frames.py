#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class WebcamViewerNode(Node):
    def __init__(self):
        super().__init__('webcam_viewer_node')
        self.subscription = self.create_subscription(
            Image,
            'webcam_image',
            self.webcam_callback,
            10  # QoS profile depth
        )
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()

    def webcam_callback(self, msg):
        try:
            # Convert the ROS Image message to OpenCV format
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Display the frame
            cv2.imshow('Webcam Stream', frame)
            cv2.waitKey(1)  # 1 ms delay to allow the OpenCV window to refresh

        except Exception as e:
            self.get_logger().error(f"Error processing webcam image: {str(e)}")

def main(args=None):
    rclpy.init(args=args)
    node = WebcamViewerNode()
    rclpy.spin(node)
    cv2.destroyAllWindows()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

