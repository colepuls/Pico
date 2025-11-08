# Pico - Desktop Robot Assistant

Pico is a locally running, voice-activated desktop robot built on a **Raspberry Pi 5 (4gb RAM)**.
It listens for a wakeword "Pico" to wakeup, processes speech, generates response using local llm or uses a skill attribute.

---

## Tech Stack and Libs

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="60" />
  <img src="https://pytorch.org/assets/images/pytorch-logo.png" width="70" />
  <img src="assets/flask.png" width="60"/>
  <img src="assets/openai.png" width="90"/>
  <img src="assets/ollama.png" width="60"/>
  <img src="assets/piper.png" width="90"/>
  <img src="assets/rasp.png" width="60"/>
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

So far Pico combines **embedded robotics**, **speech processing**, and **reasoning** into one desktop robot.

---

## Wakeword model

Repository to wakeword model: https://github.com/colepuls/wakeword

---

## To do
- [ ] Implement facedetection
- [ ] Add visual display
- [ ] Update motion control
- [ ] Update webserver
- [ ] Some other things ...
- [ ] 3d print chasis and put it all together

---

##### Made by Cole Puls
