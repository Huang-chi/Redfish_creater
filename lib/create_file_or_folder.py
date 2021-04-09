import os
import json

from setting import *
from CPU_info import get_cpu_info
from CPU_info import get_cpu_number
from mem_info import get_mem_info
from mem_info import get_mem_number

def create_index_json(path, data):
	try:
		with open(os.path.join(path, INFO_FILENAME), 'w', newline='') as f:
			json.dump(data, f, indent = 4)
		print("##### (index.json) Successful !!")
	except Exception as e:
		print(e)

def search_device_info(path):
	final_path = []
	# For each different device, there is corresponding function
	# For CPU
	if "ProcessorId" in path:
		print("# ProcessorId")
		final_path  = create_dynamic_CPU_folder(path)
	# For Memory
	elif "Memory" in path:
		print("# Memory")
		final_path  = create_dynamic_Memory_folder(path)
	else:
		final_path  = create_dynamic_Memory_folder(path)
		print("Pass")
		
	print("Final_path: ", final_path)
	return final_path
	

def create_dynamic_Memory_folder(path):
	temp_path = []
	arr_data = get_mem_info()
	Memory_length = get_mem_number(arr_data)
	
	print("Memory(s): ",Memory_length)
	print("Form factor: ", arr_data[0]["Form Factor"])

	target_path = path.split("{")[0]

	for index in range(1,Memory_length+1):
		temp_path.append(os.path.join(target_path, "DIMM"+str(index)))

	return temp_path

def create_dynamic_CPU_folder(path):
	temp_path = []
	info_index = 0

	if "{" in path and "}" in path:
		cpu_data = get_cpu_info()
		info_index = get_cpu_number(cpu_data)
	
	target_path = path.split("{")[0]
	
	for index in range(1,info_index+1):
		temp_path.append(os.path.join(target_path,"CPU"+str(index)))

	return temp_path
