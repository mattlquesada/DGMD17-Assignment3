import rospy
import math, time
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist

sub_topic = "/range"
pub_topic = "/cmd_vel"

def callback(data):
	# Publish to the command velocity topic
    pub_twist = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    message_cmd = Twist()
    
    print("Changing speed and directionality")

    # Change directionality based on the shortest (out of 45) laser vector distances; then rotate the robot
    print("Changing directionality: angle increment index: {}, angular vel: {}".format(data.radiation_type, get_angular(data.radiation_type)))
    message_cmd.linear.x = 0
    message_cmd.angular.z = get_angular(data.radiation_type)
    pub_twist.publish(message_cmd)
    time.sleep(1) # Angular velocity is in untis of radian/s. To achieve the correct total rotation angle, rotate for 1s

    # Move forward once angle has been modified
    message_cmd = Twist()
    print("Changing velocity to 1")
    if get_angular(data.radiation_type) == 0:
        message_cmd.linear.x = 0 # Stops when no object detected
    else:
        message_cmd.linear.x = 0.05
        
    message_cmd.angular.z = 0 # Stop angular movement when performing starting forward movement 
    pub_twist.publish(message_cmd)
    time.sleep(1)

def get_angular(index):
    positive_radians = 22.5
    if index == 0:
        return 0
    if index>0 and index<=22:
        # negative rotation
        return -.3909538*(1-(index/22.5))
    elif index > 22:
        # positive rotation
        return (index-22.5)/22.5 * .3909538


if __name__ == "__main__":
    rospy.init_node('follow')
    rospy.Subscriber(sub_topic, Range, callback)
    rospy.spin()

