import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/subin/cnu_ros2/heart_robot/src/install/heart_robot_control'
