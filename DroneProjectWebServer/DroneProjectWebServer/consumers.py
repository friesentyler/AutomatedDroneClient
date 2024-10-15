import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from mavsdk import System


class GPSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.drone = System()
        await self.drone.connect(system_address="udp://:14540")

        print("Waiting for drone to connect...")
        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print(f"-- Connected to drone!")
                break

        print("Waiting for global position estimate...")
        async for health in self.drone.telemetry.health():
            if health.is_global_position_ok:
                print("-- Global position estimate OK")
                break

        await self.accept()

        # Now start sending GPS data to the client
        asyncio.create_task(self.send_gps_data())

    async def disconnect(self, close_code):
        print("Websocket disconnected, closing drone connection...")

    async def send_gps_data(self):
        gps_data = {'lat': 0, 'long': 0}

        while True:
            async for position in self.drone.telemetry.position():
                gps_data['lat'] = position.latitude_deg
                gps_data['long'] = position.longitude_deg
                print(f"Sending GPS Data: {gps_data}")
                await self.send(text_data=json.dumps(gps_data))
                await asyncio.sleep(5)  # Send data every second

    async def receive(self, text_data):
        # If you need to handle incoming messages from the client
        print(f"Received message from client: {text_data}")

