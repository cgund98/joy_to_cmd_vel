#!/home/callum/anaconda2/bin/python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

class ConverterWrapper(object):
    def __init__(self):
        # self._pub = rospy.Publisher('/cmd_vel', Twist) # Disabled because I'm outputting to a different place
        self._pub = rospy.Publisher('/rover/mobile_base_controller/cmd_vel', Twist)
        self._sub = rospy.Subscriber('/joy', Joy, self.convert)
        self._vel = Twist()
        self._invert_x = True
        self._invert_z = False

    def convert(self, joy):
        self._vel.linear.x = joy.axes[1]
        if self._invert_x: self._vel.linear.x = -self._vel.linear.x
        self._vel.angular.z = joy.axes[0]
        if self._invert_z: self._vel.angular.z = -self._vel.angular.z

        self._pub.publish(self._vel)

    def stop(self):
        self._vel.linear.x = 0
        self._vel.angular.z = 0

        self._pub.publish(self._vel)

if __name__ == "__main__":
    rospy.init_node("joy_to_cmd_vel")

    converter = ConverterWrapper()

    print("Starting up!")
    while not rospy.is_shutdown():
        rospy.spin()

    converter.stop()
