# Mivi Agent

Mivi Agent turns a Raspberry Pi Zero / Zero 2 W into a USB HID keyboard that can be controlled through a web interface or REST API.

The Raspberry Pi connects to a Windows PC through USB and is detected as a normal USB keyboard.

---

# Features

- USB HID Keyboard
- Web UI
- REST API
- Swagger UI
- Automatic startup on boot
- Health endpoint

Future:

- Mouse
- Camera
- WebSockets
- Authentication
- Cloud connectivity
- OTA Updates

---

# Hardware

- Raspberry Pi Zero W / Zero 2 W
- Raspberry Pi OS Lite
- USB Data cable
- Windows PC

> IMPORTANT

Use the USB **DATA** port on the Raspberry Pi.

Do NOT use the PWR IN port.

---

# Clone

```bash
git clone https://github.com/<your-account>/mivi-agent.git

cd mivi-agent
```

---

# Install Python

Create a virtual environment.

```bash
python3 -m venv venv
```

Activate it.

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Raspberry Pi Configuration

Enable USB Gadget Mode.

Edit:

```bash
sudo nano /boot/firmware/config.txt
```

Add

```text
dtoverlay=dwc2
```

Edit

```bash
sudo nano /boot/firmware/cmdline.txt
```

Add

```text
modules-load=dwc2
```

after

```text
rootwait
```

Keep cmdline.txt on a single line.

Reboot.

```bash
sudo reboot
```

---

# Install USB Gadget Script

Copy the script

```text
scripts/usb-keyboard-gadget.sh
```

to

```text
/usr/bin/usb-keyboard-gadget
```

Make executable

```bash
sudo chmod +x /usr/bin/usb-keyboard-gadget
```

---

# Install Systemd Services

Copy

```text
systemd/usb-keyboard-gadget.service
```

to

```text
/etc/systemd/system/
```

Copy

```text
systemd/mivi-agent.service
```

to

```text
/etc/systemd/system/
```

Reload

```bash
sudo systemctl daemon-reload
```

Enable

```bash
sudo systemctl enable usb-keyboard-gadget
sudo systemctl enable mivi-agent
```

---

# Install Udev Rule

Copy

```text
udev/99-hidg.rules
```

to

```text
/etc/udev/rules.d/
```

Reload

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

---

# Run manually

```bash
source venv/bin/activate

uvicorn app.main:app --host 0.0.0.0 --port 8080
```

---

# Open the UI

```
http://PI-IP:8080
```

or

```
http://hostname.local:8080
```

---

# Swagger

```
http://PI-IP:8080/docs
```

---

# Health

```
GET /health
```

---

# REST API

Type text

```
POST /type?text=hello world
```

Commands

```
POST /command/select-all

POST /command/copy

POST /command/paste

POST /command/delete

POST /command/backspace

POST /command/tab

POST /command/enter

POST /command/escape
```

---

# Logs

Follow the API logs

```bash
journalctl -u mivi-agent -f
```

USB Gadget

```bash
journalctl -u usb-keyboard-gadget -f
```

---

# Check Services

```bash
systemctl status mivi-agent
```

```bash
systemctl status usb-keyboard-gadget
```

---

# Current Architecture

```
Browser
      ¦
      ?
 FastAPI
      ¦
      ?
 HID Keyboard
      ¦
      ?
 Windows PC
```

---

# Project Structure

```
mivi-agent/
¦
+-- app/
¦   +-- hid/
¦   +-- services/
¦   +-- static/
¦   +-- templates/
¦   +-- main.py
¦
+-- requirements.txt
+-- README.md
+-- .gitignore
```

---

# Roadmap

- Mouse support
- Full keyboard layout
- Camera streaming
- Authentication
- Device registration
- WebSocket communication
- OTA Updates
- Multi-device management
- Cloud Dashboard