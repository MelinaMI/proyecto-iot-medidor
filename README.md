# Sistema de Telemetría Eléctrica IoT ⚡

Este proyecto mide tensión, corriente y potencia en simulación (Proteus) y envía los datos a Firebase mediante MQTT.

## 🚀 Cómo ponerlo en marcha

### 1. Requisitos
* Instalar librerías: `pip install -r bridges/requirements.txt`
* Instalar **VSPE** para los puertos virtuales.

### 2. Ejecución de los Bridges
Para ver los datos en tiempo real, hay que correr los tres scripts en terminales separadas:

* **Bridge Casa 1:** `python bridges/bridge_serial1.py` (Configurado en COM9)
* **Bridge Casa 2:** `python bridges/bridge_serial2.py` (Configurado en COM111)
* **Bridge Cloud:** `python bridges/bridge_firebase.py` (Este escucha a todas las casas y sube a Firestore).

### 3. Estructura de Firebase
Los datos se guardan en:
* `telemetria/{CASA_ID}_{TIMESTAMP}`
* `alertas/{CASA_ID}_{TIMESTAMP}`
