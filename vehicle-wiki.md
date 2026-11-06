# Autonomous & AI-Powered Smart Vehicle (K6)

A private educational robotics project featuring a distributed, multi-controller architecture powered by Raspberry Pi hardware, local edge AI, open-source voice control, and a dedicated local wireless infrastructure.

## 📌 System Architecture & Network Topology

The system is deployed across **three Raspberry Pi controllers** communicating over a dedicated local network, utilizing containerized **Docker** environments for complete modularity and functional separation:

- **Local WLAN Infrastructure:** Managed by a dedicated Raspberry Pi 4 router providing an isolated wireless network for all onboard nodes.

- **Inter-Node Communication:** RESTful HTTP interfaces enabling seamless telemetry exchange and remote display control between controllers.

- **Core Language & Control:** **Python 3** primary application logic, custom HTML/JS web control panels, and teleoperation via an **8BitDo Pro 2 Bluetooth Gamepad**.

## 🛠 Controller System Specs

### 📡 1. `PI4-Router` (Network Infrastructure & Telemetry Display)

Acts as the backbone of the mobile network and provides direct visual feedback for system status.

- **Network Role:** Dedicated local WLAN access point / router.

- **Display Hardware:** Waveshare 1.27-inch RGB OLED Module (SSD1351).

- **Display Interface:** Flask-based HTTP web service allowing `PI5-Vehicle` and `PI5-AI` to push real-time system telemetry and status messages directly to the OLED screen.

### 🚗 2. `PI5-Vehicle` (Drivetrain & Sensor Fusion)

Handles physical motion control, proximity sensing, dynamic indicators, remote gamepad input, and autonomous navigation subroutines.

- **Drivetrain & Motors:** Two stepper motors for driving and differential steering.

- **Servo Controller:** Waveshare Servo Driver HAT.

- **Obstacle Detection:** 3× HC-SR04 Ultrasonic Ranging Modules.

- **IMU Sensing:** Pimoroni ICM20948 (9-DoF Motion Sensor).

- **Visual Telemetry & Status:** Pimoroni LED SHIM display.

- **Control Input:** Integrated Bluetooth driver for 8BitDo Pro 2 Gamepad support.

### 🧠 3. `PI5-AI` (Vision, Voice & Edge Inference)

Dedicated to real-time AI perception, natural language voice control, and pan-tilt camera tracking.

- **Edge AI Accelerator:** Raspberry Pi AI Kit (Hailo-8 AI HAT+, 26 TOPS NPU).

- **Camera Module:** Raspberry Camera Module 3 mounted on a custom 2-axis micro stepper motor pan-tilt assembly (horizontal/vertical movement).

- **Computer Vision:** Hailo Application Framework configured for active human face detection, tracking, and video stream web serving.

- **Voice Control:** **OpenVoiceOS (OVOS)** framework for offline voice command processing, paired with local TTS audio output to an onboard speaker.

## 📦 Core Framework Dependencies

- **[OpenVoiceOS (OVOS)](https://openvoiceos.org/):** Open-source, privacy-focused voice assistant framework for offline command recognition and speech synthesis.

- **[Hailo AI Software Suite](https://hailo.ai/):** High-performance neural network execution and vision pipeline processing on the 26 TOPS Hailo-8 platform.

- **Flask & Requests:** Lightweight HTTP server and client libraries powering the OLED telemetry API and inter-Pi communication.

- **Docker & Docker Compose:** Microservice container management across all network nodes.

  


| **Pin** | **Signal / Name** | **Connected Device** | **Function / Notes** |
| - | - | - | - |
| **01 / 17** | 3.3V Power | ICM20948 / LED SHIM | Logic power rail |
| **02 / 04** | 5V Power | Ultrasonic Sensors / HAT logic | 5V Power supply rail |
| **06 / 09 / 14** | Ground (GND) | All Peripherals | Common system ground |
| **03** | GPIO 2 (SDA1) | Waveshare HAT & ICM20948 | I2C Data line |
| **05** | GPIO 3 (SCL1) | Waveshare HAT & ICM20948 | I2C Clock line |
| **11** | GPIO 17 | Ultrasonic 1 (Front) | Trigger pin (***`HC-SR04 \#1`**) |
| **13** | GPIO 27 | Ultrasonic 1 (Front) | Echo pin (***`HC-SR04 \#1`** via level shifter) |
| **15** | GPIO 22 | Ultrasonic 2 (Left) | Trigger pin (***`HC-SR04 \#2`**) |
| **16** | GPIO 23 | Ultrasonic 2 (Left) | Echo pin (***`HC-SR04 \#2`** via level shifter) |
| **18** | GPIO 24 | Ultrasonic 3 (Right) | Trigger pin (***`HC-SR04 \#3`**) |
| **22** | GPIO 25 | Ultrasonic 3 (Right) | Echo pin (***`HC-SR04 \#3`** via level shifter) |
| **19 / 23** | SPI MOSI / SCLK | Pimoroni LED SHIM | Data & Clock for status LEDs |
| **32 / 33** | GPIO 12 / 13 | Stepper Driver / PWM | Auxiliary PWM motor control / step signals |

-   


| **Interface / Slot** | **Target Component** | **Protocol / Connection Type** | **Notes** |
| - | - | - | - |
| **PCIe M.2 Slot (HAT+)** | Raspberry Pi AI Kit (Hailo-8 NPU) | PCIe Gen 2 x1 | Dedicated 26 TOPS edge neural accelerator |
| **MIPI CSI Camera Port 0** | Raspberry Camera Module 3 | 22-lane FPC Camera Cable | High-resolution live video stream input |
| **GPIO / PWM Header** | Pan-Tilt Micro Steppers (X/Y Axis) | Direct GPIO / PWM Driver Lines | Horizontal and vertical camera tracking actuation |
| **USB / Bluetooth / Audio** | Onboard Speaker & Gamepad / OVOS | USB Audio & BlueZ Stack | Local speech output and Bluetooth telemetry link |

  
  
  


  
  
  
  
  

