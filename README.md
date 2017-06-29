# roomba

Based on https://github.com/martinschaef/roomba


On Raspberry PI:

1. Make sure GPIO serial ports are available as a serial device (e.g. /dev/serial0)
2. Install pyserial if not installed
3. Copy rfc2217_server.py from pyserial distribution or modify remote_serial.sh accordingly.
4. Run remote_serial.sh to enable network access to serial port.
5. Run camera_server.py for camera access.


On Client:

0. Configure Raspberry PI hostname in roomba.py
1. Run unmodified roomba.py (requires step 5. from Rasperry PI) or modify for you needs

