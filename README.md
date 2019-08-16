# FISE scripts
Scripts for use with FISE tilt series acquisition:

<b>FISEtomo.txt</b> - SerialEM script used for FISE tilt series acquisition

<b>CalFISE.txt</b> - SerialEM script to run calibration tilt series for specimen shifts and defocus gradient.

<b>extractTiltStacks.py</b> - Python script used on output frame stacks from FISEtomo SerialEM script. Also requires *_saved.txt (File with list of saved frames).

<b>sortByTilt.py</b> - Python script used to sort tilt stack by tilt angle. Requires .mdoc file or FISE_tilts.txt for tilt angle input.

<p></p>
<b><i>WARNING:</i></b> 
- These scripts were used mainly for dose-symmetric 3° increment tilt series. If you have trouble with other schemes, please let me know! 
- If you plan on using small pixel sizes (<2 Å/px), the loss of FOV might be too big to obtain usable data.
- If you have any questions, don't hesitate to contact me!
