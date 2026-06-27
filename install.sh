#!/bin/bash
set -e

APP_NAME="mivi-agent"
INSTALL_DIR="/opt/$APP_NAME"
SERVICE_USER="${SUDO_USER:-$USER}"

echo "Installing $APP_NAME..."

if [ "$EUID" -ne 0 ]; then
  echo "Please run with sudo:"
  echo "sudo ./install.sh"
  exit 1
fi

echo "Using service user: $SERVICE_USER"

apt update
apt install -y python3 python3-venv python3-pip git

mkdir -p "$INSTALL_DIR"

rsync -a \
  --exclude "venv" \
  --exclude ".git" \
  --exclude "__pycache__" \
  ./ "$INSTALL_DIR/"

chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"

python3 -m venv "$INSTALL_DIR/venv"

sudo -u "$SERVICE_USER" "$INSTALL_DIR/venv/bin/pip" install --upgrade pip
sudo -u "$SERVICE_USER" "$INSTALL_DIR/venv/bin/pip" install -r "$INSTALL_DIR/requirements.txt"

cp "$INSTALL_DIR/scripts/usb-keyboard-gadget.sh" /usr/bin/usb-keyboard-gadget
chmod +x /usr/bin/usb-keyboard-gadget

cp "$INSTALL_DIR/systemd/usb-keyboard-gadget.service" /etc/systemd/system/usb-keyboard-gadget.service
cp "$INSTALL_DIR/systemd/mivi-agent.service" /etc/systemd/system/mivi-agent.service
cp "$INSTALL_DIR/udev/99-hidg.rules" /etc/udev/rules.d/99-hidg.rules

sed -i "s/User=admin/User=$SERVICE_USER/g" /etc/systemd/system/mivi-agent.service
sed -i "s/OWNER=\"admin\"/OWNER=\"$SERVICE_USER\"/g" /etc/udev/rules.d/99-hidg.rules
sed -i "s/GROUP=\"admin\"/GROUP=\"$SERVICE_USER\"/g" /etc/udev/rules.d/99-hidg.rules

systemctl daemon-reload
udevadm control --reload-rules

systemctl enable usb-keyboard-gadget
systemctl enable mivi-agent

echo ""
echo "Install complete."
echo ""
echo "Now make sure USB gadget mode is enabled:"
echo ""
echo "1. /boot/firmware/config.txt contains:"
echo "   dtoverlay=dwc2"
echo ""
echo "2. /boot/firmware/cmdline.txt contains, on the same line:"
echo "   modules-load=dwc2"
echo ""
echo "Then reboot:"
echo "sudo reboot"
echo ""
echo "After reboot, open:"
echo "http://rzero.local:8080"