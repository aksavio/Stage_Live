#include <Arduino.h>

#define HANDSHAKE_REQUEST "ESP_READY"
#define HANDSHAKE_RESPONSE "PI_ACK"

bool handshakeDone = false;

#include <BLEMidi.h>

void onNoteOn(uint8_t channel, uint8_t note, uint8_t velocity, uint16_t timestamp)
{
    Serial.printf("Note on : channel %d, note %d, velocity %d (timestamp %dms)\n", channel, note, velocity, timestamp);
}

void onNoteOff(uint8_t channel, uint8_t note, uint8_t velocity, uint16_t timestamp)
{
    Serial.printf("Note off : channel %d, note %d, velocity %d (timestamp %dms)\n", channel, note, velocity, timestamp);
}

void onAfterTouchPoly(uint8_t channel, uint8_t note, uint8_t pressure, uint16_t timestamp)
{
    Serial.printf("Polyphonic after touch : channel %d, note %d, pressure %d (timestamp %dms)\n", channel, note, pressure, timestamp);
}

void onControlChange(uint8_t channel, uint8_t controller, uint8_t value, uint16_t timestamp)
{
    Serial.printf("Control change : channel %d, controller %d, value %d (timestamp %dms)\n", channel, controller, value, timestamp);
}

void onProgramChange(uint8_t channel, uint8_t program, uint16_t timestamp)
{
    Serial.printf("Program change : channel %d, program %d (timestamp %dms)\n", channel, program, timestamp);
}

void onAfterTouch(uint8_t channel, uint8_t pressure, uint16_t timestamp)
{
    Serial.printf("After touch : channel %d, pressure %d (timestamp %dms)\n", channel, pressure, timestamp);
}

void onPitchbend(uint8_t channel, uint16_t value, uint16_t timestamp)
{
    Serial.printf("Pitch bend : channel %d, value %d (timestamp %dms)\n", channel, value, timestamp);
}

void setup()
{
    Serial.begin(115200);
    delay(2000); // wait for Serial to come up
    // Serial.println(HANDSHAKE_REQUEST); // tell Pi that ESP is ready
    while (!handshakeDone)
    {
        Serial.println(HANDSHAKE_REQUEST); // tell Pi that ESP is ready
        if (!handshakeDone && Serial.available())
        {
            String msg = Serial.readStringUntil('\n');
            msg.trim();
            if (msg == HANDSHAKE_RESPONSE)
            {
                Serial.println("Handshake successful!");
                handshakeDone = true;
            }
        }
        delay(2000);
    }
    if (handshakeDone)
    {
        // Serial.println("Hello from ESP!");
        delay(2000);
    }

    BLEMidiServer.begin("MIDI device");
    BLEMidiServer.setOnConnectCallback([]()
                                       { Serial.println("Connected"); });
    BLEMidiServer.setOnDisconnectCallback([]()
                                          { Serial.println("Disconnected"); });
    BLEMidiServer.setNoteOnCallback(onNoteOn);
    BLEMidiServer.setNoteOffCallback(onNoteOff);
    BLEMidiServer.setAfterTouchPolyCallback(onAfterTouchPoly);
    BLEMidiServer.setControlChangeCallback(onControlChange);
    BLEMidiServer.setProgramChangeCallback(onProgramChange);
    BLEMidiServer.setAfterTouchCallback(onAfterTouch);
    BLEMidiServer.setPitchBendCallback(onPitchbend);
    // BLEMidiServer.enableDebugging();
}

void loop()
{
    Serial.println("0");
    delay(4000);
    Serial.println("1");
    delay(4000);
    Serial.println("3");
    delay(4000);
}
