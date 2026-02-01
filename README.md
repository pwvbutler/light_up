# Light UP

Small project to control RGB LEDs from a raspberry pi based on real-time data with smooth interpolation between colours and other effects.

Designed for multiple modes with current implementations for cheerlights and the International Space Station position.

## Software Requirements

* Python 3
* `gpiozero`
* `colorzero`
* `requests`

## Running

set the parameters in configuration.py and then execute:

```bash
python light_up.py
```

Press the button to cycle between modes.

---

## Customization

Useful parameters in `configuration.py`:

* `INTERP_DURATION` – duration for interpolating between colours
* `PULSE_SPEED` – how fast the brightness flickers
* `PULSE_AMPLITUDE` – strength of the pulse
* `MIN_V`, `MAX_V` – brightness limits
* `POLL_INTERVAL` – how often external APIs are queried

Just tell me the audience.
