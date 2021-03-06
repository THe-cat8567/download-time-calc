#! /usr/bin/python

import sys
import subprocess
import time

# general loop function
def loop(function):	
	SUCESS = 1
	REPEAT = 0
	TRY_AGAIN_PROMPT = "Please try again"
	
	while SUCESS == 1:
		if REPEAT == 1:
			time.sleep(2)
			subprocess.run(['clear', '-x'])
			print(TRY_AGAIN_PROMPT)
			SUCESS = function()
		elif REPEAT == 0:
			SUCESS = function()
		REPEAT = 1

# get file unit (MB/GB)
def get_file_unit():
	units = ["MB", "MEGABYTE", "GB", "GIGABYTE"]
	print("Which file size unit to use?\n")
	print("- %s (%s)\n" % (units[1], units[0]))
	print("- %s (%s)\n" % (units[3], units[2]))
	global FILE_UNIT
	FILE_UNIT = input()

	if FILE_UNIT.upper() in units:
		FILE_UNIT = FILE_UNIT.upper()
	else:
		print("Sorry %s is not a known file unit" % (FILE_UNIT.upper()))
		return(1)

# get file number size
def get_file_number_size():
	print("What is the file size (positive whole integer) (%s)" % (FILE_UNIT)) 
	global FILE_SIZE
	FILE_SIZE = input()

	try:
		float(FILE_SIZE)
	except:
		print("Sorry %s is a non positive whole integer value" % (FILE_SIZE))
		return(1)

# get internet speed
def get_internet_speed():
	print("Please enter the internet download speed in Megabits (positive whole integer)")
	print("Leave empty and enter for the download speed to be found by the script via a speedtest")
	global INTERNET_DOWNLOAD_SPEED
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
			def manual_download_speed():
				print("Please enter the internet download speed in Megabits (positive whole integer)")
				INTERNET_DOWNLOAD_SPEED = input()
				try:
					float(INTERNET_DOWNLOAD_SPEED)
				except:
					print("Sorry %s is a non positive whole integer value" % (INTERNET_DOWNLOAD_SPEED))
					return(1)
			loop(manual_download_speed)
	else:
		try:
			float(INTERNET_DOWNLOAD_SPEED)
		except:
			print("Sorry %s is a non positive whole integer value" % (INTERNET_DOWNLOAD_SPEED))
			return(1)
		
	# Megabits to Megabytes
	INTERNET_DOWNLOAD_SPEED_MEGABYTES = int(INTERNET_DOWNLOAD_SPEED) / 8
	INTERNET_DOWNLOAD_SPEED = INTERNET_DOWNLOAD_SPEED_MEGABYTES
	
# calculate the times
def print_result():
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

def main():
	# handle the (lack thereof) args passed to the script
	if len(sys.argv) == 1:
		# fully interactive
		loop(get_file_unit)
		loop(get_file_number_size)
		loop(get_internet_speed)
	else:
		# parse args:
		# --file-unit --file-size --download-speed
		args = ['--file-unit', '--file-size', '--download-speed']
		FILE_UNIT_SET = 0
		FILE_SIZE_SET = 0
		INTERNET_DOWNLOAD_SPEED_SET = 0
		for a in sys.argv:
			if a in args:
				arg_position = sys.argv.index(a)
				arg_arg_position = int(arg_position) + 1
				try:
					arg_arg_value = sys.argv[arg_arg_position]
				except:
					print("%s is not given a argument, exiting" % (a))
					exit(1)
			if a == args[0]:
				global FILE_UNIT
				FILE_UNIT = arg_arg_value
				FILE_UNIT_SET = 1
			elif a == args[1]:
				global FILE_SIZE
				FILE_SIZE = arg_arg_value
				FILE_SIZE_SET = 1
			elif a == args[2]:
				global INTERNET_DOWNLOAD_SPEED
				INTERNET_DOWNLOAD_SPEED = int(arg_arg_value)
				INTERNET_DOWNLOAD_SPEED_SET = 1

		if FILE_UNIT_SET != 1:
			loop(get_file_unit)
		elif FILE_SIZE_SET != 1:
			loop(get_file_number_size)
		elif INTERNET_DOWNLOAD_SPEED_SET != 1:
			loop(get_internet_speed)
			
	# print results
	print_result()

# main program
# handle Ctrl-C
try:	
	main()
except KeyboardInterrupt:
	print("Ctrl-C detected, exiting now")
	exit(0)
