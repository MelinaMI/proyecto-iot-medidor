import json
import ssl
import logging
import serial
import paho.mqtt.client as mqtt
from datetime import datetime, timezone

# --- CONFIGURACIÓN DE LOGS ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# --- PARÁMETROS DE CONFIGURACIÓN ---
SERIAL_PORT = "COM11"   
ID_CASA     = "CASA_02"
BAUD_RATE   = 9600

MQTT_HOST   = "aec31a90bbda48f3b180689b08b9e33b.s1.eu.hivemq.cloud"
MQTT_PORT   = 8883
MQTT_USER   = "pablo"
MQTT_PASS   = "Test1234"

# --- LÓGICA DE ALERTAS  ---
def detectar_anomalias(datos: dict) -> list:
    alertas = []
    m = datos.get("medicion", {})
    a = datos.get("alertas", {})

    if a.get("tension_critica"):
        v = m.get("tension_v", 0)
        tipo = "PICO_DE_TENSION" if v > 230 else "BAJA_TENSION"
        desc = f"¡{tipo.replace('_', ' ')}! Lectura: {v:.1f}V"
        alertas.append({"tipo": tipo, "severidad": "CRITICA", "descripcion": desc, "valor": v})

    if a.get("sobrecorriente"):
        i = m.get("corriente_a", 0)
        alertas.append({
            "tipo": "SOBRECORRIENTE",
            "severidad": "ALTA",
            "descripcion": f"CORRIENTE PELIGROSA: {i:.2f}A",
            "valor": i
        })
    return alertas

# --- CONFIGURACIÓN MQTT ---
cliente_mqtt = mqtt.Client(client_id=f"bridge_{ID_CASA}", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
cliente_mqtt.username_pw_set(MQTT_USER, MQTT_PASS)
cliente_mqtt.tls_set(tls_version=ssl.PROTOCOL_TLS)

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0: log.info(f"MQTT Conectado para {ID_CASA} ✓")
    else: log.error(f"Error MQTT: {rc}")

cliente_mqtt.on_connect = on_connect
cliente_mqtt.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
cliente_mqtt.loop_start()

# --- LOOP PRINCIPAL ---
def main():
    log.info(f"Iniciando Bridge {ID_CASA} en {SERIAL_PORT}...")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    except Exception as e:
        log.error(f"No se pudo abrir {SERIAL_PORT}: {e}")
        return

    while True:
        try:
            linea = ser.readline().decode("utf-8").strip()
            if not linea or not (linea.startswith('{') and linea.endswith('}')):
                continue

            # Procesamiento de datos
            datos = json.loads(linea)
            datos["casa_id"] = ID_CASA  
            datos["timestamp"] = datetime.now(timezone.utc).isoformat()
            
            # 1. Publicar Telemetría
            topic_t = f"iot/casas/{ID_CASA}/telemetria"
            cliente_mqtt.publish(topic_t, json.dumps(datos), qos=1)

            # Log resumido
            m = datos.get("medicion", {})
            log.info(f"[{ID_CASA}] ENVIADO: {m.get('tension_v')}V | {m.get('consumo_w')}W")

            # 2. Publicar Alertas si existen
            for alerta in detectar_anomalias(datos):
                payload_alerta = {"casa_id": ID_CASA, "timestamp": datos["timestamp"], "alerta": alerta}
                cliente_mqtt.publish(f"iot/casas/{ID_CASA}/alertas", json.dumps(payload_alerta), qos=2)
                log.warning(f"⚠ ALERTA EN {ID_CASA}: {alerta['descripcion']}")

        except json.JSONDecodeError: continue
        except KeyboardInterrupt: break
        except Exception as e: log.error(f"Error: {e}")

    ser.close()
    cliente_mqtt.loop_stop()

if __name__ == "__main__":
    main()