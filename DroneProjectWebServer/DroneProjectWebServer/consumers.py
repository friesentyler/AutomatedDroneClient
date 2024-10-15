import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio

from mavsdk import System


class GPSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.drone = System()
        await self.drone.connect(system_address="udp://:14540")

        print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print(f"-- Connected to drone!")
                break

        await self.accept()

    async def disconnect(self, close_code):
        print("Websocket disconnected, closing drone connection...")

    async def receive(self, text_data):
        # construct gps data to return to client
        gps_data = {
            'lat': 0,
            'long': 0
        }

        while True:
            print("Waiting for drone to have a global position estimate...")
            async for health in self.drone.telemetry.health():
                if health.is_global_position_ok and health.is_home_position_ok and health.is_local_position_ok and health.is_gyrometer_calibration_ok and health.is_accelerometer_calibration_ok:
                    print("-- Global position estimate OK")
                    break

            print("Retrieving GPS position data...")
            async for position in drone.telemetry.position():
                print(f"Latitude: {position.latitude_deg}, "
                      f"Longitude: {position.longitude_deg}, "
                      f"Absolute Altitude: {position.absolute_altitude_m} m, "
                      f"Relative Altitude: {position.relative_altitude_m} m")
                # update gps positional data which gets returned
                gps_data['lat'] = position.latitude_deg
                gps_data['long'] = position.longitude_deg

            await self.send(text_data=json.dumps(gps_data))
            await asyncio.sleep(0.1)
