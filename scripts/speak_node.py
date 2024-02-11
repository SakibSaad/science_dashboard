import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class AudioPlayerNode(Node):

    def __init__(self):
        super().__init__('dashboard_speak_node')
        self.subscription = self.create_subscription(
            String,
            '/indicator',
            self.indicator_callback,
            10
        )
        pygame.mixer.init()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))  
        self.parent_dir = os.path.abspath(os.path.join(self.script_dir, os.pardir))  
        self.resource_dir = self.parent_dir + '/asset/audio/'

    def indicator_callback(self, msg):
        indicator = msg.data
        audio_file = self.get_audio_file(indicator)

        if audio_file:
            try:
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                self.get_logger().info(f'Playing sound: {audio_file}')
            except Exception as e:
                self.get_logger().error(f"Error playing audio: {str(e)}")
        else:
            self.get_logger().warn(f"No audio file found for indicator: {indicator}")

    def get_audio_file(self, indicator):
        if indicator.startswith("RED -> Autonomous Mode"):
            return f'{self.resource_dir}autonomous.mp3'
        elif indicator.startswith("Blue -> Manual Mode"):
            return f'{self.resource_dir}manual.mp3'
        elif indicator.startswith("Point Reached: "):
            try:
                point = int(indicator.split(": ")[1])
                return f'{self.resource_dir}{point}.mp3'
            except ValueError:
                self.get_logger().warn(f"Invalid point value: {indicator}")
        return None

def main(args=None):
    rclpy.init(args=args)
    node = AudioPlayerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        pygame.mixer.quit()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
