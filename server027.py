import asyncio, socket, websockets, json


# Store all connected clients
clients = set()
clients_id = {}

IP = socket.gethostbyname(socket.gethostname())
print(IP)

# Handle a single client connection
async def dataexchange(websocket):
    # this function adds all the connected patience and doctors
    clients.add(websocket)
    print(websocket)
    print("Client connected")

    try:
        async for message in websocket:

            if isinstance(message, str):
                try:
                    meta = json.loads(message)
                    print("JSON received:", meta)
                except json.JSONDecodeError:
                    print("Text received:", message)

                for client in clients:
                    if client != websocket:
                        await client.send(message)

            elif isinstance(message, bytes):
                print(f"Binary data received ({len(message)} bytes)")

                for client in clients:
                    if client != websocket:
                        await client.send(message)

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

    finally:
        clients.remove(websocket)
# 192.168.1.6

async def main():
    # this does all the stuff like socket ,bind ,listen and also
    # receives massages into websocket
    # then calls the handler function for further process
    async with websockets.serve(dataexchange, IP, 8080,max_size=None):
        print(f"Server running at ws://{IP}:8080")
        await asyncio.Future()  # Run forever

# this fucntion runs the main function asyncronously
asyncio.run(main())


# netstat -ano | findstr :8080
# taskkill /PID 6612 /F

