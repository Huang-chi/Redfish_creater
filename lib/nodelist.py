import sys
# sys.setrecursionlimit(2000)

def add_new_node(root, info):

	if root is None:
		return info
	# Update the data
	elif root.key == info.key and info.data != None:
		root.data = info.data
		return root
	else:
		if root.key in info.uri:
			
			cur = add_new_node(root.tail, info)
			root.tail = cur
			cur.head = root
		else:
			cur = add_new_node(root.right, info)
			root.right = cur
			cur.head = root
	return root

def search_node(root, path, index=0, gate=False):
	# path = /key1/key2/key6
	test_path = []

	if root is None and index < len(path):
		gate = True
		cur, gate = search_node(root, path, index+1, gate)
		test_path.append(path[index])
		test_path = test_path + cur
		return test_path, gate

	# solution 1: The case is complete path.
	elif root is None and index == len(path):
		return [None], gate
	
	# solution 2: The case is incomplete path.
	if "{" in path[index] and "}" in path[index]:
		cur, gate = search_node(root.tail, path, index+1, gate)
		test_path.append(root.key)
		test_path = test_path + cur
		return test_path, gate

	if path[index] == root.key:
		cur, gate = search_node(root.tail, path, index+1, gate)
		test_path.append(root.key)
		test_path = test_path + cur
	else:
		cur, gate = search_node(root.right, path, index, gate)
		test_path = test_path + cur

	return test_path, gate

def show_all_node(root):

	print("\n")
	print("### Key: ", root.key)
	print("### Data: ",root.data)
	print("### current: ", root)
	print("### right: ",root.right)
	print("### tail: ",root.tail)
	print("### head: ",root.head)
	
	print("----------------------------")
	
	if not (root.tail is None):
		show_all_node(root.tail)
	if not (root.right is None):
		show_all_node(root.right)
	
	return ""

##########################
# key1
#  |
# key2 - key3 - key4
#  |             |
# key5 - key6   key7
##########################

if __name__ == "__main__":
	root = None

	info1 = Rf.RedfishNode("key1", data = "data1", uri= "/key1")
	info2 = Rf.RedfishNode("key2", data = "data2", uri= "/key1/key2")
	info3 = Rf.RedfishNode("key3", data = "data3", uri= "/key1/key3")
	info4 = Rf.RedfishNode("key4", data = "data4", uri= "/key1/key4")
	info5 = Rf.RedfishNode("key5", data = "data5", uri= "/key1/key2/key5")
	info6 = Rf.RedfishNode("key6", data = "data6", uri= "/key1/key2/key6")
	info7 = Rf.RedfishNode("key7", data = "data7", uri= "/key1/key4/key7")
	info22 = Rf.RedfishNode("key2", data = "datadd", uri= "/key1/key2")

	root = add_new_node(root, info1)
	root = add_new_node(root, info2)
	root = add_new_node(root, info3)
	root = add_new_node(root, info4)
	root = add_new_node(root, info5)
	root = add_new_node(root, info6)
	root = add_new_node(root, info7)
	root = add_new_node(root, info22)
	
	#display_all_node(root)
	test_path = info6.uri[1:].split("/")
	str_path = "key1/key2/{key}"
	test_path = str_path.split("/")
	print(search_node(root, test_path))

