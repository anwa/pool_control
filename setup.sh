#!/bin/bash
REPO_URL="https://github.com/anwa/pool_control.git"
PROJECT_DIR="pool_control"

# Repository clonen
if [ ! -d "$PROJECT_DIR" ]; then
  git clone $REPO_URL
else
  echo "Verzeichnis $PROJECT_DIR existiert bereits."
fi

# In Projektverzeichnis wechseln
cd $PROJECT_DIR

# Virtuelle Umgebung erstellen und aktivieren
python -m venv venv
source venv/bin/activate

# Bibliotheken installieren
if [ -f "requirements-linux.txt" ]; then
  pip install -r requirements-linux.txt
else
  echo "requirements-linux.txt nicht gefunden. Installiere Standard-Bibliotheken."
  pip install kivy smbus2 paho-mqtt
  pip freeze > requirements-linux.txt
fi

echo "Setup abgeschlossen. Virtuelle Umgebung ist aktiviert."