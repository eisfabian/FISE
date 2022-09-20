# Fast Incremental Single Exposure (FISE) tilt series acquisition scripts

Please refer to the [publiciation](https://doi.org/10.1016/j.jsb.2019.08.006) for more details! 

Also check the [original FISE approach](https://doi.org/10.1016/j.jsb.2018.12.008) by the Jensen lab!

### SerialEM scripts for use with FISE tilt series acquisition:

<b>[FISEtomo.txt](https://github.com/eisfabian/FISE/blob/master/FISETomo.txt)</b> - SerialEM script used for FISE tilt series acquisition

<b>[CalFISE.txt](https://github.com/eisfabian/FISE/blob/master/CalFISE.txt)</b> - SerialEM script to run calibration tilt series for specimen shifts and defocus gradient.

<b>[extractTiltStacks.py](https://github.com/eisfabian/FISE/blob/master/extractTiltStacks.py)</b> - Python script used on output frame stacks from FISEtomo SerialEM script. Also requires *_saved.txt (File with list of saved frames).

<b>[sortByTilt.py](https://github.com/eisfabian/FISE/blob/master/sortByTilt.py)</b> - Python script used to sort tilt stack by tilt angle. Requires .mdoc file or FISE_tilts.txt for tilt angle input.



### <i>WARNING:</i> 
- These scripts were used mainly for dose-symmetric 3° increment tilt series. If you have trouble with other schemes, please let me know! 
- If you plan on using small pixel sizes (<2 Å/px), the loss of FOV might be too big to obtain usable data.
- If you have any questions, don't hesitate to contact me!
