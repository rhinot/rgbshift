#!/usr/bin/python

"""rgbshift.py: Update RGB strip to the color temperature & brightness befitting the environment"""
# For more information on redshift, see https://github.com/jonls/redshift/

__author__      = "Ryan Tabone (hit.ryan.up [at] gmail.com)"
__copyright__   = "Copyright MMXVII, Ryan Tabone"

# -----------------------------------------------------
# File        rgbshift.py
# Authors     Ryan Tabone
# License     GPLv3
# Web         https://github.com/rhinot/rgbshift
# -----------------------------------------------------
# 
# Copyright (C) 2017 Ryan Tabone
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#  
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

##### IMPORTS #####
# Import 1st party

# Import 3rd party
# import pigpio
import redshift_lite


##### DEFAULT VARIABLES #####
# Pin mapping from RPi to RGB strip
RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24


bright = 255
r = 255.0
g = 0.0
b = 0.0




#pi = pigpio.pi()



##### CLASS DEFINITIONS #####
# Set brightness of led at pin - forked from https://github.com/dordnung/raspberrypi-ledstrip/blob/master/fading.py
def setLights(pin, brightness):
	realBrightness = int(int(brightness) * (float(bright) / 255.0))
	pi.set_PWM_dutycycle(pin, realBrightness)


# Get color temperature & brightness, given time of day and location
def getColor():
	temperature = redshift_lite.get_current_color()[0]
	brightness = redshift_lite.get_current_color()[1]

	return(temperature,brightness)


temperature,brightness=getColor()
print temperature
print brightness







