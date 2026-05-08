/*
  Medidor de consumo eléctrico — SIMULINO UNO + Proteus 8
  Alertas: Consumo, Corriente y Tensión (Red Eléctrica)
*/
#define ID_CASA 1
const int PIN_CORRIENTE = A0;
const int PIN_TENSION   = A1;

const int MUESTRAS      = 100;
const float FP          = 0.90;
const float CORRIENTE_MAX = 20.0;
const float TENSION_MIN   = 160.0;
const float TENSION_MAX   = 260.0;

// Umbrales de Alerta
const float CONSUMO_MAX       = 4500.0; // Watts
const float CORRIENTE_PELIGRO = 18.0;   // Amperios
const float TENSION_ALTA      = 242.0;  // Volts
const float TENSION_BAJA      = 198.0;  // Volts

void setup() {
  Serial.begin(9600);
  }

float leerTension() {
  long suma = 0;
  for (int i = 0; i < MUESTRAS; i++) {
    suma += analogRead(PIN_TENSION);
    delay(1);
  }
  return TENSION_MIN + ( (suma / (float)MUESTRAS) / 1023.0) * (TENSION_MAX - TENSION_MIN);
}

float leerCorriente() {
  long suma = 0;
  for (int i = 0; i < MUESTRAS; i++) {
    suma += analogRead(PIN_CORRIENTE);
    delay(1);
  }
  return ( (suma / (float)MUESTRAS) / 1023.0) * CORRIENTE_MAX;
}

void loop() {
  float tension   = leerTension();
  float corriente = leerCorriente();
  float potencia  = tension * corriente * FP;

  // Lógica de Alertas
  bool pico_consumo   = potencia > CONSUMO_MAX;
  bool sobrecorriente = corriente > CORRIENTE_PELIGRO;
  bool tension_critica = (tension > TENSION_ALTA || tension < TENSION_BAJA);

  // Envío JSON por Serial
  Serial.print("{");
  Serial.print("\"casa_id\":\"GENERICA\",");
  Serial.print("\"medicion\":{");
  Serial.print("\"tension_v\":"); Serial.print(tension, 1); Serial.print(",");
  Serial.print("\"corriente_a\":"); Serial.print(corriente, 3); Serial.print(",");
  Serial.print("\"consumo_w\":"); Serial.print(potencia, 1); Serial.print(",");
  Serial.print("\"factor_potencia\":"); Serial.print(FP, 2);
  Serial.print("},");
  Serial.print("\"alertas\":{");
  Serial.print("\"pico_consumo\":"); Serial.print(pico_consumo ? "true" : "false"); Serial.print(",");
  Serial.print("\"sobrecorriente\":"); Serial.print(sobrecorriente ? "true" : "false"); Serial.print(",");
  Serial.print("\"tension_critica\":"); Serial.print(tension_critica ? "true" : "false");
  Serial.print("}");
  Serial.println("}");

}
