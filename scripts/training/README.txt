# COBOT TO REACH TARGET POSE

# Pull ROS docker
docker pull gvolpe83/ros2_ur_complete

# Run MobaXTerm

# Run Docker with display env set
cd <path-to-scripts>
docker run -e DISPLAY=192.168.1.108:0.0 -p 6006:6006 --name ros2_ur --rm -v .\scripts:/root/ros2_ws/scripts -it gvolpe83/ros2_ur_complete

# Run sample robot inside container
ros2 launch ur_description view_ur.launch.py ur_type:=ur3e

# Run second container for training and control
docker exec -it ros2_ur bash
# Don't forget to source the ennvironment
source /ros_entrypoint.sh
# Go to training directory
cd /root/ros2_ws/scripts/training

# 1. Sample Random env
python3 test_gym_random.py
# 2. Test Training with SAC & Tensorboard
python3 test_training.py
# 3. Test trained policy
python3 test_after_training.py

