# Pico - A Offline Desktop Voice Assistant
Pico is a local, voice activated desktop robot built on a **Raspberry Pi 5 (4gb RAM)**.
It listens for a wakeword "Pico" to wakeup (using a custom wakeword model), processes speech, generates response using local llm or uses a skill attribute.

![Preview](assets/pico_cad.gif)

## Tech Stack
![Python](https://img.shields.io/badge/Python-3.13.5-blue?logo=python)
![C++](https://img.shields.io/badge/C++-Firmware-blue?logo=c%2B%2B)
![Arduino](https://img.shields.io/badge/Arduino-Embedded-teal?logo=arduino)
![PyTorch](https://img.shields.io/badge/PyTorch-DeepLearning-ee4c2c?logo=pytorch&logoColor=white)
![TorchAudio](https://img.shields.io/badge/TorchAudio-AudioProcessing-ee4c2c)
![ONNX](https://img.shields.io/badge/ONNX-Runtime-005ced?logo=onnx)
![WakeWord](https://img.shields.io/badge/WakeWord-CustomModel-purple)
![Ollama](https://img.shields.io/badge/Ollama-LocalLLM-black)
![SpeechToText](https://img.shields.io/badge/STT-Sherpa--ONNX-green)
![TextToSpeech](https://img.shields.io/badge/TTS-Piper-green)
![RaspberryPi](https://img.shields.io/badge/RaspberryPi-5-a22846?logo=raspberrypi)
![Servos](https://img.shields.io/badge/MG90S-Servos-red)
![UART](https://img.shields.io/badge/UART-Serial-blue)
![3DPrinting](https://img.shields.io/badge/3DPrinted-Chassis-lightgrey)
![PlatformIO](https://img.shields.io/badge/PlatformIO-EmbeddedIDE-orange?logo=platformio)
![Git](https://img.shields.io/badge/Git-VersionControl-f05032?logo=git&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Pi%20OS-yellow?logo=linux)

## Overview
Pico was built as a personal embedded system to help out on my desk. Wanted to make a more personal version of amazon's echo dot. Pico has real time audio processing and runs fully offline (other than weather api).

Pico was designed to be:
- Private
- Custom
- Fast
- Extendable

I think it's cool that I can ssh into Pico and easily add new features to my modular code.

Pico initially had the ability to spin using a bridge to an arduino uno r3 (accessing a mg90s servo), but when putting the final assembly together, the servo could not handle the weight.

## Features
- Custom wakeword model (PyTorch/Torchaudio) ("Pico")
- STT (Sherpa-ONNX)
- TTS (Piper)
- Conversation loop:
  - Wake
  - Local LLM (Ollama qwen2.5:0.5b) or skill response
  - Sleep
- JSON memory for local llm
- Skills:
  - Date & time
  - Jokes
  - System stats (RAM usage, CPU temp)
  - Random Bible verse
  - Weather
- Screen to display awake or sleep status, user input, and pico's response

## Hardware
- Raspberry Pi 5
- USB Microphone
- USB Speaker
- Small display screen
- USBC Power
- 3D printed body

## Wakeword model
https://github.com/colepuls/wakeword

## Demo
https://www.youtube.com/shorts/hfEGZxP2cPM

## What I learned
- Real time audio pipelines
- Embedded Linux Development
- Multithreading & hardware limitations with it

---

##### MIT License | © Cole Puls
