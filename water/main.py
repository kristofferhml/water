import rclpy
import os
from . import pump
from . import utils
from rclpy.node import Node
from std_msgs.msg import String
import time
from datetime import datetime

DAY = 'day'
NIGHT = 'night'
PIN = int(os.getenv('PIN',15))
MIN_INTERVAL = int(os.getenv('MIN_INTERVAL',10))
WATER_MIN_MINUTE_DIFF = int(os.getenv('WATER_MIN_MINUTE_DIFF', 3))
WATER_MIN_MINUTE_DIFF_NIGHT = int(os.getenv('WATER_MIN_MINUTE_DIFF_NIGHT',3))

class Water(Node):

    def __init__(self):
        super().__init__('water')
        self.get_logger().info('Startig water with on pin "%d" and min interval of "%d"' % (PIN, MIN_INTERVAL))
        self.pump = pump.Pump(PIN)
        self.subscription = self.create_subscription(
            String,
            'day',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):

        self.get_logger().info('Getting: "%s"' % msg.data)

        min_diff = WATER_MIN_MINUTE_DIFF if msg.data == DAY else WATER_MIN_MINUTE_DIFF_NIGHT

        minutes_since_last_run = self.get_minutes_since_last_run()

        if minutes_since_last_run < MIN_INTERVAL:
            self.get_logger().info('Starting pump, minutes since last run within interval: %d' % minutes_since_last_run)
            self.pump.flow()
        else: 
            self.get_logger().info('Stopping pump, minutes since last run within interval: %d' % minutes_since_last_run)
            self.pump.stop()
        
        if (minutes_since_last_run > min_diff):
            self.get_logger().info('Diff interval reached. Setting last run: %d' % minutes_since_last_run)
            self.last_run = datetime.now()

    def get_minutes_since_last_run(self):

        try:
            last_run_difference = datetime.now() - self.last_run
            minutes = last_run_difference.total_seconds() / 60  
            self.get_logger().info('Minutes since last run: "%d"' % minutes)
            return minutes
            
        except AttributeError:
            self.get_logger().info('Inital run. Setting last_run')
            self.last_run = datetime.now()
        
        return 0
    

def main(args=None):
    rclpy.init(args=args)

    pump_subscriber = Water()

    rclpy.spin(pump_subscriber)

    pump_subscriber.pump.shutdown()
    pump_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()