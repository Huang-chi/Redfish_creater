import json, os
import collections

from setting import*
from get import *


def create_index(path, data):
	with open(os.path.join(path, INFO_FILENAME), 'w', newline='') as f:
		json.dump(data, f)

def create_dir(path):
	if not os.path.isdir(path):
		os.mkdir(path)

def create_property(data, _properties):
	
	for attr_name in _properties:
		resource_name, resource_attr_name = _properties[attr_name].split('.')[0], _properties[attr_name].split('.')[-1]
		print(resource_name, resource_attr_name)
		
		# Property
		if resource_name == "Edm":
			data[attr_name] = ""
		
		# Reference
		elif resource_name != "Edm" :
			attr_property = get_entity_property(attr_name, resource_attr_name, resource_name)
			data[attr_name] = attr_property
		
		else:
			print("Error: Cann't identify the type.") 
	
	print("\n#########")
	print(data)
	print("#########")
		
	return data

def create_navigation_property(data, _navigation_properties):
	print("### _navigation :", _navigation_properties)
	
	for attr_name in _navigation_properties:
		print(attr_name)
		resource_name, resource_attr_name = get_reference_resource_and_attr_name(_navigation_properties, attr_name)
		attr_property = get_entity_property(attr_name, resource_attr_name, resource_name)
		if 'Collection' in _navigation_properties[attr_name]:
			temp = []
			temp.append(attr_property)
			data[attr_name] = temp
		else:
			data[attr_name] = attr_property
					
	return data

def create_content(response, odata_id, _properties, _navigation_properties):
	data = collections.OrderedDict()
	data["@odata.type"] = response['@odata_type']
	data["Id"] = response['@odata_type'].split('.')[0][1:]
	data["Name"] = ""
	data["Description"] = ""
	data = create_property(data, _properties)
	data = create_navigation_property(data, _navigation_properties)
	data["@odata.id"] = odata_id
	data[COPYRIGHT] = COPYRIGHT_CONTENT
	
	#print("\n####### Final data ########")
	#print(data)

 
	return data

def create_conllection(response):
	Collections = []
	Collection = ''
	for key in response.keys():
		if "@odata.id" in response[key]:
			URI = response[key]["@odata.id"]
			Collection = os.path.join(REDFISH_DATA,URI.split('/')[-1])
			print(Collection)
			create_dir(Collection)
			Collections.append(Collection)
	return Collections

def create_entity(path):
	response = get_entry(path)
	entities = {}
	for entry in response['navlinks']:
		if 'navlinks' in entry:
			entry_name = entry['navlinks'][0]['target']
			print(entry_name)
			Collection = os.path.join(os.path.join(REDFISH_DATA,entry['target']),entry_name)
			print(Collection)
			entities[Collection.split("/")[-2]] = Collection
			create_dir(Collection)			
	return entities

def get_entry(path):
	response = ""
	with open(path, "r") as f:
		response= json.load(f)

	return response

