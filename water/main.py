import rclpy
from . import pump
from rclpy.node import Node
from std_msgs.msg import String

DAY = 'day'
NIGHT = 'night'

class Pump(Node):

    def __init__(self):
        super().__init__('sun')
        self.pump = pump.Pump()
        self.subscription = self.create_subscription(
            String,
            'day',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):

        self.get_logger().info('Getting: "%s"' % msg.data)
        
        if msg.data == DAY:
            self.pump.flow()
        
        elif msg.data == NIGHT:
            self.pump.stop()

def main(args=None):
    rclpy.init(args=args)

    pump_subscriber = Pump()

    rclpy.spin(pump_subscriber)

    pump_subscriber.pump.shutdown()
    pump_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()