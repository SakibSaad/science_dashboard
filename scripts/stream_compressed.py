#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
import cv2
from sensor_msgs.msg import CompressedImage  # Import CompressedImage message

class WebcamStreamNode(Node):
    def __init__(self):
        super().__init__('webcam_stream_node')
        self.publisher_ = self.create_publisher(CompressedImage, 'webcam_image/compressed', 10)  # Change topic name
        # Increase the timer frequency to increase fps
        self.timer = self.create_timer(0.05, self.publish_webcam_image)
        self.cap = cv2.VideoCapture(0)  # 0 represents the default camera (you may need to change this depending on your setup)
        self.bridge = CvBridge()

    def publish_webcam_image(self):
        ret, frame = self.cap.read()
        if ret:
            # Resize the frame to lower the resolution
            frame = cv2.resize(frame, (320, 240))

            # Compress the frame
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]  # Adjust quality as needed
            _, compressed_data = cv2.imencode('.jpg', frame, encode_param)

            # Convert compressed data to bytes and create CompressedImage message
            msg = CompressedImage()
            msg.format = 'jpeg'
            msg.data = compressed_data.tobytes()

            # Publish the CompressedImage message
            self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = WebcamStreamNode()
    rclpy.spin(node)

    # Release the capture object
    node.cap.release()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
