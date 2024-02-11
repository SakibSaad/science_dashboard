import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import subprocess
import re

class RoverLatencyNode(Node):

    def __init__(self):
        super().__init__('rover_latency_node')
        self.publisher_ = self.create_publisher(String, '/latency', 10)
        self.timer = self.create_timer(1.0, self.ping_and_publish)

    def ping_and_publish(self):

        ip_address = "192.168.1.120" # jetson IP
        ip_address_1 = "192.168.1.110" # RPi IP
        try:
            
            result = subprocess.run(['ping', '-c', '1', ip_address], capture_output=True, text=True, timeout=5)
            result_1 = subprocess.run(['ping', '-c', '1', ip_address_1], capture_output=True, text=True, timeout=5)
            if result.returncode == 0 or result_1.returncode == 0:

                ping_output = str(result)
                ping_output_1 = str(result_1)

                time_match = re.search(r'time=(\d+(\.\d+)?)\s*ms', ping_output)
                time_match_1 = re.search(r'time=(\d+(\.\d+)?)\s*ms', ping_output_1)

                if time_match:
                    latency = time_match.group(1) 
                else:
                    latency = "down"

                if time_match_1:
                    latency_1 = time_match_1.group(1) 
                else:
                    latency_1 = "down"

                latency = latency + ";" + latency_1

                self.publisher_.publish(String(data=str(latency)))
                
            else:
                self.publisher_.publish(String(data='down;down'))


        except subprocess.TimeoutExpired:
            self.publisher_.publish(String(data='down;down'))

def main(args=None):
    rclpy.init(args=args)
    node = RoverLatencyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

