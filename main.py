import asyncio
import websockets
import json
import _thread
from recv import recv
from anime.what_time_now import what_time_now

ip = ""
port = ""
verifyKey = ""

uri = "ws://{}:{}/all?verifyKey={}&sessionKey=SINGLE_SESSION".format(ip, port, verifyKey)

async def hello():
    async with websockets.connect(uri) as websocket:
        # asyncio.get_event_loop().run_until_complete(what_time_now(websocket))
        while True:
            recv_text = await websocket.recv()
            recv_text = json.loads(recv_text)
            if recv_text["syncId"] == "-1":
                await recv(websocket, recv_text)

                
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(hello())
