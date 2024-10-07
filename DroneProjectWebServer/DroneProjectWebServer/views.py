from django.http import HttpResponse
import asyncio
from mavsdk import System
from mavsdk.action import OrbitYawBehavior
from mavsdk.offboard import VelocityNedYaw, OffboardError


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

async def takeoff(request):

    drone = System()
    await drone.connect(system_address="udp://:14540")

    #status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok and health.is_local_position_ok and health.is_gyrometer_calibration_ok and health.is_accelerometer_calibration_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()
    return HttpResponse("success")

# TODO
# THIS COMMAND NEEDS TO KILL ALL HORIZONTAL VELOCITY BEFORE TRYING TO LAND
async def land(request):
    drone = System()
    await drone.connect(system_address="udp://:14540")

    # status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok and health.is_local_position_ok and health.is_gyrometer_calibration_ok and health.is_accelerometer_calibration_ok:
            print("-- Global position estimate OK")
            break

    print("-- Initiate Velocity Kill")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(north_m_s=0.0, east_m_s=0.0, down_m_s=0.0, yaw_deg=0.0))
    try:
        await drone.offboard.start()
        print("-- Offboard mode started")
    except OffboardError as error:
        print(f"Failed to start offboard mode: {error._result.result}")
        await drone.action.disarm()
        return
    # Keep sending the command for some time to ensure the drone receives it
    await asyncio.sleep(3)

    print("-- Stopping Offboard mode")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Failed to stop offboard mode: {error._result.result}")

    print("-- Landing")
    await drone.action.land()
    return HttpResponse("success")

async def goto(request, lat, long):
    lat = float(lat)
    long = float(long)
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok and health.is_local_position_ok and health.is_gyrometer_calibration_ok and health.is_accelerometer_calibration_ok:
            print("-- Global position state is good enough for flying.")
            break

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        relative_altitude = terrain_info.relative_altitude_m
        if relative_altitude < 2.5:
            relative_altitude = 2.5
        break

    # To fly drone 20m above the ground plane
    flying_alt = absolute_altitude + relative_altitude
    print(absolute_altitude, relative_altitude, flying_alt)
    # goto_location() takes Absolute MSL altitude
    await drone.action.goto_location(lat, long, flying_alt, 0)
    # lat 47.397606
    # long 8.543060

    return HttpResponse("success")

async def altadjust(request, newalt):
    newalt = float(newalt)
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok and health.is_local_position_ok and health.is_gyrometer_calibration_ok and health.is_accelerometer_calibration_ok:
            print("-- Global position state is good enough for flying.")
            break

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        long = terrain_info.longitude_deg
        lat = terrain_info.latitude_deg
        break

    flying_alt = absolute_altitude + newalt
    await drone.action.goto_location(lat, long, flying_alt, 0)
    return HttpResponse("success")

async def circle(request, lat, long, radius):
    lat = float(lat)
    long = float(long)
    radius = float(radius)
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok and health.is_local_position_ok and health.is_gyrometer_calibration_ok and health.is_accelerometer_calibration_ok:
            print("-- Global position state is good enough for flying.")
            break

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        relative_altitude = terrain_info.relative_altitude_m
        if relative_altitude < 2.5:
            relative_altitude = 2.5
        break

    # To fly drone 20m above the ground plane
    flying_alt = absolute_altitude + relative_altitude
    print(absolute_altitude, relative_altitude, flying_alt)
    # do_orbit() takes Absolute MSL altitude
    await drone.action.do_orbit(radius, 0.5, OrbitYawBehavior(0), lat, long, flying_alt)
    return HttpResponse("success")

async def cancel(request):
    drone = System()
    await drone.connect(system_address="udp://:14540")

    # status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok and health.is_local_position_ok and health.is_gyrometer_calibration_ok and health.is_accelerometer_calibration_ok:
            print("-- Global position estimate OK")
            break

    print("-- Initiate Velocity Kill")
    print("-- Setting velocity to 0 for North and East directions")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(north_m_s=0.0, east_m_s=0.0, down_m_s=0.0, yaw_deg=0.0))
    try:
        await drone.offboard.start()
        print("-- Offboard mode started")
    except OffboardError as error:
        print(f"Failed to start offboard mode: {error._result.result}")
        await drone.action.disarm()
        return
    # Keep sending the command for some time to ensure the drone receives it
    await asyncio.sleep(3)

    print("-- Stopping Offboard mode")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Failed to stop offboard mode: {error._result.result}")
    return HttpResponse("success")