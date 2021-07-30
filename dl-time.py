#! /usr/bin/python

import sys
import subprocess

# get file unit (MB/GB)
units = ["MB", "MEGABYTE", "GB", "GIGABYTE"]
print("Which file size unit to use?\n")
print("- %s (%s)\n" % (units[1], units[0]))
print("- %s (%s)\n" % (units[3], units[2]))
FILE_UNIT = input()

if FILE_UNIT.upper() in units:
	FILE_UNIT = FILE_UNIT.upper()
else:
	print("Sorry %s is not a known file unit" % (FILE_UNIT.upper()))
	exit(1)

# get file number size
print("What is the file size (positive whole integer) (%s)" % (FILE_UNIT)) 
FILE_SIZE = input()

try:
	float(FILE_SIZE)
except:
	print("Sorry %s is a non positive whole integer value" % (FILE_SIZE))

# get internet speed
print("Please enter the internet download speed in Megabits (positive whole integer)")
print("Leave empty and enter for the download speed to be found by the script via a speedtest")
INTERNET_DOWNLOAD_SPEED = input()

if INTERNET_DOWNLOAD_SPEED == "":
	# use `speedtest-cli`
	try:
		print("Trying speedtest")
		dl_speed = subprocess.run(['speedtest-cli', '--single', '--simple', '--no-upload'], capture_output=True)
		# parse for just the whole number
		dl_speed_category = str(dl_speed.stdout).split(':')
		dl_speed_download = dl_speed_category[1]
		dl_speed_value = str(dl_speed_download).split(' ')
		dl_speed_pre = dl_speed_value[1]
		# do not know if `speedtest-cli` even returns a non fractional value
		# just to be safe
		if dl_speed_pre.find(".") != -1:
			dl_speed_fractional = dl_speed_pre.split('.')
			INTERNET_DOWNLOAD_SPEED = dl_speed_fractional[0]
		else:
			INTERNET_DOWNLOAD_SPEED = dl_speed_pre
	except:
		print("Sorry the internet speedtest could not be completed")
		print("Please enter it in manually")
else:
	try:
		float(INTERNET_DOWNLOAD_SPEED)
	except:
		print("Sorry %s is a non positive whole integer value" % (INTERNET_DOWNLOAD_SPEED))
		
# Megabits to Megabytes
INTERNET_DOWNLOAD_SPEED_MEGABYTES = int(INTERNET_DOWNLOAD_SPEED) / 8
INTERNET_DOWNLOAD_SPEED = INTERNET_DOWNLOAD_SPEED_MEGABYTES

# calculate the times

def print_times(inital_unit, inital_size, download_speed, seconds):
	seconds_int = seconds
	seconds = str(seconds_int)
	MINUTES_DL = int(seconds) / 60
	MINUTES_DL_pre = str(MINUTES_DL)
	MINUTES_DL = MINUTES_DL_pre
	
	# whole numbers only (no rounding)
	if seconds.find(".") != -1:
		seconds_pre = seconds.split(".")
		seconds_proper = seconds_pre[0]
		seconds = seconds_proper
	if MINUTES_DL.find(".") != -1:
		MINUTES_DL_pre = MINUTES_DL.split(".")
		MINUTES_DL_proper = MINUTES_DL_pre[0]
		MINUTES_DL = MINUTES_DL_proper
	print("A file that is %s(%s) would take:" % (inital_size, inital_unit))
	print("%s seconds or %s minutes" % (seconds, MINUTES_DL))
	print("With a connection speed of %s megabytes per second" % (INTERNET_DOWNLOAD_SPEED))
	
if FILE_UNIT == "MB":
	SECONDS_DL = int(FILE_SIZE) / INTERNET_DOWNLOAD_SPEED
	SECONDS_DL_pre = str(SECONDS_DL).split(".")
	SECONDS_DL = int(SECONDS_DL_pre[0])
	print_times(FILE_UNIT, FILE_SIZE, INTERNET_DOWNLOAD_SPEED, SECONDS_DL)
elif FILE_UNIT == "GB":
	GB_MB_FILE_SIZE = int(FILE_SIZE) * 1000
	SECONDS_DL = GB_MB_FILE_SIZE / INTERNET_DOWNLOAD_SPEED
	SECONDS_DL_pre = str(SECONDS_DL).split(".")
	SECONDS_DL = int(SECONDS_DL_pre[0])
	print_times(FILE_UNIT, FILE_SIZE, INTERNET_DOWNLOAD_SPEED, SECONDS_DL)
