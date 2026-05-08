# Sistema de Telemetría Eléctrica IoT ⚡

Este proyecto mide tensión, corriente y potencia en simulación (Proteus) y envía los datos a Firebase mediante MQTT.

## 🚀 Cómo ponerlo en marcha

### 1. Requisitos
* Instalar librerías: `pip install -r bridges/requirements.txt`
* Instalar Proteus 8 `seguir guía de este video https://www.youtube.com/watch?v=s1XB4vhJDqI&list=PL46-OijoqbXNc9b6-cn4gAYm6EBxwocQs&index=3`
* Tener Arduino IDE instalado
* Instalar **VSPE** para los puertos virtuales.

### 2. Para tener en cuenta
* Al momento de correr el simulador, tener en cuenta que VSPE debe estar corriendo también con los puertos configurados para que se creen los puertos vituales que se usan en la configuración de P1 y P
* `Una vez instalado, buscar VSPE, en la barra de herramientas buscar Device -> create new device, seleccionar Virtual Pair del menú desplegable y nombrar los puertos como COM8 y COM9, repetir proceso para COM10 y COM11`

### 3. Ejecución de los Bridges
Para ver los datos en tiempo real, hay que correr los tres scripts en terminales separadas:

* **Bridge Casa 1:** `python bridges/bridge_serial1.py` (Configurado en COM9)
* **Bridge Casa 2:** `python bridges/bridge_serial2.py` (Configurado en COM11)
* **Bridge Cloud:** `python bridges/bridge_firebase.py` (Este escucha a todas las casas y sube a Firestore).

### 4. Estructura de Firebase
Los datos se guardan en:
* `telemetria/{CASA_ID}_{TIMESTAMP}`
* `alertas/{CASA_ID}_{TIMESTAMP}`
