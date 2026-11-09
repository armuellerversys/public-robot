# Autonomous & AI-Powered Smart Vehicle (K6)

A private educational robotics project featuring a distributed multi-controller architecture based on Raspberry Pi hardware.

The vehicle combines:

- Autonomous vehicle control
- Local edge AI inference
- Computer vision and camera tracking
- Offline voice control
- Wireless teleoperation
- Sensor fusion
- A dedicated local wireless network
- Containerized software deployment using Docker

The system is designed as a modular distributed robotics platform where individual functions run on separate Raspberry Pi controllers.

## Project Repository

[GitHub Repository: public-robot](https://github.com/armuellerversys/public-robot?utm_source=chatgpt.com)

---

# 📌 System Architecture

The system consists of three Raspberry Pi controllers connected through an isolated local wireless network.

Each controller has a dedicated responsibility:

| Controller | Primary Responsibility |
|---|---|
| **PI4-Router** | WLAN infrastructure and OLED telemetry display |
| **PI5-Vehicle** | Vehicle movement, sensors, IMU, and gamepad control |
| **PI5-AI** | Computer vision, edge AI inference, camera control, and voice control |

The software is deployed using Docker containers to provide functional separation and modularity.

---

## Network Topology

```text
                   +---------------------------+
                   |     8BitDo Pro 2          |
                   |        Gamepad            |
                   +---------------------------+
                                |
                            Bluetooth
                                |
                                v

+-------------------+     +-------------------+     +-------------------+
|                   |     |                   |     |                   |
|   PI5-Vehicle     |<--->|    PI4-Router     |<--->|      PI5-AI       |
|                   | Wi-Fi                   | Wi-Fi                   |
| - Drivetrain      |     | - WLAN Access     |     | - Hailo NPU       |
| - Sensors         |     |   Point           |     | - Camera           |
| - IMU             |     | - DHCP            |     | - Computer Vision |
| - Gamepad Control |     | - OLED Server     |     | - OVOS Voice      |
|                   |     |                   |     |                   |
+-------------------+     +-------------------+     +-------------------+
                                |
                                | HTTP
                                v
                       +----------------------+
                       | Waveshare 1.27"      |
                       | RGB OLED Display     |
                       | SSD1351              |
                       +----------------------+
```

---

# 📡 1. Wireless Infrastructure — `PI4-Router`

The Raspberry Pi 4 acts as the network backbone of the vehicle.

## Access Point

The Pi 4 is configured as a dedicated wireless access point using:

- `hostapd`
- `dnsmasq`

It provides a private Wi-Fi network for the onboard Raspberry Pi controllers.

## DHCP and IP Addressing

The router provides DHCP services and assigns IP addresses to:

- `PI5-Vehicle`
- `PI5-AI`

Depending on the configuration, nodes may use:

- Static IP addresses
- DHCP reservations
- Dynamic DHCP addresses

## Network Isolation

The dedicated WLAN keeps internal robotics traffic separated from external networks.

The local network is used for:

- Vehicle telemetry
- Inter-controller communication
- Camera streaming
- Voice-control communication
- OLED status updates
- Web-based control interfaces

---

# 🔄 2. Inter-Node Telemetry and Display Pipeline

The controllers communicate using lightweight HTTP-based APIs.

## OLED Telemetry Server

The `PI4-Router` runs a Python Flask application that provides an HTTP endpoint, for example:

```text
POST /api/display
```

The endpoint receives JSON status messages from the other controllers.

## Telemetry Clients

Both `PI5-Vehicle` and `PI5-AI` can send status updates to the OLED server.

Examples include:

- CPU temperature
- Vehicle movement status
- Obstacle warnings
- AI inference status
- Face detection status
- Camera tracking status
- OVOS voice assistant state
- General system messages

Telemetry updates can be sent:

- Periodically
- Event-driven
- When the system state changes

## OLED Rendering

The Pi 4 processes the received JSON payload and updates the attached:

**Waveshare 1.27-inch RGB OLED Display**

using the SSD1351 display controller.

---

# 🎮 3. Client and Control Interfaces

## Web-Based Control Panels

Web interfaces hosted on the Raspberry Pi controllers provide browser-based access to system functions.

Depending on the service, the interfaces can provide:

- Camera video streams
- Vehicle control
- AI status information
- System monitoring

The interfaces are accessible through the private Wi-Fi network provided by `PI4-Router`.

## Gamepad Control

The `PI5-Vehicle` receives input from an **8BitDo Pro 2 Bluetooth Gamepad**.

Linux input events are processed using `evdev`.

Joystick and controller input is translated into vehicle movement commands, which are then converted into motor control signals.

---

# 🛠 Controller Hardware

# 📡 1. `PI4-Router`

**Role:** Network infrastructure and telemetry display

The Raspberry Pi 4 acts as the communication backbone of the vehicle.

### Responsibilities

- Dedicated WLAN access point
- DHCP server
- Local network routing
- OLED telemetry server
- System status display

### Hardware

- Raspberry Pi 4
- Waveshare 1.27-inch RGB OLED Display
- SSD1351 display controller

### Software

- `hostapd`
- `dnsmasq`
- Python
- Flask

---

# 🚗 2. `PI5-Vehicle`

**Role:** Drivetrain, sensors, and vehicle control

The `PI5-Vehicle` controller is responsible for physical movement and sensor processing.

## Drivetrain

- Two stepper motors
- Differential steering
- Autonomous movement routines

## Motor Controller

- Adafruit DC & Stepper Motor HAT

## Obstacle Detection

Three HC-SR04 ultrasonic ranging sensors:

- Front
- Left
- Right

> ⚠️ **Important:** The HC-SR04 Echo output operates at 5 V. A suitable level shifter or voltage divider must be used before connecting the Echo signal to a Raspberry Pi GPIO input.

## IMU

- Pimoroni ICM20948
- 9-DoF motion sensor

The IMU can provide:

- Accelerometer data
- Gyroscope data
- Magnetometer data

## Visual Status Display

- Pimoroni LED SHIM

Used for:

- Status indicators
- System feedback
- Visual warnings

## Control Input

- 8BitDo Pro 2 Bluetooth Gamepad
- Linux Bluetooth stack
- `evdev` input processing

---

# 🧠 3. `PI5-AI`

**Role:** Computer vision, edge AI inference, camera control, and voice interaction.

## Edge AI Accelerator

- Raspberry Pi AI Kit
- Hailo-8 AI accelerator
- Up to 26 TOPS of AI performance

The accelerator is used for local neural network inference.

## Camera

- Raspberry Pi Camera Module 3
- MIPI CSI interface

The camera provides the video input for computer vision and streaming applications.

## Pan-Tilt Camera System

The camera is mounted on a custom two-axis pan-tilt mechanism.

The system provides:

- Horizontal movement
- Vertical movement
- AI-assisted camera tracking

## Servo / Motor Control

- Waveshare Servo Driver HAT

Used for controlling camera movement, depending on the final mechanical implementation.

## Computer Vision

The system uses the Hailo software framework for:

- Object detection
- Face detection
- Human tracking
- Real-time edge inference
- Video streaming

## Voice Control

The vehicle uses **OpenVoiceOS (OVOS)** for local voice interaction.

The voice system supports:

- Speech recognition
- Voice command processing
- Vehicle-specific skills
- Text-to-speech output
- Local speaker playback

---

# 🔌 Hardware Pinout and Bus Connections

# `PI5-Vehicle` GPIO and Bus Mapping

## I²C Interface

**I²C-1**

| Signal | Physical Pin | GPIO |
|---|---:|---:|
| SDA | 3 | GPIO 2 |
| SCL | 5 | GPIO 3 |

Connected devices:

- Pimoroni ICM20948
- Other compatible I²C peripherals

## SPI Interface

| Signal | Physical Pin | GPIO |
|---|---:|---:|
| MOSI | 19 | GPIO 10 |
| SCLK | 23 | GPIO 11 |

Used for compatible SPI peripherals where required.

---

## 40-Pin GPIO Allocation

| Physical Pin | GPIO / Signal | Connected Device | Function |
|---|---|---|---|
| 01 / 17 | 3.3 V | ICM20948 / LED SHIM | Logic power |
| 02 / 04 | 5 V | Ultrasonic sensors / HAT | 5 V power |
| 06 / 09 / 14 | GND | All peripherals | Common ground |
| 03 | GPIO 2 / SDA1 | I²C devices | I²C data |
| 05 | GPIO 3 / SCL1 | I²C devices | I²C clock |
| 11 | GPIO 17 | HC-SR04 Front | Trigger |
| 13 | GPIO 27 | HC-SR04 Front | Echo via level shifter |
| 15 | GPIO 22 | HC-SR04 Left | Trigger |
| 16 | GPIO 23 | HC-SR04 Left | Echo via level shifter |
| 18 | GPIO 24 | HC-SR04 Right | Trigger |
| 22 | GPIO 25 | HC-SR04 Right | Echo via level shifter |
| 19 / 23 | SPI MOSI / SCLK | SPI peripheral | Data / clock |
| 32 / 33 | GPIO 12 / GPIO 13 | Motor control | Auxiliary PWM / control |

> ⚠️ The final GPIO allocation should be kept synchronized with the actual hardware configuration and source code.

---

# 🔌 `PI5-AI` Interfaces

| Interface | Connected Component | Connection Type | Purpose |
|---|---|---|---|
| PCIe M.2 / HAT+ | Raspberry Pi AI Kit | PCIe | Hailo AI acceleration |
| MIPI CSI | Camera Module 3 | CSI camera interface | Video input |
| GPIO / Driver HAT | Pan-Tilt mechanism | GPIO / I²C / PWM | Camera movement |
| USB / Audio | Speaker | USB audio | TTS output |
| Bluetooth | Input devices | BlueZ | Wireless device support |

---

# 📦 Core Software Dependencies

## OpenVoiceOS

[OpenVoiceOS (OVOS)](https://openvoiceos.org/?utm_source=chatgpt.com)

Open-source voice assistant framework used for local speech processing and vehicle-specific voice commands.

## Hailo AI Software

[Hailo AI](https://hailo.ai/?utm_source=chatgpt.com)

Used for local neural network inference and computer vision processing on the Hailo accelerator.

## Flask and Requests

Used for:

- HTTP APIs
- Telemetry communication
- OLED status updates
- Inter-node communication

## Docker and Docker Compose

Used to deploy the software as isolated containerized services.

---

# 📦 System Deployment

The project is divided into separate deployment modules.

Each module contains its own application code and Docker configuration.

## Project Modules

### `hailo_docker_install`

Contains:

- Docker deployment configuration
- Camera capture software
- Hailo AI inference software
- Computer vision functionality
- Camera control

**Deployment target:** `PI5-AI`

---

### `ovos_docker_install`

Contains:

- Docker deployment for OpenVoiceOS
- OVOS service configuration
- Vehicle-specific OVOS skills
- Voice processing
- Local TTS functionality

**Deployment target:** `PI5-AI`

---

### `move_robot_vehicle`

Contains:

- Docker deployment configuration
- Vehicle movement logic
- Motor control
- Sensor processing
- Autonomous movement functionality
- Gamepad integration

**Deployment target:** `PI5-Vehicle`

---

### `oled_server`

Contains:

- WLAN access point configuration
- OLED service deployment
- Flask OLED dashboard server
- OLED display logic

**Deployment target:** `PI4-Router`

---

# 🐳 Docker Deployment

Each module is deployed independently.

## Build and Start a Module

Navigate to the directory containing the corresponding `docker-compose.yml` file:

```bash
cd <module-directory>
```

Build the container images:

```bash
docker compose build
```

Start the services in detached mode:

```bash
docker compose up -d
```

---

## View Container Status

```bash
docker ps
```

View all containers:

```bash
docker ps -a
```

---

## View Container Logs

Example:

```bash
docker logs robot_vehicle_move
```

Follow logs in real time:

```bash
docker logs --follow --tail 200 ovos_audio
```

The same can also be done through Docker Compose:

```bash
docker compose logs -f
```

---

## Stop a Deployment

From the directory containing the `docker-compose.yml` file:

```bash
docker compose down
```

Stop all running containers:

```bash
docker stop $(docker ps -q)
```

---

## Start All Existing Containers

```bash
docker start $(docker ps -a -q)
```

> ⚠️ In normal operation, it is generally preferable to manage the project using `docker compose up` and `docker compose down` rather than manually starting every container on the system.

---

# 🖥 Open a Shell Inside a Container

Open a Bash shell in an already running container:

```bash
docker exec -it ovos_audio bash
```

Alternatively, start a temporary shell using Docker Compose:

```bash
docker compose run --rm --no-deps \
  --entrypoint /bin/bash \
  ovos_audio
```

For the vehicle container:

```bash
docker compose run --rm --no-deps \
  --entrypoint /bin/bash \
  robot_vehicle_move
```

---

# 🧩 Architecture Philosophy

The project follows a distributed robotics architecture.

Each Raspberry Pi controller has a clearly defined responsibility:

```text
PI4-Router
    │
    ├── Wireless Infrastructure
    ├── DHCP
    └── OLED Telemetry

PI5-Vehicle
    │
    ├── Motor Control
    ├── Ultrasonic Sensors
    ├── IMU Processing
    └── Manual / Autonomous Movement

PI5-AI
    │
    ├── Camera
    ├── Hailo AI Inference
    ├── Computer Vision
    ├── Camera Tracking
    └── OVOS Voice Control
```

This separation provides several advantages:

- Clear separation of responsibilities
- Independent Docker deployments
- Easier debugging
- Better maintainability
- Reduced coupling between subsystems
- Independent development of AI and vehicle control functionality
- Easier replacement or extension of individual components

