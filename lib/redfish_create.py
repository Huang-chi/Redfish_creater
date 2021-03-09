import json, os
import collections

from setting import*
from redfish_get import *
from create_file_or_folder import *
from get_component_info import *

'''
def create_property(data, _properties):
	
	for attr_name in _properties:
		resource_name, resource_attr_name = get_reference_resource_and_attr(_properties, attr_name) 
		if __debug__:
			print("### Resource_name: ", resource_name)
			print("### Resource_attr_name: ", resource_attr_name)	
			print("### Attr_name: ", attr_name)

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
		resource_name, resource_attr_name = get_reference_resource_and_attr(_navigation_properties, attr_name)
		if __debug__:	
			print("Attr_name: ",attr_name)		
	
		attr_property = get_entity_property(attr_name, resource_attr_name, resource_name)
	
		if __debug__:
			print("@-------->",attr_property)	
	
		if attr_property != "":	
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
	# There is question about the content of attribute for "Member"(2/8)
	if 'Members' not in _navigation_properties and 'Members' not in _properties:
		data["Id"] = odata_id.split('/')[-1]
	else:
		data["Members@odata.count"] = 0	
	data["Description"] = ""
	data = create_property(data, _properties)
	data = create_navigation_property(data, _navigation_properties)
	data["@odata.id"] = odata_id
	data[COPYRIGHT] = COPYRIGHT_CONTENT
	
	return data
'''
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
'''
def create_redfish_data(odata_type, redfish_data, uri):
	print("############################################\n")

	if __debug__:
		print("### Redfish data: ",redfish_data)
		print("### Odata_type: ", odata_type)

	attr_properties, attr_navigation_properties, collection_path = get_all_property(odata_type, odata_type)
	
	redfish_path, collection_path[0] = get_odata_id(collection_path[0])

	data = create_index_json_content(redfish_data, collection_path[0], attr_properties, attr_navigation_properties)

	print("redfish: ",redfish_path)
	create_index_json(redfish_path[0], data)

'''
