# setup.ps1
$RepoUrl = "https://github.com/anwa/pool_control.git"
$ProjectDir = "pool_control"

# Repository clonen
if (-not (Test-Path $ProjectDir)) {
    Write-Host "Cloning repository from $RepoUrl..."
    git clone $RepoUrl
} else {
    Write-Host "Verzeichnis $ProjectDir existiert bereits."
}

# In Projektverzeichnis wechseln
Set-Location $ProjectDir

# Virtuelle Umgebung erstellen und aktivieren
Write-Host "Erstelle virtuelle Umgebung..."
python -m venv venv
Write-Host "Aktiviere virtuelle Umgebung..."
. .\venv\Scripts\Activate.ps1

# Bibliotheken installieren
if (Test-Path "requirements.txt") {
    Write-Host "Installiere Bibliotheken aus requirements.txt..."
    pip install -r requirements.txt
} else {
    Write-Host "requirements.txt nicht gefunden. Installiere Standard-Bibliotheken."
    pip install kivy smbus2 paho-mqtt
    Write-Host "Erstelle requirements.txt..."
    pip freeze | Out-File -Encoding UTF8 requirements.txt
}

Write-Host "Setup abgeschlossen. Virtuelle Umgebung ist aktiviert."
Read-Host "Drücke Enter, um fortzufahren..."