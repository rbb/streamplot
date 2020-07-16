# streamplot

A Python (3) script to plot streaming data.

The idea is to be able to send data with command line tools like netcat or
socat, to a server, as CSV or similar delimited data, and have a plot show up on
a remote computer.

# Files

* asiosend.py: send some random data, as an example generator. It can optionally
  send data from a file, at a fixed interval.
* asyncecho.py: Example of receiver of data. It just prints what it receives
* streamplot.py: Use matplotlib to plot received data
