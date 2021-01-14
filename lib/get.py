#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, json

from create import *
from setting import *
from xml.etree import ElementTree as ET

ENTITY_PROPERTY = ['ComplexType','EnumType']
def get_root(path):
	tree = ET.parse(path)
	root = tree.getroot()
	return root

def get_property(child):
	return child.tag.split('}')[-1]

def get_reference_resource_and_attr_name(_property, attr_name):
	if 'Collection' in _property[attr_name]:
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
	print("Attr_name: ", attr_name)

	print()

	if 'Oem' == attr_name:
		temp = ""
	elif 'Edm' == child.attrib['Type'].split('.')[0]:
		print("3")
		temp = ""
	elif 'Collection' in child.attrib['Type'].split('('):
		print("1")
		resource_name, resource_attr_name = get_reference_resource_and_attr_name(child.attrib, 'Type')

		#resource_name, resource_attr_name = reference.split('.')
		temp = list(get_entity_property(attr_name, resource_attr_name, resource_name))
	else:
		print("2")
		reference = child.attrib['Type'].split('.')
		resource_name, resource_attr_name = reference[0], reference[-1]
		temp = get_entity_property(attr_name, resource_attr_name, resource_name)
		print("### temp 54: ",temp)
	return  attr_name, temp


def get_all_property(path, attr_name):
	
	root = get_root(path)	
	attr_property = {}
	attr_navigation_property = {}
	temp_path = {}

	begin = True
	count = 1
	for child in root.iter():
		if 'String' in child.tag:
			temp_path[attr_name] = child.text
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
	root = get_root(path)
	
	print("\n######### Info ",__file__, "############")
	print("attr_name: ", attr_name)
	print("resource_attr_name: ", resource_attr_name)
	print("resource_name: ", resource_name)
	print("path: ", path)
	print("#######################################\n")	
	
	begin_level_1 = False
	temp = {}	
	
	if resource_name == resource_attr_name:
		
		temp['@odata.id'] = get_reference_path(resource_attr_name, resource_name)
		return temp
	
	else: 
		temp[attr_name] = {}
		for child in root.iter():
			if 'ComplexType' in get_property(child) or 'EntityType' in get_property(child):
				if begin_level_1:
					break

				if 'BaseType' in child.attrib.keys():
					if attr_name == child.attrib['Name'] and resource_name != child.attrib['BaseType'].split('.')[0]:
						begin_level_1 = True
				elif resource_name == 'Resource':
					if attr_name == child.attrib['Name']:
						begin_level_1 = True
				else:
					temp[attr_name] = ""

			elif 'EnumType' in get_property(child):
				if resource_attr_name == child.attrib['Name']:
					temp = ""
					break
				else:
					pass

			if begin_level_1:
				_type = get_property(child)
				if _type in REFERENCE_PROPERTY_TARGET:
					print("### _type: ",_type)
					temp_key, temp_value = get_reference_property(child)
					temp[attr_name][temp_key] = temp_value
		
	'''	
	print("\n##################")
	print("Temp: ", temp)
	print("##################\n")
	'''	
	return temp


def get_outside_property(path, attr_name):
	
	root = get_root(path)	
	attr_complex_property = []

	block = False
	for child in root.iter():
		_type = get_property(child)
		if _type == "ComplexType":
			if child.attrib['Name'] == attr_name:
				block = True
		else:
			if block:
				_type = get_property(child)
				if _type == "Property":
					attr_complex_property.append( child.attrib)
				elif _type not in ENTITY_PROPERTY:
					pass
				else :
					block = False

	return attr_complex_property

def get_info(attr_property):
	print("")
	print(attr_property)

	data = {}
	

if __name__ == "__main__":
	attr_property, attr_navigation_property = get_all_property(os.path.join(RESOURCE_XML_PATH,"Resource_v1.xml"),"Status")
'''
	get_info(attr_property)
	print("-----------------------------------------------------------")
	get_all_property(os.path.join(RESOURCE_XML_PATH,"Manager_v1.xml"),'Manager')

'''	
