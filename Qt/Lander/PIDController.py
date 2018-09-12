# -*- coding: utf-8 -*-
"""

PID Controller for lander.py

Based on Orcina's version.

"""


class PIDController(object):

    def __init__(self):

        # The constants of the PID controller:
        self.k0 = 20
        self.kP = -2
        self.kI = -0.5
        self.kD = -1

        # And default to not limiting the control variable:
        self.MinValue = 0
        self.MaxValue = 100

        self.now_signal = 0

        self.prev_iedt = 0.0
        self.now_iedt = 0.0
        self.now_dedt = 0.0

        print('Initialised OK.')

    def Calculate(self, signal, target, dt):

        self.prev_signal = self.now_signal
        self.prev_iedt = self.now_iedt
        self.prev_dedt = self.now_dedt

        # Get the state values now:
        self.now_signal = signal
        self.now_iedt = self.prev_iedt

        e = target - self.now_signal

        prev_e = target - self.prev_signal

        self.now_dedt = (e - prev_e) / dt
        self.now_iedt += dt * (e + prev_e) / 2.0

        value = self.kP * e + self.kI * self.now_iedt + self.kD * self.now_dedt + self.k0
        # Keep the value within the specified limits (if any):
        value = max(self.MinValue, min(value, self.MaxValue))

        # print('signal = %f, , e = %f, dedt = %f, iedt = %f, v= %f' % (signal, e, self.now_dedt, self.now_iedt, value))

        return value
