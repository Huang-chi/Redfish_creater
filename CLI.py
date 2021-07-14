#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, sys
import argparse
from setting import *

# Private package
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
import redfish_node as Rf
from nodelist import show_all_node
from nodelist import add_new_node
from init import create_collections
from init import get_resource_uri
from init import create_data_entity
from init import create_define_entity

def CLI_setup():
	
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

	root = create_collections(root)
	responses = get_resource_uri(install_resource_gate)
	#responses = get_resource_uri(False)
	root = create_define_entity(root)
	
	return root, responses

def CLI_main(root, responses):
	while True:
		domain = ""
		try:
			command_name = "# Redfish "
			value = input(command_name + " >> ")
			
			if value.lower() == "show all":
				show_all_node(root)
			elif value.lower() == "configure":
				uri = input(command_name +"/"+domain+ " (" + value + ") >> ")	
				root = create_data_entity(root, uri, responses)
						
			elif value.lower() == "show":
					uri = input(command_name +"/"+domain+ "  >> ")
					
					print("uri = ", uri)
					if uri == "":
						pass

					elif "index" in uri:
						symbol = uri.split("/")
						index = 0
						Max_index = len(symbol)
						cur_root = root
						last_root = root

						while index < Max_index and cur_root !=None:
							print("symbol = ", symbol[index])
							if "index" in symbol[index]:
								print("-----> ", cur_root.data)
							else:
								cur_root = last_root
				
							if symbol[index] == cur_root.key:
								last_root = cur_root.tail
							else:
								last_root = cur_root.right
							index += 1

			elif value.lower() == "head":
				if (root.head == None):
					print(root.key)
				else:
					print(root.key)
			else:
				pass
										
					
			if value == "\t":
				print("----")
			elif value.lower() == "q" or value.lower() == "exit":
				break
		except KeyboardInterrupt:
			print("\n------------------------------------------------------------------")
		

if __name__ == "__main__":
	root, responses = CLI_setup()
	CLI_main(root, responses)		
