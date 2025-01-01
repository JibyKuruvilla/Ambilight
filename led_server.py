import os
from dotenv import load_dotenv, find_dotenv
from PIL import Image
import numpy as np
import paramiko
import mss
import mss.tools

# TODO count leds on each side of monitor before use
LED_TOP = 41
LED_RIGHT = 24
LED_BOTTOM = 43
LED_LEFT = 25

# Define the server and login details
# TODO change the credentials in the .env file
port = 22
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
host_ip = os.getenv("SSH_RASPBERRYPI_IPADDRESS")
username = os.getenv("SSH_RASPBERRYPI_USERNAME")
password = os.getenv("SSH_RASPBERRYPI_PASSWORD")
print(f"Host_IP: {host_ip}")
print(f"Username: {username}")
print(f"Password: {password}")


# Function to calculate rgb values for one led
def calculate_rgb(x_start, x_end, y_start, y_end):
    red = green = blue = num = 0
    for i in range(x_start, x_end):
        for j in range(y_start, y_end):
            r, g, b = screenshot.getpixel((i, j))
            red += r
            green += g
            blue += b
            num += 1

    return [int(red / num), int(green / num), int(blue / num)]

# Initializing the SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# check for second monitor
sct = mss.mss()
monitors = sct.monitors
if len(monitors) == 2:
    monitor = monitors[1]
else:
    monitor = monitors[2]

# get resolution of monitor
SCREEN_W, SCREEN_H = sct.grab(monitor).size

try:
    # Connect to the remote server
    client.connect(host_ip, port, username, password)
    transport = client.get_transport()
    channel = transport.open_session()

    # execute the remote script
    remote_script_path = "/home/raspberrypi/led_client.py"
    channel.get_pty()
    channel.exec_command(f"sudo python3 {remote_script_path}")
    print("Successfully connected to remote host")

    while True:
        init_screenshot = sct.grab(monitor)
        screenshot = Image.frombytes(
            "RGB", (init_screenshot.width, init_screenshot.height), init_screenshot.rgb
        )

        # DIANA
        h = int(SCREEN_H / LED_RIGHT)
        w = int(SCREEN_W / LED_TOP)
        leds_top = []
        for i in range(LED_TOP):
            leds_top.append(calculate_rgb(i * w, (i + 1) * w, 0, h + 20))

        leds_right = []
        for i in range(LED_RIGHT):
            leds_right.append(
                calculate_rgb(SCREEN_W - w - 30, SCREEN_W, i * h, (i + 1) * h)
            )

        h = int(SCREEN_H / LED_LEFT)
        w = int(SCREEN_W / LED_BOTTOM)
        leds_bottom = []
        for i in range(LED_BOTTOM):
            leds_bottom.append(
                calculate_rgb(i * w, (i + 1) * w, SCREEN_H - h - 20, SCREEN_H)
            )
        leds_bottom.reverse()

        leds_left = []
        for i in range(LED_LEFT):
            leds_left.append(calculate_rgb(0, w + 30, i * h, (i + 1) * h))
        leds_left.reverse()

        led_strip = leds_left + leds_top + leds_right + leds_bottom
        channel.send((f"{led_strip}" + "\n").encode("utf-8"))

except (
    paramiko.ssh_exception.AuthenticationException,
    paramiko.ssh_exception.SSHException,
    paramiko.ssh_exception.NoValidConnectionsError,
) as e:
    print(f"An SSH error occurred: {e}")
except KeyboardInterrupt:
    channel.send(("exit" + "\n").encode("utf-8"))
    print("Interrupted by user")
finally:
    client.close()
    print("SSH client closed.")


# if you want to test the algorithm without an LED strip
def test_rgb_calculation(leds_top, leds_right, leds_left, leds_bottom, img_index):
    data = np.zeros((SCREEN_H, SCREEN_W, 3), dtype=np.uint8)

    leds_bottom.reverse()
    leds_left.reverse()

    h = int(SCREEN_H / LED_RIGHT)
    w = int(SCREEN_W / LED_TOP)
    for l in range(LED_TOP):
        block = np.full((h, w, 3), leds_top[l], dtype=np.uint8)
        data[0:w, w * l : w * (l + 1)] = block
    for l in range(LED_RIGHT):
        block = np.full((h, w, 3), leds_right[l], dtype=np.uint8)
        data[l * h : (l + 1) * h, SCREEN_W - h : SCREEN_W] = block
    
    h = int(SCREEN_H / LED_LEFT)
    w = int(SCREEN_W / LED_BOTTOM)
    for l in range(LED_BOTTOM):
        block = np.full((h, w, 3), leds_bottom[l], dtype=np.uint8)
        data[SCREEN_H - w : SCREEN_H, l * w : (l + 1) * w] = block
    for l in range(LED_LEFT):
        block = np.full((h, w, 3), leds_left[l], dtype=np.uint8)
        data[l * h : (l + 1) * h, 0:h] = block

    img = Image.fromarray(data, "RGB")
    img.save(f"ledtest{img_index}.png")

