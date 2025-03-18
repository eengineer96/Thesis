# Final Thesis - Anomaly Detection for 3D Printing

This repository contains the source code for my final thesis at **Eszterházy Károly Katolikus Egyetem (2025)**. The project focuses on developing an **anomaly detection system** for my **Duet-based 3D printer**, leveraging **machine learning** and **monitoring**.

## Hardware Components
- **[Raspberry Pi 5 (8GB)](https://www.raspberrypi.com/products/raspberry-pi-5/)**
- **[Raspberry Pi Global Shutter Camera](https://www.raspberrypi.com/products/raspberry-pi-global-shutter-camera/)**
- **[Raspberry Pi 6mm Wide Angle Lens](https://www.farnell.com/datasheets/2938678.pdf)**
- **[Raspberry Pi FPC cable 500mm](https://de.farnell.com/en-DE/raspberry-pi/sc1133/fpc-display-cable-500mm-board/dp/4263056?srsltid=AfmBOopYKgs9dnkdSJHzSfG0Sp96POj_ydQVLsTb0c8EOCIxDOjlirTP)**
- **[Custom 3D-Printed Camera Mount](https://www.printables.com/model/994047-rpi-gshq-camera-mount-on-3030-extrusion)** (designed to be mounted on a **3030 extrusion**)

## Key Features
- **Anomaly detection** using a trained neural network.
- **Live video feed processing** via `Picamera2`.
- **Automated notifications and commands** through a Telegram bot.
- **CustomTkinter-based GUI** for user interaction.
- **Optimized for Raspberry Pi 5** running Linux.

## Important Considerations
- **RPi Camera Dependency**: The software **only** supports **Raspberry Pi cameras**.
- **Linux Requirement**: `libcamera2` is **Linux-only** and must be installed **system-wide** (not in a virtual environment).
- **No Model or Dataset Included**: The **trained model** and **dataset** are **not available** in this repository.
- **No Environment Variables Included**: You must configure your own environment variables.
- **Telegram Bot Required**: You'll need to create your own bot using [BotFather](https://core.telegram.org/bots#botfather), obtain its **bot token**, and use your **chat ID**.

## Disclaimer
I am **not responsible** for any **damages** resulting from the use of this code. Use at your own risk.

---
Feel free to reach out if you have any questions! 
