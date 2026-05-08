import json
import ssl
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

# --- CONFIGURACIÓN DE LOGS ---
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)

# --- 1. CONEXIÓN A FIREBASE ---
try:
    # Aseguramos que no se inicialice dos veces si reiniciás el script
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-key.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    log.info("Conexión con Firebase establecida ✓")
except Exception as e:
    log.error(f"Error crítico al iniciar Firebase: {e}")
    exit(1)

# --- 2. PARÁMETROS MQTT (HiveMQ Cloud) ---
HOST     = "aec31a90bbda48f3b180689b08b9e33b.s1.eu.hivemq.cloud"
PORT     = 8883
USER     = "pablo"
PASSWORD = "Test1234"

# --- 3. LÓGICA DE PROCESAMIENTO ---
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        log.info("MQTT Conectado. Escuchando flujo de todas las casas...")
        # Usamos el wildcard '+' para captar cualquier ID de casa
        client.subscribe("iot/casas/+/telemetria")
        client.subscribe("iot/casas/+/alertas")
    else:
        log.error(f"Error de conexión MQTT. Código: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        topic_parts = msg.topic.split("/")
        
        # Estructura del topic: iot / casas / {casa_id} / {tipo}
        casa_id = topic_parts[2]
        tipo_dato = topic_parts[3] 

        # ID único para el documento: [ID_CASA]_[TIMESTAMP]
        ts_now = datetime.now(timezone.utc)
        doc_name = f"{casa_id}_{ts_now.strftime('%Y%m%d_%H%M%S_%f')}"

        # Guardado dinámico según el tipo
        if tipo_dato == "telemetria":
            m = payload.get("medicion", {})
            log.info(f"☁ [DB] Guardando {casa_id}: {m.get('tension_v')}V | {m.get('consumo_w')}W")
            db.collection("telemetria").document(doc_name).set(payload)
            
        elif tipo_dato == "alertas":
            alerta = payload.get("alerta", {})
            log.warning(f"⚠ [DB] ALERTA EN {casa_id}: {alerta.get('descripcion')}")
            db.collection("alertas").document(doc_name).set(payload)

    except json.JSONDecodeError:
        log.error("Error: Se recibió un mensaje que no es JSON válido.")
    except Exception as e:
        log.error(f"Error procesando mensaje en {msg.topic}: {e}")

# --- 4. EJECUCIÓN DEL CLIENTE ---
cliente = mqtt.Client(
    client_id="bridge_firebase_cloud", 
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)
cliente.username_pw_set(USER, PASSWORD)
cliente.tls_set(tls_version=ssl.PROTOCOL_TLS)

cliente.on_connect = on_connect
cliente.on_message = on_message

if __name__ == "__main__":
    try:
        log.info("Iniciando Bridge de Firebase... (Presioná Ctrl+C para salir)")
        cliente.connect(HOST, PORT, keepalive=60)
        cliente.loop_forever()
    except KeyboardInterrupt:
        log.info("Bridge detenido por el usuario.")
    except Exception as e:
        log.error(f"Falla en el loop principal: {e}")