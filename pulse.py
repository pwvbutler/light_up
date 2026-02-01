import time
import random
import math



class Perlin1D:
    def __init__(self, seed=None):
        self.gradients = {}
        if seed is not None:
            random.seed(seed)

    def _gradient(self, i):
        if i not in self.gradients:
            self.gradients[i] = random.uniform(-1, 1)
        return self.gradients[i]

    @staticmethod
    def _fade(t):
        # 6t^5 - 15t^4 + 10t^3
        return t * t * t * (t * (t * 6 - 15) + 10)

    @staticmethod
    def _lerp(a, b, t):
        return a + t * (b - a)

    def noise(self, x):
        x0 = math.floor(x)
        x1 = x0 + 1

        g0 = self._gradient(x0)
        g1 = self._gradient(x1)

        t = x - x0
        fade = self._fade(t)

        n0 = g0 * (x - x0)
        n1 = g1 * (x - x1)

        return self._lerp(n0, n1, fade)
