#!/usr/bin/env python
import rospy

from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Range

pub_topic = "/range"
sub_topic = "/scan"

pub = rospy.Publisher(pub_topic, Range, queue_size=1)


def callback(data):

    range_msg = Range()
    min_index = data.ranges.index(min(data.ranges)) # Stores the index of the minimum value 
    range_msg.range = data.ranges[min_index]
    rospy.loginfo(rospy.get_caller_id() + "I heard indx: {}, distance: {}".format(min_index, data.ranges[min_index]))
    
    
    if data.ranges[min_index] < 100:
        rospy.loginfo("object detected")
    else:
        rospy.loginfo("no object detected")

    range_msg.header.stamp = rospy.Time.now()
    range_msg.header.frame_id = data.header.frame_id
    
    # Workaround: use "radiation_type" parameter to pass in the index of the minimum value
    range_msg.radiation_type = min_index 
    
    # 45 Degrees Total   
    range_msg.field_of_view = 0.7819076
    
    range_msg.min_range = 0.1
    range_msg.max_range = 100
    range_msg.range = data.ranges.index(min(data.ranges))
    
    pub.publish(range_msg)


rospy.init_node("sonar_node", anonymous=True)
rospy.Subscriber(sub_topic, LaserScan, callback)

rospy.spin()
