import os
import json

from setting import *
from get_component_info import *

def create_index_json(path, data):
	try:
		with open(os.path.join(path, INFO_FILENAME), 'w', newline='') as f:
			json.dump(data, f, indent = 4)
		print("##### (index.json) Successful !!")
	except Exception as e:
		print(e)
'''
def create_folder(path, target=None):
	final_path = []
	print("--------------->Path: ", path)
	
	if path.find("{") != -1:
		# For each different device, there is corresponding function
		# For CPU
		if "ProcessorId" in path:
			final_path  = create_dynamic_CPU_folder(path)
		# For Memory
		elif "Memory" in path:
			final_path  = create_dynamic_Memory_folder(path)
		else:
			final_path  = create_dynamic_Memory_folder(path)
			print("Pass")
			pass
	else:
		final_path.append(path)
		
	for	temp in final_path:
		try:	
			if not os.path.isdir(temp):
				print("Path: ", temp)
				os.mkdir(temp)
				print("##### (create folder) Successful !!\n")
		except:
			print("The folder is exist.\n")
		
	return final_path
'''

def search_device_info(path):
	# For each different device, there is corresponding function
	# For CPU
	if "ProcessorId" in path:
		final_path  = create_dynamic_CPU_folder(path)
	# For Memory
	elif "Memory" in path:
		final_path  = create_dynamic_Memory_folder(path)
	else:
		final_path  = create_dynamic_Memory_folder(path)
		print("Pass")
		pass
	print("Final_path: ", final_path)
	return final_path
	

def create_dynamic_Memory_folder(path):
	temp_path = []
	temp_path.append("Pass")
	return temp_path

def create_dynamic_CPU_folder(path):
	temp_path = []
	info_index = 0

	if "{" in path and "}" in path:
		cpu_data = get_cpu_all_info()
		info_index = get_cpu_number(cpu_data)
	
	target_path = path.split("{")[0]
	
	for index in range(1,info_index+1):
		temp_path.append(os.path.join(target_path,"CPU"+str(index)))

	return temp_path
