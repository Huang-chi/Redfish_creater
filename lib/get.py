#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, json

from create import *
from setting import *
from xml.etree import ElementTree as ET

ENTITY_PROPERTY = ['ComplexType','EnumType']
def get_reference_path(attr_name, resource_name):
	path = os.path.join(RESOURCE_XML_PATH, resource_name+'_v1.xml')
	root = get_root(path)
	for child in root.iter():
		if 'String' in get_property(child):
			# Not sure the regular
			if attr_name == child.text.split('{')[1][:-1]:
				return child.text

def get_reference_property(data, child):
	target = ['NavigationProperty','Property']
	_type = get_property(child)
	print('### _type :', _type)
	temp = ""

	if _type in target:
		attr_name = child.attrib['Name']
		print("Attr_name: ", attr_name)
		if 'Edm' == child.attrib['Type'].split('.')[0]:
			print("1")
			temp = ""
		elif 'Collection' in child.attrib['Type'].split('('):
			print("2")
			reference = child.attrib['Type'].split('(')[-1][:-1]
			resource_name, resource_attr_name = reference.split('.')
			#temp[child.attrib['Name']] = list(get_reference_path(attr_name, resource_name))
			temp = list(get_inside_property(data, attr_name, resource_attr_name, resource_name))
		else:
			reference = child.attrib['Type'].split('.')
			resource_name, resource_attr_name = reference[0], reference[-1]
			print("3")
			print(attr_name, resource_name)
			temp = get_inside_property(data, attr_name, resource_attr_name, resource_name)
			print("/3")
	elif _type == 'ComplexType':
		pass
	
	
	return temp

def get_root(path):
	tree = ET.parse(path)
	root = tree.getroot()
	return root

def get_property(child):
	return child.tag.split('}')[-1]

def get_all_property(path, attr_name, collection_path):
	
	root = get_root(path)	
	attr_property = {}
	attr_navigation_property = {}
	temp_path = []

	begin = True
	count = 1
	for child in root.iter():
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
	collection_path[attr_name] = temp_path
	return attr_property, attr_navigation_property, collection_path	

def get_inside_property(data, attr_name, resource_name):
	path = os.path.join(RESOURCE_XML_PATH, resource_name+'_v1.xml')
	root = get_root(path)
	print("attr_name: ", attr_name)
	print("resource_name: ", resource_name)
	print("path: ", path)	
	begin_level_1 = False
	
	temp = {}
	
	if resource_name == attr_name:
		
		temp[attr_name] = get_reference_path(attr_name, resource_name)
		print(temp[attr_name])
		return temp
	 
	for child in root.iter():

		if 'ComplexType' in get_property(child) or 'EntityType' in get_property(child):
			if begin_level_1:
				break

			if 'BaseType' in child.attrib.keys():
				if attr_name == child.attrib['Name'] and resource_name != child.attrib['BaseType'].split('.')[0]:
					print("1 ##### child.attrib :", child.attrib)
					begin_level_1 = True
			elif resource_name == 'Resource':
				if attr_name == child.attrib['Name']:
					begin_level_1 = True
					print("2 ##### child.attrib :", child.attrib)
			else:
				temp[attr_name] = ""

		elif 'EnumType' in get_property(child):
			if attr_name == child.attrib['Name']:
				print("--------------")
				temp[attr_name] = ""
				break
			else:
				break

		if begin_level_1:
			print("Begin_level_1")
			temp[attr_name] = get_reference_property(data, child)
		
	
	print("\n##################")
	print("Temp: ", temp)
	print("##################\n")
	
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
