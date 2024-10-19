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
        tasks = asyncio.all_tasks()
        for task in tasks:
            task.cancel()
        print("Websocket disconnected, closing drone connection...")

    async def send_gps_data(self):
        # TODO
        #47.3977417, 'long': 8.545594099999999
        # 47.3977417, 'long': 8.545594099999999
        # Something is fishy here, the GPS coordinates are not accurate/updating accurately to match the drone's position on the map
        # check MAVSDK docs to check for accuracy on GPS, look into JMavSim GPS location reporting if it exists
        # also on page reload the drone marker jumps to the correct position, so evidently its getting the correct GPS data from
        # somewhere, so why isn't that updating correctly everytime?

        # Ok it is definitely an issue with the websocket implementation because the REST endpoint is sending the proper data
        while True:
            async for position in self.drone.telemetry.position():
                gps_data = {'lat': position.latitude_deg, 'long': position.longitude_deg}
                print(f"Sending GPS Data: {gps_data}")
                await self.send(text_data=json.dumps(gps_data))
                await asyncio.sleep(3)  # Send data every second
                break

    async def receive(self, text_data):
        # If you need to handle incoming messages from the client
        print(f"Received message from client: {text_data}")

