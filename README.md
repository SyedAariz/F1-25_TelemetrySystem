# 🏎️ F1-25_TelemetrySystem

This Python application listens for **UDP telemetry packets from F1 25** and displays the data on a **live Grafana dashboard** (real-time charts for things like speed, throttle, brake, RPM, etc.).

*** VIDEO ***

---

## ✅ Pre-Requisites

### 🎮 F1 25 Game
The whole point of this project is to collect the UDP packets that F1 25 sends through the in-game telemetry settings.

> You *can* tweak the packet formats to support older F1 games too.

### 📊 Grafana
Grafana is an open-source platform for real-time dashboards and visual analysis.

I recommend this tutorial for setting up Grafana:
https://www.youtube.com/watch?v=QGG_76OmRnA&pp=ygUTZ3JhZmFuYSBpbmZsdXhkYiBmMQ%3D%3D

> **Important:** That video includes **InfluxDB**, but **InfluxDB is NOT required** for this project — ignore the InfluxDB steps.

---

## ⚙️ Game Settings (F1 25 Telemetry)

The idea is simple:
- Your **game** sends UDP packets
- Your **computer** receives them and parses them

You need to set the game UDP settings to your **local device IP address**.

<img width="1141" height="377" alt="image" src="https://github.com/user-attachments/assets/2fbaa038-4d5c-4e7d-9720-0b1ec4e20ddb" />

### Recommended Settings
- ✅ **Disable UDP Broadcast Mode**  
  (So packets don’t get sent to every device on your network)
- ✅ **Set UDP IP Address to your device IP**  
- ✅ **Keep UDP Port as `20777`**  
- ✅ **UDP Send Rate: 20Hz recommended**  
  (Feels much more “live” on Grafana with less delay)
- ✅ **Telemetry: Restricted** *(optional)*  
  (Use this if you don’t want anyone else accessing telemetry)

---

## 📍 How to Find Your Local IP Address

### Mac
```bash
ipconfig getifaddr en0
Windows
ipconfig
Use your IPv4 address (usually something like 192.168.x.x) in the game’s UDP IP Address field.
🧩 Installation
Assuming you already have Grafana running:
Requirements
Python >= 3.12
Install
pipx install f1-25_telemetry.py
🔐 Grafana API Token Setup (Required for Dashboard Updates)
If you want the telemetry to appear on your Grafana dashboard, you’ll need to configure:
Your Grafana localhost URL
Your Grafana API token
This screenshot shows the setup that’s required:
<img width="575" height="202" alt="Screenshot 2026-01-12 at 7 24 18 PM" src="https://github.com/user-attachments/assets/1a26d919-2d54-4df5-95e9-7e9ebfdada1d" />
The video tutorial above walks through generating a token — after that you just paste your localhost and API token into the code.

<img width="709" height="232" alt="Screenshot 2026-01-12 at 7 28 39 PM" src="https://github.com/user-attachments/assets/976ea789-dbee-4845-bbf6-b60e5c143e20" />
🧠 Understanding the UDP Header Format
The UDP packets from F1 25 always start with a header.
That header tells you important things like:

which packet type it is (packetId)
session time
frame number
player car index
etc.
In the F1 documentation, the header is defined in C++ like this:
<img width="895" height="439" alt="Screenshot 2026-01-12 at 7 32 37 PM" src="https://github.com/user-attachments/assets/17e3594c-50e2-47b8-b591-35ae2c1dbfa7" />
But in Python, we parse it using struct format strings.

🔄 C++ → Python Struct Cheat Sheet
Here’s the conversion you’ll use when translating packet structs from the official docs into Python:
uint8   → B
int8    → b
uint16  → H
int16   → h
uint32  → I
int32   → i
uint64  → Q
int64   → q
float   → f
char[N] → Ns
➕ Adding New Packets / Expanding Telemetry
If you want to add a new packet from the documentation (or expand existing ones), use this approach:
<img width="742" height="403" alt="Screenshot 2026-01-12 at 7 37 15 PM" src="https://github.com/user-attachments/assets/33b372d8-e23e-4b91-bc7e-9368e1f96539" />
⚠️ Important Rule:
When defining packet formats, include every field from the official struct, even if you don’t use it.

If you skip fields, Python will read the wrong bytes and everything after that will become corrupted.

🧾 Packet IDs (Packet Categories)
Packet IDs tell you what type of packet you received (lap data, telemetry, motion, etc.).
These are the packet categories you’ll use to route parsing logic:
<img width="677" height="598" alt="Screenshot 2026-01-12 at 7 39 26 PM" src="https://github.com/user-attachments/assets/bbe2bd7e-210b-40e7-89ce-de9015b755b0" />
✅ Notes / Best Practices
Keep UDP send rate around 20Hz for the best “live” feel
Keep the port at 20777
Make sure your game IP matches your computer IP exactly
If telemetry looks wrong, it’s usually caused by:
wrong struct format
missing fields in a packet
wrong packet version
