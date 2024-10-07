Run these commands before opening jmavsim
export JAVA_HOME=$(/usr/libexec/java_home -v 15)
export PATH=$JAVA_HOME/bin:$PATH
make px4_sitl_default jmavsim

make sure you are in the Firmware directory

then run the webserver as normal
python manage.py runserver

to run the frontend we need to move to the drone-webserver-frontend folder and execute
npm start