import time

from gpiozero import Button, RGBLED
from colorzero import Color

from configuration import *
from pulse import Perlin1D
from interpolate import interp_hsv
from cheerlights import get_cheerlights_colour
from iss import get_iss_colour


class LightUpMode:
    MODES = [
        ("cheerlights", get_cheerlights_colour),
        ("iss", get_iss_colour),
    ]

    def __init__(self):
        self._current_idx = 0
        self.num_modes = len(LightUpMode.MODES)

    def increase_mode(self):
        self._current_idx = (self._current_idx + 1) % self.num_modes
        return self.current_mode

    @property
    def current_mode(self):
        return LightUpMode.MODES[self._current_idx]



def main():

    print("starting light up")

    led = RGBLED(
        red=RED_PIN,
        green=GREEN_PIN,
        blue=BLUE_PIN,
    )

    mode = LightUpMode()
    state = {
        "get_new_colour": mode.current_mode[1],
        "changed_mode": False,
    }

    def pressed():
        print("changing mode")
        name, fn = mode.increase_mode()
        state["get_new_colour"] = fn 
        state["changed_mode"] = True
        print("mode =", name)

    btn = Button(BTN_PIN)
    btn.when_pressed = pressed

    try:
        current_color = state["active_mode"]()
    except:
        current_color = Color(0, 0, 0)
    start_color = current_color
    target_color = current_color
    perlin = Perlin1D(seed=42)
    perlin_t = 0.0

    transitioning = False
    transition_start = 0.0
    last_fetch = 0.0


    while True:
        now = time.time()

        # get target colour
        if state["changed_mode"] or now - last_fetch > POLL_INTERVAL:
            try:
                new_color = state["get_new_colour"]()


                if new_color != target_color:
                    start_color = current_color
                    target_color = new_color
                    transition_start = now
                    transitioning = True

                last_fetch = now
                changed_mode = False
            except Exception as e:
                print(e)

        # interpolate to target if not there
        if transitioning:
            t = (now - transition_start) / INTERP_DURATION
            if t >= 1.0:
                current_color = target_color
                transitioning = False
                h, s, v = current_color.hsv
            else:
                h, s, v = interp_hsv(start_color, target_color, t)
                current_color = Color.from_hsv(h, s, v)
        else:
            h, s, v = current_color.hsv

        # brightness variation
        n_fast = perlin.noise(perlin_t * PULSE_SPEED)
        n_slow = perlin.noise(perlin_t * 0.3)
        n = 0.7 * n_fast + 0.3 * n_slow

        #n_biased = n - 0.15
        #v_pulsed = v * (1.0 + PULSE_AMPLITUDE * n_biased)
        v_pulsed = v * (1.0 + PULSE_AMPLITUDE * n)
        v_pulsed = max(MIN_V, min(MAX_V, v_pulsed))

        led.color = Color.from_hsv(h, s, v_pulsed)

        perlin_t += DT
        time.sleep(DT)

if __name__ == "__main__":
    main()
