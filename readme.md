# Drone Web Server
* this project aims to create a webserver that can automate a drone's movements using a google map interface
* Take a look below to see the already implemented functionality
* It uses the mavlink protocol to send commands to a drone via a Django web server
* The frontend uses React and the google maps library to send commands to the drone 

When the project is complete the webserver will run on the cloud where anyone with the proper credentials 
can connect and send commands to the drone. The drone will be connected to the internet via cellular towers so that
the operator can be hundred of miles away and still issue commands to the drone.\

# Some clips of the software in action

### Frontend
![high_quality_output](https://github.com/user-attachments/assets/d612e68b-2ab1-439c-a31d-b96b05630627)

### Takeoff
![high_quality_output](https://github.com/user-attachments/assets/94455efd-4c0f-4bac-b757-6eaefee673e9)

### Goto
![high_quality_output](https://github.com/user-attachments/assets/6192b267-4eaa-4515-b91b-8dd9cbfcb887)

### Land
![high_quality_output](https://github.com/user-attachments/assets/01c14f71-025a-453b-a831-fc7335fef337)



# Helpful instructions for building and running the project

### Project Backend (Django webserver)
Run these commands before opening jmavsim (for simulating the drone)
`export JAVA_HOME=$(/usr/libexec/java_home -v 15)
export PATH=$JAVA_HOME/bin:$PATH
make px4_sitl_default jmavsim`

make sure you are in the PX4-Autopilot directory

You will need to clone this repo inside DroneProjectWebServer/DroneProjectWebServer in order to run jmavsim and create
the PX4-Autopilot directory
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
then build the PX4-Autopilot
make px4_sitl jmavsim

this website is pretty helpful for issues with jmavsim
https://docs.px4.io/main/en/sim_jmavsim/index.html

in the future I will most likely move to gazebo, it appears to be more modern

then run the webserver using daphne since we need an async capable webserver to handle websockets
daphne -p 8000 DroneProjectWebServer.asgi:application

### Project Frontend (React + Google maps library)
to run the frontend we need to move to the drone-webserver-frontend folder and execute
`npm start`
