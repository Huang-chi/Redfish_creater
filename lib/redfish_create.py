import json, os
import collections

from setting import*
from redfish_get import *
from create_file_or_folder import *
from get_component_info import *

def create_property(data, _properties):
	
	for attr_name in _properties:
		resource_name, resource_attr_name = get_reference_resource_and_attr_name(_properties, attr_name) 
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
		resource_name, resource_attr_name = get_reference_resource_and_attr_name(_navigation_properties, attr_name)
		if __debug__:	
			print("Attr_name: ",attr_name)		
	
		attr_property = get_entity_property(attr_name, resource_attr_name, resource_name)

		print("-------->",attr_property)	
		if attr_property != "":	
			print("@", attr_property)
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
	if __debug__:
		print("### Redfish data: ",redfish_data)
		print("### Odata_type: ", odata_type)

	attr_properties, attr_navigation_properties, collection_path = get_all_property(os.path.join(RESOURCE_XML_PATH, odata_type+"_v1.xml"), odata_type)
	redfish_path, collection_path[0] = get_odata_id(collection_path[0])

	print("#####",redfish_path,"   ",collection_path[0])
	if not os.path.isdir(redfish_path):
		target_folder = redfish_path.split("/")[-1]
		if "{" in target_folder and "}" in target_folder:
			print("GGGGG")
			cpu_data = get_cpu_all_info()
			cpu_number = get_cpu_number(cpu_data)
			print("CPU"+str(cpu_number))
			for index in range(1,cpu_number+1):
				create_folder(redfish_path.split("{")[0]+"CPU"+str(index))
		else:
			create_folder(redfish_path)

	data = create_index_json_content(redfish_data, collection_path[0], attr_properties, attr_navigation_properties)



	create_index_json(redfish_path, data)


