# F1-25_TelemetrySystem

This Python application uses UDP packets to collect data from F1 25 and display it on a live dashboard through Grafana

*** VIDEO ***


# Pre - Requisites:

- F1 25 Game: The whole idea is to collect UDP packets from the telemetry setting on the game.
  (You can tweak the code if you want to make it work in the past F1 games.)
  
- Grafana: It is an open-sourced platform that shows real-time data visualization for analysis.
  I highly recommend watching this video https://www.youtube.com/watch?v=QGG_76OmRnA&pp=ygUTZ3JhZmFuYSBpbmZsdXhkYiBmMQ%3D%3D to setup your Grafana. It also goes through influxDB which is a database where you are able to store your data that is displaying on Grafana. (INFLUXDB IS NOT REQUIRED SO IGNORE ITS STEPS)


# Game Setting:

The idea is to connect the game IP address to the Local IP where were typing the code.

<img width="1141" height="377" alt="image" src="https://github.com/user-attachments/assets/2fbaa038-4d5c-4e7d-9720-0b1ec4e20ddb" />

- Disable UDP Broadcast Mode since we dont our packets to transmit to all the local devices.
- Write your own UDP IP Address, the device IP.
To figure out your Local IP
  Mac - ipconfig getifaddr en0
  Windows - ipconfig
  
- The UDP Port SHOULD stay "20777". The reason for it is because our IP is going to be accessing games IP, its not the opposite.
- UDP Send Rate is recommended to 20Hz since it reduces delay on the Grafana real-time dash.
- Keep the telemetry Restricted if you don't want anyone accessing it.


# Installation

Assuming you have Grafana properly working.


Python >= 3.12

pipx install f1-25_telemetry.py


<img width="575" height="202" alt="Screenshot 2026-01-12 at 7 24 18 PM" src="https://github.com/user-attachments/assets/1a26d919-2d54-4df5-95e9-7e9ebfdada1d" />
This is required if you want to display your telemetry on the dash. That video will show you everything and you just have to paste your localhost and API token.

<img width="709" height="232" alt="Screenshot 2026-01-12 at 7 28 39 PM" src="https://github.com/user-attachments/assets/976ea789-dbee-4845-bbf6-b60e5c143e20" />

- The header format is basically defining how to read UDP packets from the F1 25 game throught its appropriate Python format.

- In the documentation, its written in C++ like this <img width="895" height="439" alt="Screenshot 2026-01-12 at 7 32 37 PM" src="https://github.com/user-attachments/assets/17e3594c-50e2-47b8-b591-35ae2c1dbfa7" /> but we want it in python.



