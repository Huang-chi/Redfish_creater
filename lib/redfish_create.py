import json, os
import collections

from setting import*
from redfish_get import *
from create_file_or_folder import *

def create_property(data, _properties):
	
	for attr_name in _properties:
		resource_name, resource_attr_name = get_reference_resource_and_attr_name(_properties, attr_name) 
		
		# Property
		if resource_name == "Edm":
			data[attr_name] = ""
		
		# Reference
		else:
			attr_property = get_entity_property(attr_name, resource_attr_name, resource_name)
			if 'Collection(' in _properties[attr_name]:
				dict_add_list = []
				dict_add_list.append(attr_property)
				data[attr_name] = dict_add_list
			else:
				data[attr_name] = attr_property
		
	return data

def create_navigation_property(data, _navigation_properties):
	
	for attr_name in _navigation_properties:
		resource_name, resource_attr_name = get_reference_resource_and_attr_name(_navigation_properties, attr_name)
		
		attr_property = get_entity_property(attr_name, resource_attr_name, resource_name)
		if 'Collection' in _navigation_properties[attr_name]:
			temp = []
			temp.append(attr_property)
			data[attr_name] = temp
		else:
			data[attr_name] = attr_property
					
	return data

def create_index_json_content(response, odata_id, _properties, _navigation_properties):
	
	data = collections.OrderedDict()
	data["@odata.type"] = response['@odata_type']
	data["Name"] = ""
	
	if 'Members' not in _navigation_properties:
		data["Id"] = odata_id.split('/')[-1]
	else:
		data["Members@odata.count"] = 0	
	data["Description"] = ""
	data = create_property(data, _properties)
	data = create_navigation_property(data, _navigation_properties)
	data["@odata.id"] = odata_id
	data[COPYRIGHT] = COPYRIGHT_CONTENT
	
	return data

def create_collection(response):
	Collections = []
	Collection = ''
	
	for key in response.keys():
		if "@odata.id" in response[key]:
			URI = response[key]["@odata.id"]
			Collection = os.path.join(REDFISH_DATA,URI.split('/')[-1])
			print(Collection)
			create_folder(Collection)
			Collections.append(Collection)
	return Collections

def create_entity(path):
	response = get_entry(path)
	entities = {}
	for entry in response['navlinks']:
		if 'navlinks' in entry:
			entry_name = entry['navlinks'][0]['target']
			print("### :", entry_name)
			Collection = os.path.join(os.path.join(REDFISH_DATA,entry['target']),entry_name)
			print("---->: ", Collection)
			entities[Collection.split("/")[-2]] = Collection
			create_folder(Collection)			
	return entities

def create_redfish_data(odata_type, redfish_data):
	attr_properties, attr_navigation_properties, collection_path = get_all_property(os.path.join(RESOURCE_XML_PATH, odata_type+"_v1.xml"), odata_type)
	redfish_path, collection_path[0] = get_odata_id(collection_path[0])

	data = create_index_json_content(redfish_data, collection_path[0], attr_properties, attr_navigation_properties)
	create_index_json(redfish_path, data)


