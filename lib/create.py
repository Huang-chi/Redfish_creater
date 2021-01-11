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
		resource_name, property_name = _properties[attr_name].split('.')[0], _properties[attr_name].split('.')[-1]
		print(resource_name, property_name)
		
		# Property
		if resource_name == "Edm":
			print("#### data[attr_name]: ",attr_name)
			data[attr_name] = ""
		
		# Reference
		elif resource_name != "Edm" :
			attr_property = get_inside_property(data, attr_name, resource_name)
			
			_property = {}
			print("### attr_name: ", attr_name,"(",__file__,")")
			#for C_property in attr_property:
			#	_property[C_property['Name']] = ""
			data[attr_name] = _property
		
		else:
			print("Error: Cann't identify the type.") 
	
	print("\n#########")
	print(data)
	print("\n#########")
		
	return data

def create_navigation_property(data, _navigation_properties, paths):
	print("### _navigation :", _navigation_properties)
	print("### paths :", paths)
	for attr_name in _navigation_properties:
		if 'Collection' in _navigation_properties[attr_name]:
			 temp_list = []
			 _type = _navigation_properties[attr_name].split('(')[-1][:-1]
			 resource_name, property_name = _type.split('.')[0], _type.split('.')[-1]
		else:
			resource_name, property_name = _navigation_properties[attr_name].split('.')[0], _navigation_properties[attr_name].split('.')[-1]
		print("\n#########:",resource_name, data['Id'], property_name)
		data[attr_name] = get_inside_property(data, property_name, resource_name)

		print("\n#########")
		print(data)
		print("#########\n")
		break
			
			
	return data

def create_content(response, odata_id, _properties, _navigation_properties, entities = None):
	data = collections.OrderedDict()
	data["@odata.type"] = response['@odata_type']
	data["Id"] = response['@odata_type'].split('.')[0][1:]
	data["Name"] = ""
	data["Description"] = ""
	data = create_property(data, _properties)
	#data = create_navigation_property(data, _navigation_properties, odata_id)

		
	data["@odata.id"] = odata_id
	data[COPYRIGHT] = COPYRIGHT_CONTENT
	 
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

