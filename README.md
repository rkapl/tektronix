This program allows you to pull samples over USB from your Tektronix oscilloscope
(tested with TDS2014B, but others should be compatible). The data is in CSV form
and can then be plotted using gnuplot.

You do all your setup (trigers, volts per div, position etc.) on the
oscilloscope. This program then just acquires the samples.  I've also played
with the idea of adding tektronix support to Sigrok, but I've realized I prefer
this style of work.

To run this program:
 - install usbtmc `pip install python-usbtmc`
 - install gnuplot
 - connect the oscilloscope using USB
 - make sure the permissions are right for the USB device (either by udev rules
   or by `chown $USER -r /dev/bus/usb/<your-scope>`)

Setup your scope, stop it, and acquire and plot the data by running:

     bin/tektronix --channels 1,2 test-data

The samples from channels 1 and 2 will be saved to directory `test-data` and
plotted using gnuplot.

By default, the produced gnuplot is similar to what your oscilloscope shows: it
uses the per-channel volts per divisions and horizontal offsets. Just beware
that the divisions do not yet properly match the y axis ticks in the graph.

Alternative mode can also be requested by using `--scope-like no`. You can
re-render an already acquired data directory by using `--acquire no`.
