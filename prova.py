import serial

# Define the serial port and baud rate
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

try:
    # Open the serial port
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Listening on {SERIAL_PORT} at {BAUD_RATE} baud...\n")

    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            print(line)  # Print received data

except serial.SerialException as e:
    print(f"Serial error: {e}")

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial connection closed.")
