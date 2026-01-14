import socket
import struct
import requests
import threading
import pandas as pd
import time
from datetime import datetime



GRAFANA_URL = "http://localhost:XXXX"
GRAFANA_API_KEY = "XXXXXXXXXXXXXX"
LIVE_STREAM = "f1-25_telemetry" # Whatever you want to call your stream

grafana_headers = {
    "Authorization": f"Bearer {GRAFANA_API_KEY}",
    "Content-Type": "text/plain",
}






# === UDP setup ===
UDP_IP = "0.0.0.0" # This listens on all interfaces
UDP_PORT = 20777 # This should be default in the game settings
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # This is a connection based protocol
sock.bind((UDP_IP, UDP_PORT))
print(f"✅ Listening for F1 25 packets on port {UDP_PORT}...")

# === Struct formats from official F1 25 spec ===
HEADER_FORMAT = "<H5BQfIIBB"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)




CAR_TELEMETRY_DATA = (
    "<"
    "H"      # m_speed; //Speed of car in kilometres per hour
    "f"      # m_throttle; // Amount of throttle applied (0.0 to 1.0)
    "f"      # m_steer; // Steering (-1.0 (full lock left) to 1.0 (full lock right))
    "f"      # m_brake; // Amount of brake applied (0.0 to 1.0)
    "B"      # m_clutch; // Amount of clutch applied (0 to 100)
    "b"      # m_gear;  // Gear selected (1-8, N=0, R=-1)
    "H"      # m_engineRPM; // Engine RPM
    "B"      # m_drs; // 0 = off, 1 = on
    "B"      # m_revLightsPercent; // Rev lights indicator (percentage)
    "H"      # m_revLightsBitValue; // Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
    "4H"     # m_brakesTemperature[4]; // Brakes temperature (celsius)
    "4B"     # m_tyresSurfaceTemperature[4]; // Tyres surface temperature (celsius)
    "4B"     # m_tyresInnerTemperature[4]; // Tyres inner temperature (celsius)
    "H"      # m_engineTemperature; // Engine temperature (celsius)
    "4f"     # m_tyresPressure[4]; // Tyres pressure (PSI)
    "4B"     # m_surfaceType[4];  // Driving surface, see appendices 
    
)

CAR_DAMAGE_DATA = (
    "<"
    "4f"     # m_tyresWear[4]; // Tyre wear (percentage)
    "4B"     # m_tyresDamage[4]; // Tyre damage (percentage)
    "4B"     # m_brakesDamage[4]; // Brakes damage (percentage)
    "4B"     # m_tyreBlisters[4]; // Tyre blisters value (percentage)
    "B"      # m_frontLeftWingDamage; // Front left wing damage (percentage)
    "B"      # m_frontRightWingDamage; // Front right wing damage (percentage)
    "B"      # m_rearWingDamage; // Rear wing damage (percentage)
    "B"      # m_floorDamage; // Floor damage (percentage)
    "B"      # m_diffuserDamage; // Diffuser damage (percentage)
    "B"      # m_sidepodDamage; // Sidepod damage (percentage)
    "B"      # m_drsFault; // Indicator for DRS fault, 0 = OK, 1 = fault
    "B"      # m_ersFault; // Indicator for ERS fault, 0 = OK, 1 = fault
    "B"      # m_gearBoxDamage; // Gear box damage (percentage)
    "B"      # m_engineDamage; // Engine damage (percentage)
    "B"      # m_engineMGUHWear; // Engine wear MGU-H (percentage)
    "B"      # m_engineESWear; // Engine wear ES (percentage)
    "B"      # m_engineCEWear; // Engine wear CE (percentage)
    "B"      # m_engineICEWear; // Engine wear ICE (percentage)
    "B"      # m_engineMGUKWear; // Engine wear MGU-K (percentage)
    "B"      # m_engineTCWear; // Engine wear TC (percentage)
    "B"      # m_engineBlown; // Engine blown, 0 = OK, 1 = fault
    "B"      # m_engineSeized; // Engine seized, 0 = OK, 1 = fault
)

CAR_LAP_DATA = (
    "<"
    "I"    # m_lastLapTimeInMS
    "I"    # m_currentLapTimeInMS
    "H"    # m_sector1TimeMSPart
    "B"    # m_sector1TimeMinutesPart
    "H"    # m_sector2TimeMSPart
    "B"    # m_sector2TimeMinutesPart
    "H"    # m_deltaToCarInFrontMSPart
    "B"    # m_deltaToCarInFrontMinutesPart
    "H"    # m_deltaToRaceLeaderMSPart
    "B"    # m_deltaToRaceLeaderMinutesPart
    "f"    # m_lapDistance
    "f"    # m_totalDistance
    "f"    # m_safetyCarDelta
    "B"    # m_carPosition
    "B"    # m_currentLapNum
    "B"    # m_pitStatus
    "B"    # m_numPitStops
    "B"    # m_sector
    "B"    # m_currentLapInvalid
    "B"    # m_penalties
    "B"    # m_totalWarnings
    "B"    # m_cornerCuttingWarnings
    "B"    # m_numUnservedDriveThroughPens
    "B"    # m_numUnservedStopGoPens
    "B"    # m_gridPosition
    "B"    # m_driverStatus
    "B"    # m_resultStatus
    "B"    # m_pitLaneTimerActive
    "H"    # m_pitLaneTimeInLaneInMS
    "H"    # m_pitStopTimerInMS
    "B"    # m_pitStopShouldServePen
    "f"    # m_speedTrapFastestSpeed
    "B"    # m_speedTrapFastestLap
)


