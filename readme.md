Run these commands before opening jmavsim
export JAVA_HOME=$(/usr/libexec/java_home -v 15)
export PATH=$JAVA_HOME/bin:$PATH
make px4_sitl_default jmavsim

make sure you are in the PX4-Autopilot directory

You will need to clone this repo inside DroneProjectWebServer/DroneProjectWebServer in order to run jmavsim and create
the PX4-Autopilot directory
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
then build the PX4-Autopilot
make px4_sitl jmavsim

this website is pretty helpful for issues with jmavsim
https://docs.px4.io/main/en/sim_jmavsim/index.html

in the future I will most likely move to gazebo, it appears to be more modern

then run the webserver as normal
python manage.py runserver

#to run the frontend we need to move to the drone-webserver-frontend folder and execute
npm start