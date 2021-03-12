import os, sys
import json
import platform, subprocess, re
from psutil import virtual_memory

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from setting import *

def get_cpu_number(data):
	return int(data["CPU(s)"])

def get_cpu_thread_number(data):
	return int(data["Core(s)_per_socket"]) * int(data["Socket(s)"]) * int(data["Thread(s)_per_core"])

def get_cpu_core_number(data):
	return int(data["Core(s)_per_socket"]) * int(data["Socket(s)"])

def get_cpu_socket(data):
	return int(data["Socket(s)"])

def get_cpu_all_info():
	# For linux
	data = {}
	if platform.system() == "Linux":
		all_info = subprocess.check_output(COMMAND_CPU_LINUX_LS, shell=True).strip()

		for line in all_info.decode("utf-8").split("\n"):
			type_, value = line.split(":")[0].replace(" ","_"), line.split(":")[1].replace(" ","")
			data[type_] = value
	else:
		print("May be the others OS.")
		return ""
	return data

def get_special_processor(ProcessorId):
	if platform.system() == "Linux":
		all_info = subprocess.check_output(COMMAND_CPU_LINUX_CAT, shell = True).strip()
		index = 0
		data = {}
		for line in all_info.decode("utf-8").split("\n"):
			if not line:
				index += 1
			elif ProcessorId < index:
				break			

			elif ProcessorId == index:
				type_, value = line.split(":")[0].replace(" ","_"), line.split(":")[1].replace(" ","")
				data[type_] = value
			else:
				pass

		return data
	else:
		print("May be the others OS.")

def get_memory_number(data):
	return len(data)

def get_memory_all_info():
	if platform.system() == "Linux":
		arr_memory_info = []
		info = subprocess.check_output("dmidecode -t memory | grep -A16 'Memory Device'", shell=True).strip()
		str_infos = (info.decode('utf-8')).split("--")

		for str_info in str_infos:
			
			if not "No Module Installed" in str_info:
				dict_memory_info = {}	
				for data in str_info.split("\n\t")[1:]:
					key, value = data.split(":")
					dict_memory_info[key] = value
				arr_memory_info.append(dict_memory_info)
			else:
				break
		return arr_memory_info	

		exist_memory = [memory  for memory in info.decode("utf-8").split("\n\t") if "MB" in memory ]
		print(exist_memory)
	else:
		print("May be the others OS.")
		return ""


if __name__ == "__main__":
	data = get_cpu_all_info()
	CPU_length = get_cpu_number(data)
	Core_length = get_cpu_core_number(data)
	Socket_length = get_cpu_socket(data)
	Thread_length = get_cpu_thread_number(data)

	print("\n------------------------------------------------")
	print("CPU(s): ", CPU_length)
	print("Core(s): ", Core_length)
	print("Socket(s): ", Socket_length)
	print("Thread(s): ", Thread_length)

	print("\n------------------------------------------------")
	arr_data = get_memory_all_info()
	Memory_length = get_memory_number(arr_data)

	print("Memory(s): ",Memory_length)
	print("Form factory: ", data[0]["Form Factor"])
