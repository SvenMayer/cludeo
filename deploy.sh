#! /bin/sh

ssh -i cluedo.perm pi@raspberrypi << EOF
# Kill running version of the game.
sudo pkill python3
# remove all files in game directory.
rm -rf /home/pi/cluedo/*
EOF

# Create local tar
tar -cf cluedo.tar clue gui
scp -i cluedo.perm cluedo.tar pi@raspberrypi:/home/pi/cluedo/

# ssh connection to server
ssh -i cluedo.perm pi@raspberrypi << EOF
# unpack tar
cd /home/pi/cluedo
tar -xf cluedo.tar
# start new game instance in detached mode.
#sudo nohup python3 /home/pi/cluedo/gui/webgui.py &
# Confirm it is running and has not crashed.

EOF
