import json, os
import collections

from setting import*
from redfish_get import *
from create_file_or_folder import *
from get_component_info import *

def create_collection(response):
	Collection_set_array = []
	Collection_path = ''
	
	for key in response.keys():
		if "@odata.id" in response[key]:
			URI = response[key]["@odata.id"]
			Collection_path = os.path.join(REDFISH_DATA,URI.split('/')[-1])
			#print(Collection_path)
			#create_folder(Collection_path)
			Collection_set_array.append(Collection_path)
	return Collection_set_array

def create_entity(path):
	response = get_json_info(path)
	entities = {}
	for entry in response['navlinks']:
		if 'navlinks' in entry:
			entry_name = entry['navlinks'][0]['target']
			print("### :", entry_name)
			Collection = os.path.join(os.path.join(REDFISH_DATA,entry['target']),entry_name)
			print("---->: ", Collection)
			entities[Collection.split("/")[-2]] = Collection
			#create_folder(Collection)			
	return entities
