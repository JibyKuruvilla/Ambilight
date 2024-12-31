import board
import neopixel
import multiprocessing

# define constants for rgb strip
LED_COUNT = 133  # TODO the total LED count must be defined before use
LED_BRIGHTNESS = 65
strip = neopixel.NeoPixel(
    board.D18, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False
)


# Function to set the LEDs
def set_leds(rgbs):
    for i in range(LED_COUNT):
        strip[i] = rgbs[i]
    strip.show()


# Function to stop the LEDs (turn them off)
def stop_leds():
    for i in range(LED_COUNT):
        strip[i] = [0, 0, 0]
    strip.show()


if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=10)

    try:
        while True:
            input_data = input()
            if input_data == "exit":
                pool.apply_async(stop_leds, args=())
                break
            pool.apply_async(set_leds, args=(eval(input_data),))
    except KeyboardInterrupt:
        pool.apply_async(stop_leds, args=())
    finally:
        pool.close()
        pool.join()
