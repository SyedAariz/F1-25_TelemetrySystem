# F1-25_TelemetrySystem

This Python application listens for **UDP telemetry packets from F1 25** and displays the data on a **live Grafana dashboard** (real-time charts for things like speed, throttle, brake, RPM, etc.).

<p align="center">
  <a href="https://www.youtube.com/watch?v=SUn1JK6MtBw">
    <img src="https://img.youtube.com/vi/SUn1JK6MtBw/maxresdefault.jpg" width="900" />
  </a>
</p>
<p align="center"><b>▶ Click to watch the F1 25 Telemetry Demo</b></p>


<img width="1434" height="894" alt="Screenshot 2026-01-13 at 11 25 50 PM" src="https://github.com/user-attachments/assets/9d25b218-c3be-44d3-ac39-0588f861f4db" />

This dashboard visualizes real-time vehicle telemetry streamed from the F1 game via UDP and rendered in Grafana. It is designed to give instant insight into driver inputs, vehicle behavior, tyre health, and race context.


## Telemetry Dashboard Metrics

### Speed (km/h)
Purpose: Shows current vehicle speed for baseline performance reference.

### Engine RPM
Purpose: Indicates engine speed to analyze acceleration and shift behavior.

### Brake vs Throttle
Purpose: Displays driver input balance to evaluate driving smoothness.

### Tyre Temperature
Purpose: Monitors tyre temperatures to assess grip and balance.

### Tyre Wear
Purpose: Tracks tyre degradation to predict grip loss and stint length.

### Tyre Pressure
Purpose: Displays tyre pressure to optimize grip and stability.

### Delta to Car in Front
Purpose: Measures time gap to the car ahead for race positioning analysis.

### Delta to Race Leader
Purpose: Provides overall pace comparison against the race leader.

---

## ✅ Pre-Requisites

### F1 25 Game
The whole point of this project is to collect the UDP packets that F1 25 sends through the in-game telemetry settings.

> You *can* tweak the packet formats to support older F1 games too.

### 📊 Grafana
Grafana is an open-source platform for real-time dashboards and visual analysis.

I recommend this tutorial for setting up Grafana:

https://www.youtube.com/watch?v=QGG_76OmRnA&pp=ygUTZ3JhZmFuYSBpbmZsdXhkYiBmMQ%3D%3D

> **Important:** That video includes **InfluxDB**, but **InfluxDB is NOT required** for this project, ignore the InfluxDB steps.

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

-----

## Installation
This project assumes you already have Grafana installed and running correctly.
### Requirements
- Python 3.12 or higher
- Install the telemetry package using:

Clone the repository
```bash
git clone https://github.com/SyedAariz/F1-25_TelemetrySystem.git
cd F1-25_TelemetrySystem
python3 -m venv venv
source venv/bin/activate
python3 -m pip install requests pandas
python3 F1-25_Telemetry.py


```

#### Grafana Setup (Required for Dashboard Visualization)

<img width="575" height="202" alt="Screenshot 2026-01-12 at 7 24 18 PM" src="https://github.com/user-attachments/assets/1a26d919-2d54-4df5-95e9-7e9ebfdada1d" />

*This setup is only required if you want to visualize telemetry data in Grafana.*

The video linked above walks through the entire process step-by-step.
When prompted, simply paste:
- Your localhost URL
- Your Grafana API token
Once configured, telemetry data will stream live to your dashboard.

<img width="709" height="232" alt="Screenshot 2026-01-12 at 7 28 39 PM" src="https://github.com/user-attachments/assets/976ea789-dbee-4845-bbf6-b60e5c143e20" />

#### UDP Packet Header Format
The UDP packet header defines how Python reads and parses telemetry packets sent from the F1 25 game.

The official F1 documentation defines packet structures in C++, but Python requires converting these into a struct-compatible format.

<img width="895" height="439" alt="Screenshot 2026-01-12 at 7 32 37 PM" src="https://github.com/user-attachments/assets/17e3594c-50e2-47b8-b591-35ae2c1dbfa7" />

#### C++ → Python Type Conversion Cheat Sheet

```bash
Use the following mapping when converting packet definitions from C++ to Python’s struct format:
uint8   → B
int8    → b
uint16  → H
int16   → h
uint32  → I
int32   → i
uint64  → Q
int64  → q
float   → f
char[N] → Ns
```

### Creating or Extending Packets

<img width="742" height="403" alt="Screenshot 2026-01-12 at 7 37 15 PM" src="https://github.com/user-attachments/assets/33b372d8-e23e-4b91-bc7e-9368e1f96539" />

If you want to create your own packet from the documentation or extend an existing one:

- Follow the same Python struct format
- Include every variable listed in the documentation, even if you don’t plan to use all of them
- Maintain the correct field order
This ensures the packet stays aligned and is parsed correctly.

#### Packet IDs

These packet IDs determine which telemetry category you are accessing (e.g., Motion, Lap Data, Car Telemetry).

<img width="677" height="598" alt="Screenshot 2026-01-12 at 7 39 26 PM" src="https://github.com/user-attachments/assets/bbe2bd7e-210b-40e7-89ce-de9015b755b0" />

Each packet ID maps to a specific data structure, allowing the application to route and process telemetry data correctly.

HERE IS THE DOCUMENTATION - [Data Output from F1 25 v3.pdf](https://github.com/user-attachments/files/24605758/Data.Output.from.F1.25.v3.pdf)

------

### Grafana Tips
<img width="285" height="61" alt="Screenshot 2026-01-13 at 12 04 52 PM" src="https://github.com/user-attachments/assets/c5ed4ea7-22af-4dcb-8158-4005480189c7" />

- Make sure to enable this data source
- Set panel calculation to “Last” for live values
- Use Stat or Bar Gauge panels for telemetry
- Lock time range to “Last 5 minutes” or less
- Use thresholds for throttle, brake, and RPM
- Play around with panel types and settings to see what looks best for you
- If nothing shows, check your API token, data source, and that the UDP listener is running


