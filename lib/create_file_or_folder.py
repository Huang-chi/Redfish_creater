import os
import json

from setting import *

def create_index(path, data):
	with open(os.path.join(path, INFO_FILENAME), 'w', newline='') as f:
		json.dump(data, f, indent = 4)

def create_folder(path):
	if not os.path.isdir(path):
		os.mkdir(path)


