#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, sys
import argparse
from setting import *

# Private package
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
import redfish_node as Rf
from nodelist import display_all_node
from nodelist import add_new_node
from init import get_collection
from init import get_resource_uri
from init import create_data_entity
from init import create_specified_data_entity

def setup():
	parser = argparse.ArgumentParser()
	parser.add_argument('-U', '--uri', type=str, help='Enter the specified domain.')
	parser.add_argument('-R', '--resource', action = 'store_true', help="Install resource.")
	args = parser.parse_args()  
	domain = args.uri   
	install_resource_gate = args.resource
	data = {}   
	collection_path = []
	root = None

	root = add_new_node(root, Rf.RedfishNode(REDFISH_DATA[2:], REDFISH_DIR, uri = REDFISH_DATA))

	root = get_collection(root)
	responses = get_resource_uri(install_resource_gate)
	root = create_data_entity(root)
	
	return root, responses

def CLI(root, responses):
	while True:
		domain = ""
		try:
			command_name = "# Redfish "
			value = input(command_name + " >> ")
			
			if value.lower() == "show all":
				display_all_node(root)
			elif value.lower() == "configure":
				uri = input(command_name +"/"+domain+ " (" + value + ") >> ")	
				root = create_specified_data_entity(root, uri, responses)
						
			elif value.lower() == "show":
					uri = input(command_name +"/"+domain+ "  >> ")

					if uri == "":
						pass

					elif "index" in uri:
						symbol = uri.split("/")
						index = 0
						Max_index = len(symbol)
						test_root = root
						last_root = root

						while index < Max_index and test_root !=None:
							if "index" in symbol[index]:
								print("-----> ", test_root.data)
							else:
								test_root = last_root
				
							if symbol[index] == test_root.key:
								last_root = test_root.tail
							else:
								last_root = test_root.right
							index += 1
							
					
			if value == "\t":
				print("----")
			elif value.lower() == "q" or value.lower() == "exit":
				break
		except KeyboardInterrupt:
			print("\n------------------------------------------------------------------")
		

if __name__ == "__main__":
	root, responses = setup()
	CLI(root, responses)		
