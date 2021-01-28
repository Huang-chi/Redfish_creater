import os
import json

from setting import *

def create_index_json(path, data):
	try:
		with open(os.path.join(path, INFO_FILENAME), 'w', newline='') as f:
			json.dump(data, f, indent = 4)
		#print("Successful !!")
	except Exception as e:
		print(e)

def create_folder(path):
	if not os.path.isdir(path):
		os.mkdir(path)
		#print("Successful !!")
	#else:
		#print("The folder is exist.")


