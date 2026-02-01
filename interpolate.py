
def interp_hsv(c0, c1, t):
    h0, s0, v0 = c0.hsv
    h1, s1, v1 = c1.hsv

    dh = ((h1 - h0 + 0.5) % 1.0) - 0.5

    h = (h0 + dh * t) % 1.0
    s = s0 + (s1 - s0) * t
    v = v0 + (v1 - v0) * t

    return h, s, v

