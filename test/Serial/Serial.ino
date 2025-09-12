#include <Arduino.h>

#define HANDSHAKE_REQUEST "ESP_READY"
#define HANDSHAKE_RESPONSE "PI_ACK"

bool handshakeDone = false;

void setup()
{
  Serial.begin(115200);
  delay(2000);                       // wait for Serial to come up
  Serial.println(HANDSHAKE_REQUEST); // tell Pi that ESP is ready
}

void loop()
{
  if (!handshakeDone && Serial.available())
  {
    String msg = Serial.readStringUntil('\n');
    msg.trim();
    if (msg == HANDSHAKE_RESPONSE)
    {
      // Serial.println("Handshake successful!");
      handshakeDone = true;
    }
  }

  if (handshakeDone)
  {
    Serial.println("Hello from ESP!");
    delay(2000);
  }
}
