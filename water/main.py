import rclpy
import os
from . import pump
from . import utils
from rclpy.node import Node
from std_msgs.msg import String

DAY = 'day'
NIGHT = 'night'
PIN = int(os.getenv('PIN',15))
MIN_INTERVAL = int(os.getenv('MIN_INTERVAL',10))

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
        
        if msg.data == NIGHT or not self.is_active_periode():
            self.pump.stop()
            self.get_logger().info('Stopping pump')

        elif msg.data == DAY:
            self.pump.flow()
            self.get_logger().info('Staring pump')
        
    def is_active_periode(self):
        nanoseconds = self.get_clock().now().nanoseconds
        minute_of_day = utils.nanoseconds_to_minutes(nanoseconds)

        return minute_of_day < MIN_INTERVAL
  
def main(args=None):
    rclpy.init(args=args)

    pump_subscriber = Water()

    rclpy.spin(pump_subscriber)

    pump_subscriber.pump.shutdown()
    pump_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()