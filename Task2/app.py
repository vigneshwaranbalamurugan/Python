import asyncio, json, websockets, sqlite3
from datetime import datetime

DB_NAME = "chat.db"
users = {}
rooms = {}

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages
        (id INTEGER PRIMARY KEY,
         chat_id TEXT,
         sender TEXT,
         text TEXT,
         timestamp TEXT)
    ''')
    conn.commit()
    conn.close()

async def broadcast(targets, msg):
    data = json.dumps(msg)
    for name in targets:
        if name in users:
            try:
                await users[name].send(data)
            except:
                pass

async def handler(ws):
    name = None
    room = None
    dm_target = None

    try:
        async for raw in ws:
            d = json.loads(raw)

            if d["type"] == "login":
                name = d["name"]
                users[name] = ws
                await ws.send(json.dumps({"type": "ok"}))

            elif d["type"] == "join":
                room = d["room"]
                dm_target = None 
                rooms.setdefault(room, [])
                if name not in rooms[room]:
                    rooms[room].append(name)

                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("SELECT sender, text, timestamp FROM messages WHERE chat_id = ? ORDER BY id", (f"room_{room}",))
                history = [{"type": "msg", "from": row[0], "text": row[1], "time": row[2]} for row in c.fetchall()]
                conn.close()

                await ws.send(json.dumps({"type": "joined", "room": room, "members": rooms[room], "history": history}))
                await broadcast([n for n in rooms[room] if n != name],
                                {"type": "system", "text": f"{name} joined #{room}"})

            elif d["type"] == "msg":
                t = datetime.now().strftime("%H:%M")
                msg = {"type": "msg", "from": name, "text": d["text"], "time": t}
                
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("INSERT INTO messages (chat_id, sender, text, timestamp) VALUES (?, ?, ?, ?)",
                          (f"room_{room}", name, d["text"], t))
                conn.commit()
                conn.close()

                await broadcast(rooms.get(room, []), msg)

            elif d["type"] == "dm":
                t = datetime.now().strftime("%H:%M")
                dm_target = d["to"]
                room = None
                p = {"type": "dm", "from": name, "to": dm_target, "text": d["text"], "time": t}

                chat_id = "_".join(sorted(["dm", name, dm_target]))
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("INSERT INTO messages (chat_id, sender, text, timestamp) VALUES (?, ?, ?, ?)",
                          (chat_id, name, d["text"], t))
                conn.commit()
                conn.close()
                
                await broadcast([dm_target, name], p)

            elif d["type"] == "typing":
                if d.get("mode") == "room" and room:
                    await broadcast([n for n in rooms.get(room, []) if n != name],
                                    {"type": "typing", "from": name, "active": d["active"]})
                elif d.get("mode") == "dm":
                    await broadcast([d["to"]], {"type": "typing", "from": name, "active": d["active"]})

            elif d["type"] == "who":
                await ws.send(json.dumps({"type": "who", "users": list(users.keys())}))
            
            elif d["type"] == "load_dm":
                dm_target = d["with"]
                room = None
                chat_id = "_".join(sorted(["dm", name, dm_target]))
                
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("SELECT sender, text, timestamp FROM messages WHERE chat_id = ? ORDER BY id", (chat_id,))
                history = [{"type": "dm", "from": row[0], "to": dm_target if row[0] == name else name, "text": row[1], "time": row[2]} for row in c.fetchall()]
                conn.close()
                
                await ws.send(json.dumps({"type": "history", "history": history}))

    except:
        pass
    finally:
        if name:
            users.pop(name, None)
        if room and room in rooms and name in rooms[room]:
            rooms[room].remove(name)

async def main():
    init_db()
    print("ws://localhost:8765")
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

asyncio.run(main())