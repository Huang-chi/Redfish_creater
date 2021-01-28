import sys, os
import json
import time

from setting import*

from generater import analysis_xml

# private package
sys.path.append(os.path.join(os.path.dirname(__file__),'lib'))
from redfish_create import *
from redfish_get import *
from redfish_copy import copy_file
from redfish_delete import *

def create_role():
	try:
		pass
	except Exception as e:
		print(e)
		return False
	return True

def add_role(redfish_info, attr, value):
	#odata_id = ""
	model = redfish_info['@odata.id']
	
	new_data = {}
	new_data['@odata.id'] = os.path.join(model, value)
	
	# The odata_id and new_data['@odata.id'] are same
	new_str_path, new_odata_id = get_odata_id(new_data['@odata.id'])
	
	if __debug__:
		print("new_str_path: ", new_str_path)
		print("new_odata_id: ", new_odata_id)

	create_folder(new_str_path)
	time.sleep(0.1)	
	str_path, odata_id = get_odata_id(redfish_info[attr][0]['@odata.id'])
	copy_file(os.path.join(str_path, INFO_FILENAME), new_str_path)

	redfish_info[attr].append({"@odata.id":new_odata_id})


	if '{' in redfish_info[attr][0]['@odata.id'] and '}' in redfish_info[attr][0]['@odata.id']:
		redfish_info[attr].pop(0)
		delete_folder(str_path)
	
	return redfish_info


if __name__ =="__main__":
		
	redfish_data = analysis_xml(XML_PATH)[sys.argv[1]]
	
	'''
	# CLI
	while True:
		try:
			value = input("# Redfsih >> ")
			if value == "\t":
				print("111")
			elif value == "q" or value == "exit":
				break
		except KeyboardInterrupt:
			print("\n--------------------------------------------------------")
			pass
	'''

	queue_temp = []

	if 'child' in redfish_data.keys():
		queue_temp.append(redfish_data['child']['@odata_type'].split('.')[-1])
	queue_temp.append(redfish_data['@odata_type'].split('.')[-1])


	for odata_type in queue_temp:
		# _attr_properties, _attr_navigation_properties is unused
		_attr_properties, _attr_navigation_properties , collection_path = get_all_property(os.path.join(RESOURCE_XML_PATH, odata_type+"_v1.xml"), odata_type)
		
		redfish_data_path, collection_path[0] = get_odata_id(collection_path[0])
	
		redfish_info = get_json_data(os.path.join(redfish_data_path, INFO_FILENAME))

		for attr in redfish_info:
			if attr  == "Members":
				number = int(input("How many do you create: "))
				count = 0
				while count < number:
					member_value = input("Add "+attr+": ")
					if (create_role()):
						redfish_info = add_role(redfish_info, attr, member_value)
					count +=1
					redfish_info["Members@odata.count"] = len(redfish_info["Members"]) 
					create_index_json(redfish_data_path, redfish_info)
			
