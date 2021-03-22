#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import os
import urllib.request
import argparse
import redfish_node as Rf

from setting import *
from xml.etree import ElementTree as ET
from redfish_create import get_collections
from redfish_create import create_entity
from redfish_get import get_json_info
from nodelist import add_new_node

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

def create_collections(root):	
	print("Create collection ... \n")
	collections = get_collections(get_json_info(JSON_PATH))
	for collection in collections:
		_key = collection.split("/")[-1]
		symbol = _key
		root = add_new_node(root, Rf.RedfishNode(_key, symbol, uri=collection))
	return root
	
def get_resource_uri(install_resource_gate):
	print("Get resource uri ... \n")
	responses = analysis_xml(XML_PATH)
	if __debug__:
		print("### Responses: ", responses)
	
	if install_resource_gate:
		setup_install_resource()
	return responses

def create_define_entity(root):
	print("Get define entity ... \n")
	entities = create_entity(CONFIG_PATH)
	
	if __debug__:
		print("### Entities: ", entities)
	
	for entity in entities.keys():
		_key = entities[entity].split("/")[-1]
		symbol = _key
		root = add_new_node(root, Rf.RedfishNode(_key, symbol, uri = entities[entity][1:]))
	
	return root

def create_data_entity(root, domain, responses):
	
	symbols = [type_ for type_ in domain.split('/') if not (type_ in 'redfish' or type_ in 'v1')]

	print("Symbols: ", symbols)
	next_type = False	
	uri = ""

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
					print("redfish_architecture: ", redfish_architecture)
					uri = os.path.join(uri, symbols[index])
					if 'parent' in redfish_architecture.keys():
						next_type = True
				
						parent_key = symbols[index]
						redfish_type= redfish_architecture['parent']['@odata_type'].split('.')[-1]
						parent_redfish_architecture = redfish_architecture['parent']

						temp = Rf.RedfishNode(parent_key, _type = redfish_type, _root=root, uri=domain)
						temp.create_redfish_data(parent_redfish_architecture)
						root = add_new_node(root, temp)
						if __debug__:
							print("-------> ", temp._key)
							print("-------> ", temp.data)
							print("-------> ", temp.uri)
						
						index+=1

						if index == len(symbols):
							break

						uri = os.path.join(uri, symbols[index])

					_key = symbols[index]
					redfish_type = _type
						
					temp_1 = Rf.RedfishNode(_key, _type = redfish_type, _root=root, uri=domain)
					temp_1.create_redfish_data(redfish_architecture)
					root = add_new_node(root, temp_1)
					if __debug__:
						print("-------> ", temp_1._key)
						print("-------> ", temp_1.data)
						print("-------> ", temp_1.uri)
	return root
