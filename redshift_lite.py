#!/usr/bin/python

"""redshift_lite.py: A light version of redshift, written in Python"""
# For more information on redshift, see https://github.com/jonls/redshift/

__author__      = "Ryan Tabone (hit.ryan.up [at] gmail.com)"
__copyright__   = "Copyright MMXVII, Ryan Tabone"

# -----------------------------------------------------
# File        redshift_lite.py
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
from datetime import datetime
import json
import math
import requests

# Import 3rd party
from astral import Astral





##### DEFAULT VARIABLES #####
# Default values for temperature & brightness.
DEFAULT_DAY_TEMP =  5500   # Sun @ Noon
DEFAULT_NIGHT_TEMP = 2700  # Incandescent
DEFAULT_BRIGHTNESS = 1.0
DEFAULT_DAY_BRIGHTNESS = DEFAULT_BRIGHTNESS
DEFAULT_NIGHT_BRIGHTNESS = 0.3

# The color temperature when no adjustment is applied.
#NEUTRAL_TEMP = 6500

# Solar variables
# Model of atmospheric refraction near horizon (in degrees).
#SOLAR_ATM_REFRAC = 0.833

#SOLAR_ASTRO_TWILIGHT_ELEV = -18.0
#SOLAR_NAUT_TWILIGHT_ELEV  = -12.0
SOLAR_CIVIL_TWILIGHT_ELEV = -6.0
#SOLAR_DAYTIME_ELEV = (0.0 - SOLAR_ATM_REFRAC)


# Angular elevation of the sun at which the color temperature
# transition period starts and ends (in degress).
# Transition during twilight, and while the sun is lower than
# 3.0 degrees above the horizon.

TRANSITION_LOW = SOLAR_CIVIL_TWILIGHT_ELEV
TRANSITION_HIGH =  3.0

# Duration of sleep between screen updates (milliseconds).
SLEEP_DURATION = 5000
SLEEP_DURATION_SHORT = 100





##### CLASS DEFINITIONS #####
# Class for storing location in latitude and longitude
class location:
	def __init__(self):
		self.lat = None
		self.lon = None

# Class for storing temperature, gamma & brightness at time t
class color_setting_t:
	def __init__(self):
		self.temperature = None
		# self.gamma = [DEFAULT_GAMMA] * 3
		self.brightness = DEFAULT_BRIGHTNESS

class transition_scheme_t:
	def __init__(self):
		self.high = TRANSITION_HIGH
		self.low = TRANSITION_LOW
		self.day = color_setting_t()
		self.day.temperature = DEFAULT_DAY_TEMP
		self.night = color_setting_t()
		self.night.temperature = DEFAULT_NIGHT_TEMP
		self.night.brightness = DEFAULT_NIGHT_BRIGHTNESS






##### FUNCTIONS #####

# Conversion to radians
def RAD(num):
	return (num*(math.pi/180))



# Clamping function - value is now lower than low and no higher than high, otherwise, no change
def CLAMP(n,low,high):
	return max(low, min(n,high))



# Get current latitude and longitude, returned in tuple - [0] = lat; [1] = lon
def getlatlon(location):
	send_url = 'http://freegeoip.net/json'
	r = requests.get(send_url)
	j = json.loads(r.text)

	location.lat = j['latitude']
	#print location.lat
	location.lon = j['longitude']
	#print location.lon

	return (location)



# Determine what the color settings should be during transition
def interpolate_color_settings(transition, elevation, result):
	day = transition.day
	night = transition.night

	alpha = (transition.low - elevation) / (transition.low - transition.high)
	alpha = CLAMP(alpha,0.0,1.0)

	result.temperature = (1.0-alpha) * night.temperature + alpha * day.temperature
	result.brightness = (1.0-alpha) * night.brightness + alpha * day.brightness
	# for x in range(3) :
	#	result.gamma[x] = (1.0-alpha) * night.gamma[x] + alpha * day.gamma[x]



# Main function: Get the current temperature & brightness, given time & location
def get_current_color():
	# Get current angular elevation of the sun
	loc = getlatlon (location())
	sol_elev = Astral.solar_elevation(Astral(),datetime.utcnow(),loc.lat,loc.lon)

	#print sol_elev

	# Use elevation of sun to set color temperature
	scheme = transition_scheme_t()
	interp = color_setting_t()
	#print interp.temperature
	print interp.brightness
	interpolate_color_settings (scheme,sol_elev,interp)

	

	return (interp.temperature, interp.brightness)

test_vars = get_current_color()

#print test_vars[0]
print test_vars[1]


