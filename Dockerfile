# Dockerfile für KI-Assistent auf openSUSE
FROM opensuse/leap:15.5

# Metadaten
LABEL maintainer="KI Project"
LABEL description="KI-Assistent für Wetter- und Nachrichtenfragen"

# System-Updates und Python installieren
RUN zypper --non-interactive refresh && \
    zypper --non-interactive install -y \
        python311 \
        python311-pip \
        python311-devel \
    && zypper clean --all

# Python als Standard setzen
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/pip3 pip3 /usr/bin/pip3.11 1

# Arbeitsverzeichnis erstellen
WORKDIR /app

# Requirements kopieren und installieren
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY src/ ./src/
COPY app.py .

# Optional: .env Datei (falls vorhanden)
COPY .env* ./

# Standardbefehl
CMD ["python3", "app.py"]
