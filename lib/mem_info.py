import os, sys
import json
import platform, subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from setting import *


def get_mem_number(data):
	return len(data)

def get_mem_info():
	if platform.system() == "Linux":
		arr_mem_info = []
		info = subprocess.check_output("dmidecode -t memory | grep -A16 'Memory Device'", shell=True)
		
		str_datas = (info.decode('utf-8')).split("--")
		for str_data in str_datas:
			if not "No Module Installed" in str_data:
				dict_mem = {}
				for data in str_data.split("\n\t")[1:]:
					key, value = data.split(":")
					dict_mem[key] = value
				arr_mem_info.append(dict_mem)
			else:
				break
		return arr_mem_info
	else:
		print("May be the other OS.")
		return -1

if __name__ == "__main__":
	arr_data = get_mem_info()
	mem_len = get_mem_number(arr_data)
	
	print("Mem number: ", mem_len)
	print("Mem Type: ", arr_data[0]["Type"])
	print("Mem DataWidthBits: ", arr_data[0]["Data Width"])
	print("Mem BusWidthBits: ", arr_data[0]["Total Width"])
	print("Mem Size: ", arr_data[0]["Size"])
	print("Mem slot: ", arr_data[0]["Locator"].split(" ")[1:])

