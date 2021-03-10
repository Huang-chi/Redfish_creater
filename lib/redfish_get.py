#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, json
import sys
from collections import OrderedDict

from setting import *
from xml.etree import ElementTree as ET

from create_file_or_folder import *

ENTITY_PROPERTY = ['ComplexType','EnumType']

def get_json_info(path):
	if os.path.isfile(path):
		jsonData = ""
		with open(path, 'r', newline = '') as f:
			jsonData = json.load(f, object_pairs_hook = OrderedDict)
			f.close()
		return jsonData
	else:
		return None

def get_root(attr_name):
	path = os.path.join(RESOURCE_XML_PATH, attr_name + REDFISH_VERSION + ".xml")
	tree = ET.parse(path)
	root = tree.getroot()
	return root

def get_property(child):
	return child.tag.split('}')[-1]

def get_reference_path(resource_name):
	
	root = get_root(resource_name)
	for child in root.iter():
		# Fetch first path
		if 'String' in get_property(child):
			# print("### String", child.text)
			# Not sure the regular
			return child.text
	return ""

if __name__ == "__main__":
	attr_property, attr_navigation_property = get_all_property(os.path.join(RESOURCE_XML_PATH,"Resource_v1.xml"),"Status")
'''
	get_info(attr_property)
	print("-----------------------------------------------------------")
	get_all_property(os.path.join(RESOURCE_XML_PATH,"Manager_v1.xml"),'Manager')

'''	
