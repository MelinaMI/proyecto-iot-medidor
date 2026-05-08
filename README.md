# Sistema de Telemetría Eléctrica IoT

Este proyecto simula medidores de consumo eléctrico para dos domicilios en **Proteus**, enviando los datos a **Firebase Firestore** mediante un broker MQTT (**HiveMQ Cloud**).

## 🚀 Cómo ponerlo en marcha

### 1. Requisitos de Software
* **Python 3.x**: Instalar librerías con `pip install -r bridges/requirements.txt`
* **Arduino IDE**: Para compilar el código `.ino`
* **Proteus 8.13+**: [Guía de instalación](https://www.youtube.com/watch?v=s1XB4vhJDqI)
* **VSPE (Virtual Serial Port Driver)**: Necesario para los puertos virtuales.
* **Instalador de Proteus y VSPE**:  [Instalables](https://drive.google.com/drive/folders/1AvDNC8VeEFvVP2i_Fgh-rcRkQikiX4Gv?usp=sharing)

### 2. Configuración de Puertos Virtuales (VSPE)
Antes de iniciar la simulación, configurar los siguientes pares en **VSPE**:
1. Abrir VSPE y seleccionar `Device` -> `Create`
2. Seleccionar Virtual Pair del menú desplegable
3. Nombrar los puertos como COM8 y COM9, repetir proceso para COM10 y COM11.
* Nota: En Proteus, los COMPIM están configurados en COM8 y COM10. Los scripts de Python escuchan en COM9 y COM11 respectivamente.
4. Vas a poder ver si están corriendo abriendo el  `admin. de dispositivos` -> `puertos (COM y LPT)`
  
### 3. Ejecución del Sistema
Para que el flujo de datos funcione, abrir **3 terminales** en VS Code y ejecutar:

1. **Bridge Casa 1:** `python bridges/bridge_serial1.py`
2. **Bridge Casa 2:** `python bridges/bridge_serial2.py`
3. **Bridge Cloud (Firebase):** `python bridges/bridge_firebase.py`

*Una vez que los bridges digan "Conectado", dar Play a la simulación en Proteus.*

### 4. Estructura de Datos (Firestore)
Los datos se organizan automáticamente en:
* `telemetria/`: Lecturas en tiempo real (`tension_v`, `corriente_a`, `consumo_w`).
* `alertas/`: Registros de anomalías detectadas (Picos de tensión o sobrecorriente).

---
### 🔑 Configuración de Firebase
Por razones de seguridad, las credenciales de la base de datos no se incluyen en este repositorio.

1. Localizá el archivo `firebase-key.json.example` en la raíz.
2. Duplicá el archivo y renombralo exactamente como `firebase-key.json`.
3. Pegá tus credenciales de Service Account dentro del archivo.
4. El archivo `.gitignore` ya está configurado para que nunca subas tu clave real al servidor.
