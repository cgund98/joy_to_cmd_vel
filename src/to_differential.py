#!/home/callum/anaconda2/bin/python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from sensor_msgs.msg import Joy

class ConverterWrapper(object):
    def __init__(self):
        # self._pub = rospy.Publisher('/cmd_vel', Twist) # Disabled because I'm outputting to a different place
        self._lpub = rospy.Publisher('/lwheel_vtarget', Float32)
        self._rpub = rospy.Publisher('/rwheel_vtarget', Float32)
        self._sub = rospy.Subscriber('/joy', Joy, self.convert)
        self._lvel = Float32()
        self._rvel = Float32()
        # self._invert_x = True
        # self._invert_z = False

    def convert(self, joy):
        self._lvel.data = joy.axes[1]*.92 - joy.axes[0]/2
        self._rvel.data = joy.axes[1] + joy.axes[0]/2
        # if self._invert_x: self._vel.linear.x = -self._vel.linear.x
        # self._vel.angular.z = joy.axes[0]
        # if self._invert_z: self._vel.angular.z = -self._vel.angular.z

        self._lpub.publish(self._lvel)
        self._rpub.publish(self._rvel)

    def stop(self):
        self._lvel.data = 0
        self._rvel.data = 0

        self._lpub.publish(self._lvel)
        self._rpub.publish(self._rvel)

if __name__ == "__main__":
    rospy.init_node("joy_to_cmd_vel")

    converter = ConverterWrapper()

    print("Starting up!")
    while not rospy.is_shutdown():
        rospy.spin()

    converter.stop()
