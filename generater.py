#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import os, sys
import urllib.request
import argparse
import subprocess

from setting import *
from xml.etree import ElementTree as ET

# Private package
sys.path.append(os.path.join(os.path.dirname(__file__),'lib'))

from redfish_create import *
from redfish_get import *
from create_file_or_folder import *

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
	parser.add_argument('-U', '--uri', type=str, help="Enter request uri .")
	args = parser.parse_args()	
	
	uri = args.uri
	odata_types = args.odata_type
	dir_path = args.dir
	'''	
	if 'all' in odata_types:
		odata_types = ALL_COLLECTIONS
	print(odata_types)
	'''
	data = {}	
	collection_path = []	
		
	if not bool(dir_path):
		print("\n################################################################################")
		print("Create collection ... \n")
		collections = create_collection(get_entry(JSON_PATH))
	
	print("\n################################################################################")
		
	print("Get resource uri ... \n")
	responses = analysis_xml(XML_PATH)
	if __debug__:
		print("### Responses: ", responses)
	#setup_install_resource(responses)
	
	print("\n################################################################################")
	print("Get data entity ... \n")
	entities = create_entity(CONFIG_PATH)	
	if __debug__:
		print("### Entities: ", entities)

	print("\n################################################################################")
	print("Get property of resource ... \n")
	
	uris = [type_ for type_ in uri.split('/') if not (type_ in 'redfish' or type_ in 'v1')]

	next_type = False	
	
	for uri in uris:
		print("--------------------\n\n")
		print(uri)
		
		if next_type:
			next_type = False
		else:
			for _key in responses.keys():
				
				# Remove the last of the word. (Remove 's')
				odata_type = _key.find(uri[:-1])
				if not odata_type == -1:
					print(_key)
					next_type = True
					redfish_data = responses[_key]
					if 'child' in redfish_data.keys():
						child_odata_type = redfish_data['child']['@odata_type'].split('.')[-1]
						child_redfish_data = redfish_data['child']
						create_redfish_data(child_odata_type, child_redfish_data)
					create_redfish_data(_key, redfish_data)

	'''
	if bool(odata_types):
		for odata_type in odata_types:
			redfish_data = responses[odata_type]
			if __debug__:
				print("### Redfish data: ",redfish_data)			
		
			if 'child' in redfish_data.keys():
				child_odata_type = redfish_data['child']['@odata_type'][1:].split('.')[0]
				child_redfish_data = redfish_data['child']
				create_redfish_data(child_odata_type, child_redfish_data)
			
			create_redfish_data(odata_type, redfish_data)
	
	'''		
	print("\n################################################################################")
	print("OK")	
