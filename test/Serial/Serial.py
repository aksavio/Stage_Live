import serial
import serial.tools.list_ports
import time

HANDSHAKE_REQUEST = "ESP_READY"
HANDSHAKE_RESPONSE = "PI_ACK"

def find_esp():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            print(f"Trying {port.device}...")
            ser = serial.Serial(port.device, 115200, timeout=2)
            time.sleep(2)  # wait for ESP reset on new serial connection

            # give ESP time to send message
            line = ser.readline().decode("utf-8").strip()
            if line == HANDSHAKE_REQUEST:
                print(f"✅ Found ESP on {port.device}")
                ser.write((HANDSHAKE_RESPONSE + "\n").encode("utf-8"))
                return ser  # return the open serial connection
            else:
                print(f"No handshake message from {port.device} (got: '{line}')")
                ser.close()
        except Exception as e:
            print(f"Error with {port.device}: {e}")
    return None

if __name__ == "__main__":
    esp_serial = find_esp()
    if esp_serial:
        print("Handshake complete! You can now communicate with the ESP.")
        try:
            while True:
                if esp_serial.in_waiting:
                    msg = esp_serial.readline().decode().strip()
                    print(f"[ESP] {msg}")
                    esp_serial.write(b"Hello back from Pi!\n")
                time.sleep(1)
        except KeyboardInterrupt:
            esp_serial.close()
            print("Closed connection.")
    else:
        print("No ESP found.")
