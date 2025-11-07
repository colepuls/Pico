# Pico - Desktop Robot Assistant

Pico is a locally running, voice-activated desktop robot built on a **Raspberry Pi 5 (4gb RAM)**.
It listens for a wakeword "Pico" to wakeup, processes speech, generates response using local llm or uses a skill attribute.

---

## Tech Stack and Libs

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="60" />
  <img src="https://flask.palletsprojects.com/en/3.0.x/_images/flask-logo.png" width="80" />
  <img src="https://pytorch.org/assets/images/pytorch-logo.png" width="90" />
  <img src="https://raw.githubusercontent.com/pytorch/audio/main/docs/source/_static/img/torchaudio_logo.png" width="90" />
  <img src="https://avatars.githubusercontent.com/u/15389229?s=200&v=4" width="60" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/3a/OpenAI_Logo.svg" width="100" />
  <img src="https://avatars.githubusercontent.com/u/57054066?s=200&v=4" width="60" />
  <img src="https://avatars.githubusercontent.com/u/51221248?s=200&v=4" width="60" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/31/Raspberry_Pi_Logo.svg" width="70" />
</p>

**Core Technologies**
- **Python 3.11** - Main language for entire robot
- **PyTorch / Torchaudio** - Wakeword RNN
- **OpenAI GPT-4o-Transcribe** - Speech-to-text model, used becasue of Pi's hardware limitations
- **Piper** - Local text-to-speech model
- **Gpiozero** - Servo motor control
- **Picamera2** - Video feed
- **Ollama Qwen** - Local LLM
- **Flask** - Web server

---

## Overview

Pico combines **embedded robotics**, **speech processing**, and **reasoning** into one desktop robot.

---

## Wakeword model

Repository to wakeword model: https://github.com/colepuls/wakeword

##### Made by Cole Puls
