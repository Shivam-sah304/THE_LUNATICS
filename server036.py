# import asyncio
# import websockets, socket
# import json

# # Store all connected clients
# clients = set()
# clients_id = {}
# # user_id = None


# host = socket.gethostname()
# ip = socket.gethostbyname(host)

# print("Hostname:", host)
# print("IP Address:", ip)

# # Handle a single client connection
# async def dataexchange(websocket):
#     # this function adds all the connected patience and doctors
#     clients.add(websocket)
#     print("Client connected")

#     try:
#         # async for message in websocket:

#         #     if isinstance(message, str):
#         #         try:
#         #             meta = json.loads(message)
#         #             print("JSON received:", meta)

#         #             if meta.get("type") == "auth":
#         #                 user_id = meta.get("user_id")
#         #                 clients_id[user_id] = websocket
#         #                 print("user id is ",user_id)
                        
#         #             elif meta.get("type") == "send":
#         #                 user_id = meta.get("user_id")
#         #                 mesg_text = meta.get("message")
#         #         except json.JSONDecodeError:
#         #             print("Text received:", message)

#         #         for uid,ws in clients_id.items():
#         #             if uid == user_id and ws != websocket:
#         #                 await ws.send(mesg_text)

#         #     elif isinstance(message, bytes):
#         #         print(f"Binary data received ({len(message)} bytes)")

#         #         # for client in clients:
#         #         #     if client != websocket:
#         #         #         await client.send(message)
#         #         for client in clients_id:
#         #             if client[user_id] != websocket:
#         #                 await client.send(message)

#         async for message in websocket:

#             if isinstance(message, str):
#                 try:
#                     meta = json.loads(message)
#                     print("JSON received:", meta)

#                     if meta.get("type") == "auth":
#                         user_id = meta.get("user_id")
#                         clients_id[user_id] = websocket
#                         print("from auth user id is", user_id,"websocket is ",clients_id[user_id])
#                         print("size of dic is ",len(clients_id))

#                     # elif meta.get("type") == "send":
#                     #     recipient_id = meta.get("to")
#                     #     mesg_text = meta.get("message")
#                     #     print("form snd idis ",recipient_id)
#                     #     # send to recipient
#                     #     for uid,recipient_ws in clients_id.items():
#                     #         if uid == recipient_id:
#                     #             print("form send uid ",uid,"websocet is ",recipient_ws)
#                     #             await recipient_ws.send(mesg_text)

#                     elif meta.get("type") == "send":
#                         recipient_id = meta.get("to")
#                         msg_text = meta.get("message")

#                         recipient_ws = clients_id.get(recipient_id)

#                         if recipient_ws and isinstance(msg_text, str):
#                             await recipient_ws.send(msg_text)

#                 except json.JSONDecodeError:
#                     print("Text received:", message)

#             # elif isinstance(message, bytes):
#             #     print(f"Binary data received ({len(message)} bytes)")

#             #     # send to all except sender
#             #     for uid, ws in clients_id.items():
#             #         if ws != websocket:
#             #             await ws.send(message)

#             elif isinstance(message, bytes):
#                 try:
#                     meta = json.loads(message)
#                     print("JSON received:", meta)


#                     # elif meta.get("type") == "send":
#                     #     recipient_id = meta.get("to")
#                     #     mesg_text = meta.get("message")
#                     #     print("form snd idis ",recipient_id)
#                     #     # send to recipient
#                     #     for uid,recipient_ws in clients_id.items():
#                     #         if uid == recipient_id:
#                     #             print("form send uid ",uid,"websocet is ",recipient_ws)
#                     #             await recipient_ws.send(mesg_text)

#                     if meta.get("type") == "send":
#                         recipient_id = meta.get("to")
#                         msg_text = meta.get("message")

#                         recipient_ws = clients_id.get(recipient_id)

#                 except json.JSONDecodeError:
#                     print("Text received:", len(msg_text))
#                     recipient_ws = clients_id.get(recipient_id)
#                 if recipient_ws:
#                     await recipient_ws.send(msg_text)



#     except websockets.exceptions.ConnectionClosed:
#         print("Client disconnected")

#     finally:
#         clients.remove(websocket)
#         print("still connected uid ,web",clients)
# # 192.168.1.6

# async def main():
#     # this does all the stuff like socket ,bind ,listen and also
#     # receives massages into websocket
#     # then calls the handler function for further process
#     async with websockets.serve(dataexchange, ip, 8080,max_size=None):
#         print(f"Server running at ws://{ip}:8080")
#         await asyncio.Future()  # Run forever

# # this fucntion runs the main function asyncronously
# asyncio.run(main())


# # netstat -ano | findstr :8080
# # taskkill /PID 6612 /F




import asyncio
import websockets
import socket
import json

# user_id -> set of websockets (multiple devices supported)
clients = {}

host = socket.gethostname()
ip = socket.gethostbyname(host)

print("Hostname:", host)
print("IP Address:", ip)


async def dataexchange(websocket):
    print("Client connected")
    user_id = None  # store which user this socket belongs to
    current_binary_target = None  # used for binary transfer

    try:
        async for message in websocket:

            # =======================
            # TEXT MESSAGE (JSON)
            # =======================
            if isinstance(message, str):
                try:
                    meta = json.loads(message)
                except json.JSONDecodeError:
                    continue

                print("JSON received:", meta)

                # -------- AUTH --------
                if meta.get("type") == "auth":
                    user_id = meta.get("user_id")

                    if user_id not in clients:
                        clients[user_id] = set()

                    clients[user_id].add(websocket)

                    print("User", user_id, "connected")
                    print("Current users:", list(clients.keys()))

                # -------- SEND TEXT --------
                elif meta.get("type") == "send":
                    recipient_id = meta.get("to")
                    msg_text = meta.get("message")

                    if isinstance(msg_text, str):
                        recipient_sockets = clients.get(recipient_id, set())

                        for ws in recipient_sockets:
                            await ws.send(msg_text)

                # -------- PREPARE FOR BINARY --------
                elif meta.get("type") == "binary":
                    current_binary_target = meta.get("to")

            # =======================
            # BINARY MESSAGE
            # =======================
            elif isinstance(message, bytes):
                if meta.get("type") == "offer":
                    recipient_id = meta.get("to")
                    senders_id = meta.get("from")
                    offer_recv = meta.get("offer")
                    if isinstance(offer_recv,bytes):
                        recipient_sockets =clients.get(recipient_id,set())
                        await recipient_sockets.send({
                            type : "offer",
                            from : "samir",
                        })

                if current_binary_target:
                    recipient_sockets = clients.get(current_binary_target, set())

                    for ws in recipient_sockets:
                        await ws.send(message)

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

    finally:
        # Remove socket from clients
        if user_id and user_id in clients:
            clients[user_id].discard(websocket)

            if not clients[user_id]:  # no devices left
                del clients[user_id]

        print("Remaining users:", list(clients.keys()))


async def main():
    async with websockets.serve(dataexchange, ip, 8080, max_size=None):
        print(f"Server running at ws://{ip}:8080")
        await asyncio.Future()  # run forever


asyncio.run(main())
