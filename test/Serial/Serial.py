import serial
import time

# Configure the serial port
# Replace '/dev/ttyUSB0' with the appropriate port for your system (e.g., 'COM1' on Windows)
ser = serial.Serial(
    port='/dev/cu.usbmodem1101',  
    baudrate=115200,
    timeout=1  # Timeout in seconds for read operations
)

def read_serial_data():
    """Reads data from the serial port if available."""
    if ser.in_waiting > 0:
        # Read until a newline character and decode from bytes to string
        data = ser.readline().decode('utf-8').rstrip()
        print(f"Received: {data}")
        return data
    return None

# Main loop to continuously read data
try:
    while True:
        read_serial_data()
        time.sleep(0.1)  # Small delay to prevent busy-waiting
except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    ser.close()
    print("Serial port closed.")
