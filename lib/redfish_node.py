import os, sys, json

import collections

from create_file_or_folder import search_device_info
from redfish_get import get_root
from redfish_get import get_reference_path
from nodelist import search_node

sys.path.append(os.path.join(os.path.dirname(__file__), "./.."))
from setting import *

class RedfishNode:
	def __init__(self, _key, _root=None, _type=None, data=None, uri=None):
		self.key = _key
		self.data = data
		self.uri = uri
		self.type = _type
		self.head = None
		self.right = None
		self.tail = None
		self.root = _root
	
	def get_property(self, child):
		return child.tag.split("}")[-1]
	
	# start point
	def create_redfish_data(self, architecture):
		
		properties, navigation_properties, path_array = self.assign_property(self.type)

		temp_uri, odata_id_path = self.get_data_path_and_redfish_path(path_array[0])
		self.data = self.create_index_json_content(architecture, odata_id_path, properties, navigation_properties)
		self.uri = temp_uri

	def create_index_json_content(self, data, odata_id, properties, navigation_properties):
		# create an object with ordering
		info = collections.OrderedDict()

		info["@odata.type"] = data['@odata_type']
		info["Name"] = ""
		
		# There is question about the content of attribute for "Memeber"(2/8)
		if 'Members' not in navigation_properties and 'Members' not in properties:	
			info ["Id"] = odata_id.split('/')[-1]
		else:
			info["Members@odata.count"] = 0
		
		info["Description"] = ""
		info = self.create_property(info, properties)
		info = self.create_navigation_property(info, navigation_properties)
		
		if 'Members' in navigation_properties or 'Members' in properties:
			info["Members@odata.count"] = len(info["Members"])
		info["@odata.id"] = odata_id
		info[COPYRIGHT] = COPYRIGHT_CONTENT
		
		return info

	def assign_property(self, attr_name):

		root = get_root(attr_name)
	
		# Declare varible and initial
		property_dict = {}
		navigation_property_dict = {}
		odata_id_path_arr = []

		# Represent as the start signal
		gate = False
		count = 1

		for child in root.iter():
			# Get referenced path
			if 'String' in child.tag:
				odata_id_path_arr.append(child.text)
			# Get the body of schema
			if 'Name' in child.attrib.keys():
				# For collection, not need to ignore first line
				if child.attrib['Name'].find("Collection") != -1:
					count += 1
				# Ignore first line, because the line is title
				if count == 1:
					count += 1
				# Start point
				elif count == 2 or count == 3:
					if 'BaseType' in child.attrib.keys():
						# Determine the starting point
						if attr_name == child.attrib['Name']:
							gate = True
							count += 1
						else:
							gate = False
					else:
						# start that info determines
						if gate:
							# Distinguish property and navigation property
							property_name = self.get_property(child)
							if property_name == "Property":
								property_dict[child.attrib["Name"]] = child.attrib["Type"]
							elif property_name == "NavigationProperty":
								navigation_property_dict[child.attrib["Name"]] = child.attrib["Type"]
							else:
								pass
						else:
							pass
				else:
					break
		return property_dict, navigation_property_dict, odata_id_path_arr

	def get_data_path_and_redfish_path(self, path, Member_is_not=False):		
		tags = path[1:].split("/")
		#print("Path: ", path)
	
		# Initial root folder for data path
		data_path = REDFISH_DATA
		redfish_path = "/redfish/v1/"
		
		if not ("{" in path and "}" in path):
			data_path = os.path.join(data_path, path.split("/v1/")[-1])
			return data_path, path	
		else:
			test_path, gate = search_node(self.root.tail,tags[2:])
			target_path = self.uri.split("/")

			gate = False
			members = []
			for path, target in zip(test_path[:-1], target_path[3:]):
				if path == target:
					gate = True
				elif "{" in path and "}" in path and gate:
					members = search_device_info(path)
					if Member_is_not:
						arr_members = []
						for member in members:
							arr_members.append(os.path.join(redfish_path,member))
						data_path = os.path.join(data_path, target)
						return data_path, arr_members

					else:
						if target in members:
							path = target
						else:
							print("# Error: the link is not exist.")
				else: pass

				data_path = os.path.join(data_path, path)
				redfish_path = os.path.join(redfish_path, path)
			if __debug__:
				print("         ", target_path[3:])
				print("         ", redfish_path)
			
			return data_path, redfish_path

	# Create the attribute that exists in other resource
	def create_reference_property(self, info, attr_name, resource_attr_name, resource_name, properties):

		#11
		entity_property = self.get_entity_property(attr_name, resource_attr_name, resource_name)
		if not entity_property:
			if "Collection" in properties[attr_name]:
				info[attr_name] = []
			else:
				info[attr_name] = entity_property
		else:			
			if "Collection" in properties[attr_name]:
				_list = []
				for entity in entity_property.values():
					temp = {}
					temp["@odata.id"] = entity
					_list.append(temp)
				info[attr_name] = _list
			else:
				info[attr_name] = entity_property

		return info
	
	def create_property(self, info, properties):
		for attr_name in properties:
			resource_name, resource_attr_name = self.get_reference_resource_and_attr(properties, attr_name)
	
			# In the future, write info into info in here
			# Entity 
			if resource_name == "Edm":
				info[attr_name] = ""
			# Reference
			else:
				info = self.create_reference_property(info, attr_name, resource_attr_name, resource_name, properties)
	
		return info

	def create_navigation_property(self, info, properties):
		for attr_name in properties:
			resource_name, resource_attr_name = self.get_reference_resource_and_attr(properties, attr_name)
			info = self.create_reference_property(info, attr_name, resource_attr_name, resource_name, properties)
	
		return info
					
	def get_reference_resource_and_attr(self, properties, attr_name):
		
		# Remove "(" and ")"
		if "Collection(" in properties[attr_name]:
			res = properties[attr_name].split("Collection")[-1][1:-1].split(".")		
			resource, attr_name = res[0],res[-1]
		else:
			_type = properties[attr_name].split(".")	
			resource, attr_name = _type[0], _type[-1]
			
		return resource, attr_name

	def get_entity_property(self, attr_name, resource_attr_name, resource_name):
		root = get_root(resource_name)
		
		gate = False
		temp = {}
	
		# Get the reference uri
		if resource_name == resource_attr_name:
			reference_path = get_reference_path(resource_name)
			#print("-----------> ",reference_path)
			if reference_path == "":
				return ""
			else:
				redfish_path, temp["@odata.id"] = self.get_data_path_and_redfish_path(reference_path, Member_is_not = True)
				if __debug__:
					print("\n######## Redfish Path: ", redfish_path)
					print("######## temp['@odata.id']: ", temp['@odata.id'],"\n")
		
		else:
			for child in root.iter():
				if "ComplexType" in self.get_property(child) or "EntityType" in self.get_property(child):
					if gate:
						break
					
					# Search the start point
					if resource_attr_name == child.attrib["Name"]:
						if "BaseType" in child.attrib.keys():
							if resource_name != child.attrib["BaseType"].split(".")[0]:
								gate = True
						elif resource_name == "Resource":
							gate = True
						elif len(child.attrib.keys()) == 1:
							gate = True
						else:
							pass
				elif "EnumType" in self.get_property(child):
					# EnumType is represented that the attribute includes some sub-attribute
					# In future, the part has to verify the attribute
					if resource_attr_name == child.attrib["Name"]:
						return ""
					else:
						pass

				if gate:
					_type = self.get_property(child)
					# REFERENCE_PROPERTY_TARGET = ['NavigationProperty','Property']
					if _type in REFERENCE_PROPERTY_TARGET:
						temp_key, temp_value = self.get_reference_property(child)
						temp[temp_key] = temp_value
		return temp

	def get_reference_property(self, child):
		temp_info = {}
		attr_name = child.attrib["Name"]
		
		#print("### child.attrib: ", child.attrib)
		
		if "Oem" == attr_name:
			temp = ""
		elif "Edm" == child.attrib["Type"].split(".")[0]:
			temp = ""
		elif "Collection" in child.attrib["Type"]:
			resource_name, resource_attr_name = self.get_reference_resource_and_attr(child.attrib, "Type")
			temp_list = []
			temp = self.get_entity_property(attr_name, resource_attr_name, resource_name)
			if temp:
				temp_list.append(temp)
			temp_info = temp_list
		else:
			reference = child.attrib["Type"].split(".")
			resource_name, resource_attr_name = reference[0], reference[-1]
			temp_info = self.get_entity_property(attr_name, resource_attr_name, resource_name)

		return attr_name, temp_info

if __name__ == "__main__":
	pass
