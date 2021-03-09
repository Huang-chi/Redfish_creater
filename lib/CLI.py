#!/usr/bin/python
# -*- coding: UTF-8 -*-
from nodelist import display_all_node

def CLI(root):
	while True:
		domain = ""
		try:
			command_name = "# Redfish "
			value = input(command_name + " >> ")
			
			if value.lower() == "show":
				display_all_node(root)
			elif value.lower() == "configure":

				while True:
					uri = input(command_name +"/"+domain+ " (" + value + ") >> ")

					if uri == "":
						pass

					elif "index" in uri:
						symbol = uri.split("/")
						index = 0
						Max_index = len(symbol)
						test_root = root
						last_root = root
						print(Max_index)

						while index < Max_index:
							if "index" in symbol[index]:
								print("-----> ", test_root.data)
							else:
								test_root = last_root
				
							if symbol[index] == test_root.key:
								last_root = test_root.tail
							else:
								last_root = test_root.right
							index += 1
					
							if value.lower() == "q" or value.lower() == "exit":
								break
					else:

						domain = uri
					if uri.lower() == "q" or uri.lower() == "exit":
						break

			if value == "\t":
				print("----")
			elif value.lower() == "q" or value.lower() == "exit":
				break
		except KeyboardInterrupt:
			print("\n------------------------------------------------------------------")
		

if __name__ == "__main__":
	CLI()		
