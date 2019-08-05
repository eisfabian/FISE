# FISE scripts
Scripts for use with FISE tilt series acquisition:

FISEtomo - SerialEM script used for FISE tilt series acquisition

CalFISE - SerialEM script to run calibration tilt series for specimen shifts and defocus gradient.

extractTiltStacks.py - Python script used on output frame stacks from FISEtomo SerialEM script. Also requires *_saved.txt (File with list of saved frames).

sortByTilt.py - Python script used to sort tilt stack by tilt angle. Requires .mdoc file or FISE_tilts.txt for tilt angle input.
