jataruku
========

This project provides a PID controller written in Python. It is based on 
[the Arduino PID code written by Brett Beauregard](https://github.com/br3ttb/Arduino-PID-Library).

Brett's code is the result of much research and thought on his part, which
he has [generously documented](http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/).
Most of what I did is translate it into a form which I hope can be easily
used if you are implementing a system in Python that wants to use PID
control.

How to Use
----------

The module exports only one object, a class called PID. The best way
to learn how to use it is to look at the test.py file (see below).

The second-best way to learn how to use it is to keep reading this
section.

The PID object must be constructed with the following parameters:

* ``input``: a lambda which reports the input value, e.g. the temperature of the object the temperature of which is being controlled

* ``output``: a function which controls the output setting, e.g. whether
  or not the heater is turned on or not. it takes a single parameter,
  which is the value that the output object should receive

* ``setpoint``: the target value for input, e.g. the desired temperature
  of the object in question

* ``kp``, ``ki``, and ``kd``: the three PID parameters.  (If you don't know
  what they are you should go read about how PIDs work, though you may
  be able to get away with using defaults based on the test code herein.)

* ``direct``: True if an increase in the output value will produce an
  increase in the input value, False otherwise

``pid = PID(input, output, setpoint, kp, ki, kd, direct)``

After the object has been created, just call ``pid.compute()`` as
frequently as possible, preferably via an interrupt of some sort. The
frequency required for good results will depend on the characteristics
of your entire system, but the default update frequency of 100
milliseconds is probably a good place to start. If the system is
working, then the input value will approach the set point and stay there.

Testing
-------

Since a PID is inherently real-time and dependent on external systems,
you can't really write code to test it quickly without decoupling it
from the wall clock or having an external system with which to integrate it.
In order to prove to myself that it basically works, I wrote a very simple
simulation of a heater attached to a tank of water, and some tests to
see what the PIDs behavior is when attached to the heater simulation.
The heater, when turned on, heats up at a certain rate, and if its
temperature is above the ambient temperature will
lose a certain amount of heat to the environment over time.

The first test should demonstrate that the dummy heater is basically working.

    test.py 0

The second test should demonstrate that the system can bring the water to
a given temperature and hold it there.

    test.py 1


Caveats
-------

This is basically first draft code and doesn't come with any module
setup niceties. Since the object is relatively straightforward there's
hardly any need. If this bothers you, go ahead and add them,
though it is not inconceivable that I would eventually get around to it
myself. Nevertheless, it should be usable as-is without too much
difficulty.

There are other PID features which could be added to make this even
better. I'm not even sure I know what they are. If you do, feel free
to write them and submit a pull request.

P.S. "jataruku" is a word in the Warlpiri language which according to
[the Australian Society for Indigenous Languages' Walpiri lexicon](http://ausil.org/Dictionary/Warlpiri/lexicon/index.htm) means
"stubborn, bullheaded, hot-tempered."
