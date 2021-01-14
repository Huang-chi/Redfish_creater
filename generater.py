#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import os, sys
import urllib.request
import argparse
import subprocess

from setting import *
from xml.etree import ElementTree as ET

# Private library
sys.path.append(os.path.join(os.path.dirname(__file__),'lib'))

from create import *
from get import *

def analysis_xml(path):
	tree = ET.parse(path)
	root = tree.getroot()

	last_namespace = ""
	response = {}
	
	for child in root:
		if child.attrib:
			odata_type = ""
				
			for i in child:
				new_odata_type = i.attrib['Namespace']
				odata_type = new_odata_type+'.'+odata_type
			odata_type = odata_type[:-1]
			namespace = odata_type.split('.')[0]
			if len(child) == 1:
				if namespace in SPECIAL_RESOURCE:
					response[namespace] = child.attrib
					response[namespace]["@odata_type"] = "#"+odata_type
				else:
					response[last_namespace]['child'] = child.attrib
					response[last_namespace]['child']["@odata_type"] = "#"+odata_type+"."+odata_type
				
			else:
				response[namespace] = child.attrib
				response[namespace]["@odata_type"] = "#"+odata_type
	
			last_namespace = namespace
		
		else:
			pass
		
	return response

def install_resource(response, attr):
	if 'child' in response[attr].keys():
		uri = response[attr]['child']['Uri']
		print("Install uri: ", uri)
		filename = uri.split("/")[-1]
		urllib.request.urlretrieve(uri,"./resource/"+filename)
		
	uri = response[attr]['Uri']	
	print("Install uri: ", uri)
	filename = uri.split("/")[-1]
	urllib.request.urlretrieve(uri,"./resource/"+filename)

def setup_install_resource(responses):
	for attr in responses:
		install_resource(responses, attr)

def print_tree():
	subprocess.call(['tree','./redfish_data/'], shell = False)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-T', '--odata_type', type=str, nargs='+', help='Enter need resources or all')
	parser.add_argument('-D', '--dir', action = 'store_true' , help='create dir.')
	args = parser.parse_args()	
	odata_types = args.odata_type
	dir_path = args.dir
	
	if 'all' in odata_types:
		odata_types = ALL_COLLECTIONS
	print(odata_types)
	
	data = {}	
	collection_path = {}	
	
	if bool(dir_path):
		print("\n################################################################################")
		print("Create collection ... \n")
		collections = create_conllection(get_entry(JSON_PATH))
		#print(collections)
	
	print("\n################################################################################")
	print("Get resource uri ... \n")
	responses = analysis_xml(XML_PATH)
	#setup_install_resource(responses)
	
	print("\n################################################################################")
	print("Get data entity ... \n")
	entities = create_entity(CONFIG_PATH)	
	print(entities)

	print("\n################################################################################")
	print("Get property of resource ... \n")

	if bool(odata_types):
		for odata_type in odata_types:
			redfish_data_info = responses[odata_type]
			establish_level_number = 1
 
			
			if 'child' in redfish_data_info.keys():
				temp_odata_type = redfish_data_info['child']['@odata_type'][1:].split('.')[0]

				attr_properties, attr_navigation_properties, collection_path = get_all_property(os.path.join(RESOURCE_XML_PATH, temp_odata_type+"_v1.xml"), temp_odata_type)
				
				print(collection_path)

				data = create_content(redfish_data_info['child'], collection_path[temp_odata_type], attr_properties, attr_navigation_properties)
				redfish_path = data['@odata.id'].split('v1')[-1][1:]
				print(data['Members'])	
				

				dir_path = os.path.join(REDFISH_DATA,redfish_path)
				create_index(dir_path, data)
				
				
			attr_properties, attr_navigation_properties, collection_path = get_all_property(os.path.join(RESOURCE_XML_PATH, odata_type+"_v1.xml"), odata_type)

			if odata_type in entities.keys():
				collection_path[odata_type] = entities[odata_type]	
		
			data = create_content(redfish_data_info, collection_path[odata_type], attr_properties,attr_navigation_properties)
			redfish_path = data['@odata.id'].split('v1')[-1]
			
			create_index(redfish_path, data)
			
