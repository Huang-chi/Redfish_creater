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

import redfish_node as Rf

#from redfish_create import create_redfish_data
from redfish_create import create_collection
from redfish_create import create_entity
from redfish_get import get_json_info
from nodelist import add_new_node
from nodelist import display_all_node
from CLI import CLI


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
					response[last_namespace]['parent'] = child.attrib
					response[last_namespace]['parent']["@odata_type"] = "#"+odata_type+"."+odata_type
				
			else:
				response[namespace] = child.attrib
				response[namespace]["@odata_type"] = "#"+odata_type
	
			last_namespace = namespace
		
		else:
			pass
		
	return response

def install_resource(response, attr):
	if 'child' in response[attr].keys():
		uri = response[attr]['parent']['Uri']
		print("Install uri: ", uri)
		filename = uri.split("/")[-1]
		urllib.request.urlretrieve(uri,"./resource/"+filename)
		
	uri = response[attr]['Uri']	
	print("Install uri: ", uri)
	filename = uri.split("/")[-1]
	urllib.request.urlretrieve(uri,"./resource/"+filename)

def setup_install_resource():
	uri_info = get_json_info(RESOURCE_URI_PATH)
	for attr in uri_info.values():
		install_resource(responses, attr)

def print_tree():
	subprocess.call(['tree','./redfish_data/'], shell = False)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-T', '--odata_type', type=str, nargs='+', help='Enter need resources or all.')
	parser.add_argument('-U', '--uri', type=str, help='Enter resource.')
	parser.add_argument('-D', '--dir', action = 'store_true' , help='create dir.')
	parser.add_argument('-R', '--resource', action = 'store_true', help="Install resource.")
	parser.add_argument('-C', '--CLI', action = 'store_true', help="Open CLI.")
	args = parser.parse_args()	

	domain = args.uri	
	install_resource_or_not = args.resource
	odata_types = args.odata_type
	dir_path = args.dir
	
	data = {}	
	collection_path = []
	root = None
	
	# Data form: 
	# _key: redfish_data
	# uri: ./redfish_data
	root = add_new_node(root, Rf.RedfishNode(REDFISH_DATA[2:], REDFISH_DIR, uri = REDFISH_DATA))
	
	if not bool(dir_path):
		print("\n################################################################################")
		print("Create collection ... \n")
		collections = create_collection(get_json_info(JSON_PATH))
		print(collections)
		for collection in collections:
			_key = collection.split("/")[-1]
			symbol = _key
			root = add_new_node(root, Rf.RedfishNode(_key, symbol, uri=collection))
			'''
			try:
				os.mkdir(collection)	
			except:
				pass
			'''
	print("\n################################################################################")
	
	print("Get resource uri ... \n")
	responses = analysis_xml(XML_PATH)
	if __debug__:
		print("### Responses: ", responses)
	
	if install_resource_or_not:
		setup_install_resource()

	print("\n################################################################################")
	print("Get data entity ... \n")
	entities = create_entity(CONFIG_PATH)
	
	if __debug__:
		print("### Entities: ", entities)
	
	for entity in entities.keys():
		_key = entities[entity].split("/")[-1]
		symbol = _key
		root = add_new_node(root, Rf.RedfishNode(_key, symbol, uri = entities[entity][1:]))

		try:
			os.mkdir(entities[entity])
		except:
			pass
	
	print("\n################################################################################")
	print("Get property of resource ... \n")
	
	symbols = [type_ for type_ in domain.split('/') if not (type_ in 'redfish' or type_ in 'v1')]

	print("Symbols: ", symbols)
	next_type = False	

	for index in range(len(symbols)):
		if next_type:
			next_type = False
		else:
			for _type in responses.keys():
				# Remove the last of the word (Remove 's') and find related type.
				match_resource_or_not = (_type.find(symbols[index][:-1]) != -1)
				
				if match_resource_or_not:
					print("#########################################\n")
					
					redfish_architecture = responses[_type]
					
					if 'parent' in redfish_architecture.keys():

						next_type = True
				
						parent_key = symbols[index]
						redfish_type= redfish_architecture['parent']['@odata_type'].split('.')[-1]
						parent_redfish_architecture = redfish_architecture['parent']
						print("_key: ",parent_key)	
						#create_redfish_data(parent_odata_type, parent_redfish_data, uri)
						temp = Rf.RedfishNode(parent_key, _type = redfish_type, _root=root)
						temp.create_redfish_data(parent_redfish_architecture)
						root = add_new_node(root, temp)
						#print("-------> ", temp._key)
						#print("-------> ", temp.data)
						#print("-------> ", temp.uri)
						
						index+=1

					_key = symbols[index]
					redfish_type = _type
					print("_key: ", _key)
					
					#create_redfish_data(_key, redfish_data, uri)
					temp_1 = Rf.RedfishNode(_key, _type = redfish_type, _root=root)
					temp_1.create_redfish_data(redfish_architecture)
					root = add_new_node(root, temp_1)
					#print("-------> ", temp_1._key)
					#print("-------> ", temp_1.data)
					#print("-------> ", temp_1.uri)

	print("\n################################################################################")
	print("OK")

	if args.CLI:
		CLI(root)
