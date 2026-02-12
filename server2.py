import asyncio
import websockets
import socket
import json
import sqlite3

# DATABASE SETUP

conn = sqlite3.connect("chat.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    receiver TEXT,
    message TEXT,
    delivered INTEGER DEFAULT 0
)
""")

conn.commit()

# ONLINE USERS MEMORY

# user_id -> set of websockets
clients = {}

# user_id -> role (doctor / patient)
user_roles = {}

# emergency_id -> selected doctor
active_emergencies = {}

# lock for emergency race condition
emergency_lock = asyncio.Lock()

host = socket.gethostname()
ip = socket.gethostbyname(host)

print("Server IP:", ip)


async def handler(websocket):
    print("Client connected")

    user_id = None
    current_binary_target = None

    try:
        async for message in websocket:

            # STRING MESSAGES
            if isinstance(message, str):

                try:
                    data = json.loads(message)
                except:
                    continue

                msg_type = data.get("type")

                #  AUTH 
                if msg_type == "auth":

                    user_id = data.get("user_id")
                    role = data.get("role")

                    user_roles[user_id] = role

                    if user_id not in clients:
                        clients[user_id] = set()

                    clients[user_id].add(websocket)

                    print(f"{user_id} ({role}) connected")
                    print("Active users:", list(clients.keys()))

                    # Send undelivered messages
                    cursor.execute("""
                        SELECT id, sender, message
                        FROM messages
                        WHERE receiver=? AND delivered=0
                    """, (user_id,))

                    rows = cursor.fetchall()

                    for msg_id, sender, text in rows:
                        await websocket.send(json.dumps({
                            "type": "message",
                            "from": sender,
                            "message": text
                        }))

                        cursor.execute("""
                            UPDATE messages
                            SET delivered=1
                            WHERE id=?
                        """, (msg_id,))
                        conn.commit()

                #  NORMAL MESSAGE 
                elif msg_type == "send":

                    recipient_id = data.get("to")
                    text = data.get("message")

                    cursor.execute("""
                        INSERT INTO messages (sender, receiver, message, delivered)
                        VALUES (?, ?, ?, 0)
                    """, (user_id, recipient_id, text))
                    conn.commit()

                    if recipient_id in clients:
                        for ws in clients[recipient_id]:
                            await ws.send(json.dumps({
                                "type": "message",
                                "from": user_id,
                                "message": text
                            }))

                        cursor.execute("""
                            UPDATE messages
                            SET delivered=1
                            WHERE sender=? AND receiver=? AND message=? AND delivered=0
                        """, (user_id, recipient_id, text))
                        conn.commit()

                #  EMERGENCY BROADCAST 
                elif msg_type == "emergency":

                    if data.get("s") == 1:

                        emergency_id = data.get("emergency_id")

                        async with emergency_lock:

                            active_emergencies[emergency_id] = None

                            print(f"Emergency triggered by {user_id}")

                            # Send to all online doctors
                            for uid, role in user_roles.items():
                                if role == "doctor" and uid in clients:
                                    for ws in clients[uid]:
                                        await ws.send(json.dumps({
                                            "type": "incoming_emergency",
                                            "from": user_id,
                                            "emergency_id": emergency_id
                                        }))

                #  DOCTOR ACCEPT 
                elif msg_type == "accept_emergency":

                    emergency_id = data.get("emergency_id")
                    patient_id = data.get("patient_id")

                    async with emergency_lock:

                        if active_emergencies.get(emergency_id) is None:

                            active_emergencies[emergency_id] = user_id
                            print(f"Doctor {user_id} accepted {emergency_id}")

                            # Notify patient
                            if patient_id in clients:
                                for ws in clients[patient_id]:
                                    await ws.send(json.dumps({
                                        "type": "emergency_accepted",
                                        "doctor": user_id,
                                        "emergency_id": emergency_id
                                    }))

                            # Cancel for other doctors
                            for uid, role in user_roles.items():
                                if role == "doctor" and uid != user_id and uid in clients:
                                    for ws in clients[uid]:
                                        await ws.send(json.dumps({
                                            "type": "emergency_cancelled",
                                            "emergency_id": emergency_id
                                        }))

                #  WEBRTC SIGNALING
                elif msg_type in ["offer", "answer", "ice"]:

                    recipient_id = data.get("to")

                    if recipient_id in clients:
                        for ws in clients[recipient_id]:
                            await ws.send(json.dumps(data))

                elif msg_type == "binary":
                    current_binary_target = data.get("to")

            # BINARY FILE DATA
        
            elif isinstance(message, bytes):

                if current_binary_target and current_binary_target in clients:
                    for ws in clients[current_binary_target]:
                        await ws.send(message)

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

    finally:
        if user_id and user_id in clients:
            clients[user_id].discard(websocket)

            if not clients[user_id]:
                del clients[user_id]
                user_roles.pop(user_id, None)

        print("Remaining users:", list(clients.keys()))


async def main():
    async with websockets.serve(handler, ip, 8080, max_size=None):
        print(f"Server running at ws://{ip}:8080")
        await asyncio.Future()


asyncio.run(main())
