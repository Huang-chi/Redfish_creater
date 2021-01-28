#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, json
import sys
from collections import OrderedDict

from setting import *
from xml.etree import ElementTree as ET

from create_file_or_folder import *

ENTITY_PROPERTY = ['ComplexType','EnumType']

def get_json_data(path):
	if os.path.isfile(path):
		jsonData = ""
		with open(path, 'r', newline = '') as f:
			jsonData = json.load(f, object_pairs_hook = OrderedDict)
			f.close()
		return jsonData
	else:
		return None

def get_entry(path):
	with open(path, "r") as f:
		return json.load(f)

def get_odata_id(path):
	if __debug__:
		print("\n##########",__file__," ",str(sys._getframe().f_lineno),"###########")
		print("### Path: ",path)
	tags = path.split('/')
	str_path = REDFISH_DATA
	odata_id = "/"
	for index in range(len(tags)):
		if __debug__:
			print("### tag",tags[index],"  ",str_path)

		if '{' in tags[index][:1] and '}' in tags[index][-1:]:
			try:
				list_dir = os.listdir(str_path)

				for dirname in list_dir:
					if dirname != INFO_FILENAME:
						tags[index] = dirname
					else:
						pass
			except:
				print("No find the path.")
	
		if tags[index] != 'redfish' and tags[index] != 'v1':
			str_path = os.path.join(str_path, tags[index])
		odata_id = os.path.join(odata_id, tags[index])
	
	if __debug__:
		print("### odata_id: ",odata_id)
		print("### Str_path", str_path)			
		print("#######################################")
	
	return str_path, odata_id

def get_root(path):
	tree = ET.parse(path)
	root = tree.getroot()
	return root

def get_property(child):
	return child.tag.split('}')[-1]

def get_reference_resource_and_attr_name(_property, attr_name):
	
	if 'Collection(' in _property[attr_name]:
		_type = _property[attr_name].split('(')[-1][:-1]
	else:
		_type = _property[attr_name]

	return _type.split('.')[0], _type.split('.')[-1]

def get_reference_path(attr_name, resource_name):
	
	path = os.path.join(RESOURCE_XML_PATH, resource_name+'_v1.xml')
	root = get_root(path)
	for child in root.iter():
		if 'String' in get_property(child):
			# Not sure the regular
			return child.text

def get_reference_property(child):
	temp = {}
	attr_name = ""

	attr_name = child.attrib['Name']

	if 'Oem' == attr_name:
		temp = ""
	elif 'Edm' == child.attrib['Type'].split('.')[0]:
		temp = ""
	elif 'Collection' in child.attrib['Type'].split('('):
		resource_name, resource_attr_name = get_reference_resource_and_attr_name(child.attrib, 'Type')
		dict_add_list = []
		dict_add_list.append(get_entity_property(attr_name, resource_attr_name, resource_name))
		temp = dict_add_list
	else:
		reference = child.attrib['Type'].split('.')
		resource_name, resource_attr_name = reference[0], reference[-1]
		temp = get_entity_property(attr_name, resource_attr_name, resource_name)
	
	return  attr_name, temp

# There is one question:
# - Use the "count"
'''
- count = 2 is a start point 
- count = 3 is special case
'''

def get_all_property(path, attr_name):
	
	root = get_root(path)	
	attr_property = {}
	attr_navigation_property = {}
	temp_path = []

	begin = True
	count = 1
	
	for child in root.iter():
		# 
		if 'String' in child.tag:
			temp_path.append(child.text)
		if 'Name' in child.attrib.keys():
			if count == 1: 
				count = count +1
			elif count == 2 or count == 3:
				if 'BaseType' in child.attrib.keys():
					if attr_name == child.attrib['Name']:
						begin = True
						count = count +1
					else:
						begin = False
				else:	
					if begin:
						property_name = get_property(child)
						if property_name == 'Property':
							attr_property[child.attrib['Name']] = child.attrib['Type']
						elif property_name == 'NavigationProperty':
							attr_navigation_property[child.attrib['Name']] = child.attrib['Type']
			else: break
	return attr_property, attr_navigation_property, temp_path	

def get_entity_property(attr_name, resource_attr_name, resource_name):
	
	path = os.path.join(RESOURCE_XML_PATH, resource_name+'_v1.xml')
	if __debug__:	
		print("\n######### Info ",__file__, sys._getframe().f_lineno,"############")
		print("attr_name: ", attr_name)
		print("resource_attr_name: ", resource_attr_name)
		print("resource_name: ", resource_name)
		print("path: ", path)
		print("#######################################\n")
		
	root = get_root(path)
	
	begin_level_1 = False
	temp = {}	
	
	if resource_name == resource_attr_name:
		
		temp['@odata.id'] = get_reference_path(resource_attr_name, resource_name)
		if temp['@odata.id'] == None:
			return 
		else:
			str_path, temp['@odata.id'] = get_odata_id(temp['@odata.id'])
			create_folder(str_path)	
		
	else: 
		for child in root.iter():
			if 'ComplexType' in get_property(child) or 'EntityType' in get_property(child):
				if begin_level_1:
					break
				
				if resource_attr_name == child.attrib['Name']:
					if 'BaseType' in child.attrib.keys():
						if resource_name != child.attrib['BaseType'].split('.')[0]:
							begin_level_1 = True
					elif resource_name == 'Resource':
						begin_level_1 = True
					else:
						pass					

			elif 'EnumType' in get_property(child):
				if resource_attr_name == child.attrib['Name']:
					return ""
				else:
					pass

			if begin_level_1:
				_type = get_property(child)
				if _type in REFERENCE_PROPERTY_TARGET:
					temp_key, temp_value = get_reference_property(child)
					temp[temp_key] = temp_value
		
	return temp

if __name__ == "__main__":
	attr_property, attr_navigation_property = get_all_property(os.path.join(RESOURCE_XML_PATH,"Resource_v1.xml"),"Status")
'''
	get_info(attr_property)
	print("-----------------------------------------------------------")
	get_all_property(os.path.join(RESOURCE_XML_PATH,"Manager_v1.xml"),'Manager')

'''	
