#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
import time

from jataruku import PID


class SimpleHeater(object):
    """
    Simulation of a system containing a heater and a tank of (inexhaustible) water.
    Intended for basic testing of PID algorithms.
    This heater can either be off or on, so could be controlled with PWM.
    """

    def __init__(self):
        self._heat_lost_to_radiation_per_second = 0.25  # in degrees Celsius
        self._heat_gained_per_second_when_heating = 5.0  # in degrees Celsius
        self._temperature_max = 100  # We are simulating water, which will never get hotter than 100C.

        self._ambient_temperature = 18.0  # in degrees Celsius
        self._heating = False
        self._temperature = self._ambient_temperature
        self._timestamp = datetime.datetime.now()  # When we last turned on the heater, or updated _temperature while heating.

    def _update_temperature(self):
        now = datetime.datetime.now()
        elapsed_time = now - self._timestamp
        elapsed_seconds = elapsed_time.total_seconds()

        # over this period we have lost some heat and, if we are heating, gained some heat.
        # a more real answer would probably require us to get fancy with math, but we don't actually care.

        new_temperature = self._temperature - self._heat_lost_to_radiation_per_second * elapsed_seconds
        if self.heating:
            new_temperature += self._heat_gained_per_second_when_heating * elapsed_seconds

        if new_temperature > self._temperature_max:
            new_temperature = self._temperature_max
        elif new_temperature < self._ambient_temperature:
            new_temperature = self._ambient_temperature

        self._temperature = new_temperature
        self._timestamp = now

    @property
    def temperature(self):
        self._update_temperature()
        return self._temperature

    @property
    def heating(self):
        return self._heating

    @heating.setter
    def heating(self, value):
        new_heating = value is not False and value != 0
        if new_heating != self._heating:
            print "* Heat is {}".format("ON" if new_heating else "OFF")
            self._update_temperature()
            self._heating = new_heating



def test_1():
    start_time = datetime.datetime.now()
    heater = SimpleHeater()
    heater_temperature = lambda: heater.temperature
    def heater_set_output(x):
        heater.heating = x

    set_point = 88

    PID_PARAMS = dict(large_gap=dict(kp=4, ki=0.2, kd=1),
                      small_gap=dict(kp=1, ki=0.05, kd=0.25))

    LARGE_GAP_TEMPERATURE = 10

    def has_large_gap():
        return abs(heater.temperature - set_point) >= LARGE_GAP_TEMPERATURE

    if has_large_gap():
        pid_params = PID_PARAMS['large_gap']
        set_for_large_gap = True
    else:
        pid_params = PID_PARAMS['small_gap']
        set_for_large_gap = False

    pid = PID(heater_temperature, heater_set_output, set_point, pid_params['kp'], pid_params['ki'], pid_params['kd'], True)
    pid.set_output_limits(0, 1)
    pid.auto = True
    for x in xrange(0,100000):
        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        pid.compute()
        if x % 1000 == 0:
            print "Elapsed time: {}; temperature: {:.2f}".format(elapsed_time, heater.temperature)
        if has_large_gap():
            if not set_for_large_gap:
                print "* RETUNING FOR LARGE GAP"
                pid_params = PID_PARAMS['large_gap']
                pid.set_tunings(pid_params['kp'], pid_params['ki'], pid_params['kd'])
                set_for_large_gap = True
        elif set_for_large_gap:
            print "* RETUNING FOR SMALL GAP"
            pid_params = PID_PARAMS['small_gap']
            pid.set_tunings(pid_params['kp'], pid_params['ki'], pid_params['kd'])
            set_for_large_gap = False
        time.sleep(0.001)


def test_0():
    start_time = datetime.datetime.now()
    heater = SimpleHeater()

    def show_heater_status():
        elapsed_seconds = int((datetime.datetime.now() - start_time).total_seconds() + 0.005)
        print "Elapsed time: {}; temperature: {:.2f}".format(elapsed_seconds, heater.temperature)

    for x in xrange(0,5):
        show_heater_status()
        time.sleep(1.0)
    print "* STARTING TO HEAT"
    heater.heating = True
    for x in xrange(0, 20):
        show_heater_status()
        time.sleep(1.0)
    print "* NO MORE HEAT"
    heater.heating = False
    for x in xrange(0, 10):
        show_heater_status()
        time.sleep(1.0)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        which_test = 0
    else:
        which_test = int(sys.argv[1])

    if which_test == 0:
        test_0()
    elif which_test == 1:
        test_1()
    else:
        print "No test #{}".format(which_test)
