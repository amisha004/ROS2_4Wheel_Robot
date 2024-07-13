import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


from launch_ros.actions import Node
import xacro

def generate_launch_description():
     
     #name should be same as in Xacro file
     robotXacroName = 'differential_drive_robot'
     
     #name of package same as name of our folder
     namePackage = 'mobile_robot'
     
     #relative path to xacro file defining the model
     modelFileRelativePath = 'model/robot.xacro'
     
     #relative path to the gazebo world file
     worldFileRelativePath = 'model/empty_world.world'
     
     #absolute path to model
     pathModelFile = os.path.join(get_package_share_directory(namePackage), modelFileRelativePath)
     
     #absolute path to world model
     pathWorldFile = os.path.join(get_package_share_directory(namePackage), worldFileRelativePath)
     
     #get robot description from xacro model
     robotDescription = xacro.process_file(pathModelFile).toxml()
     
     #launch file from gazebo_ros package
     gazebo_rosPackageLaunch = PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('gazebo_ros'), 'launch' , 'gazebo.launch.py'))
     
     #launch description
     gazeboLaunch = IncludeLaunchDescription(gazebo_rosPackageLaunch, launch_arguments={'world': pathWorldFile}.items())
     
     #create gazebo node
     spawnModelNode = Node(package='gazebo_ros', executable='spawn_entity.py', arguments=['-topic', 'robot_description', '-entity', robotXacroName], output='screen')
     
     #Robot state publisher node
     nodeRobotStatePublisher = Node(
     	package = 'robot_state_publisher',
     	executable = 'robot_state_publisher',
     	output = 'screen',
     	parameters=[{'robot_description' : robotDescription,
     	'use_sim_time' : True}]
     )
     
     #create empty launch description object
     launchDescriptionObject = LaunchDescription()
     
     #add gazebo launch
     launchDescriptionObject.add_action(gazeboLaunch)
     
     #add two nodes
     launchDescriptionObject.add_action(spawnModelNode)
     launchDescriptionObject.add_action(nodeRobotStatePublisher)
     
     return launchDescriptionObject 