CAR_TELEMETRY_SIZE = struct.calcsize(CAR_TELEMETRY_DATA)
CAR_DAMAGE_SIZE = struct.calcsize(CAR_DAMAGE_DATA)
CAR_LAP_SIZE = struct.calcsize(CAR_LAP_DATA)



latest_telemetry_data = {} # Creating a list
latest_damage_data = {}
latest_lap_data = {}
collecting = False
running = True
lock = threading.Lock() # Prevents two features from touching the same data



def telemetry_listener():
    global latest_data, collecting, latest_data2
    while running:
        try:
            data, addr = sock.recvfrom(2048)
        except OSError:
            break
        if not collecting:
            continue
        packet_id = data[6]
    
        print(f" From {addr} | Packet ID: {packet_id} | Size: {len(data)} bytes")

        if packet_id == 6:
            player_index = data[27]
            start = HEADER_SIZE + player_index * CAR_TELEMETRY_SIZE
            end = start + CAR_TELEMETRY_SIZE
            car = struct.unpack(CAR_TELEMETRY_DATA, data[start:end])
            

            # Extract relevant fields from CAR_TELEMETRY_DATA 
            tyres_inner_temp = list(car[18:22])
            tyres_pressure = list(car[23:27])
            
            latest_telemetry_data = {
                "m_speed": car[0],
                "m_throttle": round(car[1] * 100, 0),
                "m_brake": round(car[3] * 100, 0),
                "m_steer": car[2],
                "m_gear": car[5],
                "m_rpm": car[6],
                "m_engineTemperature" : car[13],
                "tyres_inner_temp": tyres_inner_temp,
                "tyres_pressure": tyres_pressure
            }

    
            # ---- Grafana Live push (true streaming) ----
            # We use Grafana Live features to push real-time data
            line = (
                f"f1_live,driver=player "
                f"m_speed={car[0]},"
                f"m_rpm={car[6]},"
                f"m_throttle={round(car[1] * 100, 0)},"
                f"m_brake={round(car[3] * 100, 0)},"
                f"m_gear={car[5]},"
                f"m_engineTemperature={car[13]},"
                f"tyre_rl={tyres_pressure[0]},"
                f"tyre_rr={tyres_pressure[1]},"
                f"tyre_fl={tyres_pressure[2]},"
                f"tyre_fr={tyres_pressure[3]},"
                f"tyre_temp_rl={tyres_inner_temp[0]},"
                f"tyre_temp_rr={tyres_inner_temp[1]},"
                f"tyre_temp_fl={tyres_inner_temp[2]},"
                f"tyre_temp_fr={tyres_inner_temp[3]}"

                
            )

            try:
                requests.post(
                    f"{GRAFANA_URL}/api/live/push/{LIVE_STREAM}",
                    headers=grafana_headers,
                    data=line,
                    timeout=0.05,
                )
            except requests.exceptions.RequestException:
                pass  # never block telemetry

        if packet_id == 10:
            player_index = data[27]
            start = HEADER_SIZE + player_index * CAR_DAMAGE_SIZE
            end = start + CAR_DAMAGE_SIZE
            car = struct.unpack(CAR_DAMAGE_DATA, data[start:end])

            tyre_wear = list(car[0:4])

            latest_damage_data = {
                "tyre_wear": tyre_wear
            }

            # ---- Grafana Live push (true streaming) ----
            line_2 = (
                f"f1_damage,driver=player "
                f"tyre_wear_rl={tyre_wear[0]},"
                f"tyre_wear_rr={tyre_wear[1]},"
                f"tyre_wear_fl={tyre_wear[2]},"
                f"tyre_wear_fr={tyre_wear[3]}"
            )
            try:
                requests.post(
                    f"{GRAFANA_URL}/api/live/push/{LIVE_STREAM}",
                    headers=grafana_headers,
                    data=line_2,
                    timeout=0.05,
                )
            except requests.exceptions.RequestException:
                pass  # never block telemetry
        if packet_id == 2:
            player_index = data[27]
            start = HEADER_SIZE + player_index * CAR_LAP_SIZE
            end = start + CAR_LAP_SIZE
            car = struct.unpack(CAR_LAP_DATA, data[start:end])

            
            

            latest_lap_data = {
                "m_deltaToCarInFrontMSPart": car[6],
                "m_deltaToRaceLeaderMSPart": car[8]
            }

            # ---- Grafana Live push (true streaming) ----
            line_2 = (
                f"f1_lap,driver=player "
                f"m_deltaToCarInFrontMSPart={car[6]},"
                f"m_deltaToRaceLeaderMSPart={car[8]}"
            )
            try:
                requests.post(
                    f"{GRAFANA_URL}/api/live/push/{LIVE_STREAM}",
                    headers=grafana_headers,
                    data=line_2,
                    timeout=0.05,
                )
            except requests.exceptions.RequestException:
                pass  # never block telemetry






def telem_control():
    global collecting, running, sock

    time.sleep(1.5)

    while True:

        print("1 - start", )
        print("2 - stop", )
        print("3 - quit")

        choice = int(input())

        if choice == 1:
            print("Starting telemetry listener...")
            collecting = True
        elif choice == 2:
            print("Stopping telemetry listener...")
            collecting = False
        elif choice == 3:
            collecting = False
            running = False
            sock.close()
            print("quitting..")
            exit()
        else:
            print("invalid choice")


if __name__ == "__main__":
    threading.Thread(target=telemetry_listener, daemon=True).start()
    telem_control()
