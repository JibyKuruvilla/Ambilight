# Ambilight
Ambilight helps to dynamically adjusts the RGB LEDs to match the edge colors of your screen in real time, creating an immersive viewing experience.

## How It Works
- The led_server.py script on the host machine captures screen colors periodically and calculates RGB values for the LED strip.
- It transmits the RGB data to a Raspberry Pi via SSH.
- The led_client.py script on the Raspberry Pi sets the LED strip colors based on the received data.
- The LED strip dynamically adjusts to match the screen's edge colors.

## Hardware Requirements
- A Raspberry Pi (e.g., Raspberry Pi 4 or equivalent).
- A RGB LED strip (e.g., WS2812B).
- A 5V power supply suitable for your LED strip's length and power consumption and a DC Barrel Jack to 2-Pin Terminal Block Adapter .
- Necessary wiring and connectors to connect the LED strip to the Raspberry Pi's GPIO pins.

For a detailed guide on assembling the hardware, watch this instructional video from Core Electronics for the long LED Strip:
https://www.youtube.com/watch?v=aNlaj1r7NKc

## Setup
The host machine and the Raspberry Pi must be connected to the same local network for proper communication.
1. **Host Machine**:
2. - Install the required libraries:
     ```bash
     pip install -r requirements_led_server.txt
     ```
   - Create a .env file and add these variables with their respective values:
      SSH_RASPBERRYPI_IPADDRESS=<Your Raspberry Pi IP>
      SSH_RASPBERRYPI_USERNAME=<Your Username>
      SSH_RASPBERRYPI_PASSWORD=<Your Password>
   - Adjust `LED_TOP`, `LED_RIGHT`, `LED_BOTTOM`, and `LED_LEFT` in `led_server.py` to match your LED configuration.

3. **Raspberry Pi**:
   - Install the required libraries:
     ```bash
     pip3 install rpi_ws281x --break-system-packages
     pip3 install adafruit-circuitpython-neopixel --break-system-packages
     python3 -m pip install --force-reinstall adafruit-blinka --break-system-packages
     ```
   - Ensure `led_server.py` is located at `/home/raspberrypi/`.
   - Adjust `LED_COUNT` in `led_server.py` based on the total amount of LEDS required.

## Usage
Run the `led_server.py` script on the host machine:
```bash
python3 led_server.py
```

## Acknowledgments
Special thanks to my project partner Marie-Louise Korn and all the developers and contributors of all the libraries used in this project.
