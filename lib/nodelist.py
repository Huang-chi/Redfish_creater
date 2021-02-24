import sys
import redfish_node as Rf
# sys.setrecursionlimit(2000)

def add_new_node(root, info, direction=None, keyword=None):

	if root is None:
		return info
	else:
		if root._key in info.uri:
			print("1")
			cur = add_new_node(root.tail, info, direction)
			root.tail = cur
		else:
			print("2")
			cur = add_new_node(root.right, info, direction)
			root.right = cur
		'''
		elif "right" == direction:
			cur = add_new_node(root.right, info, direction)
			root.right = cur
		elif "tail" ==direction:
			cur = add_new_node(root.tail, info, direction)
			root.tail = cur
		else:
			print("Error: ..............")
			return ""
		'''
	return root


def display_all_node(root):
	print(root._key)
	print("### current: ", root)
	print("### right: ",root.right)
	print("### tail: ",root.tail)
	print("----------------------------")
	
	if not (root.tail is None):
		display_all_node(root.tail)
	if not (root.right is None):
		display_all_node(root.right)
	
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

	info1 = Rf.RedfishNode("key1","data1","/key1")
	info2 = Rf.RedfishNode("key2","data2","/key1/key2")
	info3 = Rf.RedfishNode("key3","data3","/key1/key3")
	info4 = Rf.RedfishNode("key4","data4","/key1/key4")
	info5 = Rf.RedfishNode("key5","data5","/key1/key2/key5")
	info6 = Rf.RedfishNode("key6","data6","/key1/key2/key6")
	info7 = Rf.RedfishNode("key7","data7","/key1/key4/key7")

	root = add_new_node(root, info1)
	print("\n--------------------------------")
	root = add_new_node(root, info2, "tail")
	print("\n--------------------------------")
	root = add_new_node(root, info3, "right")
	print("\n--------------------------------")
	root = add_new_node(root, info4, "tail")
	print("\n--------------------------------")
	root = add_new_node(root, info5, "right")
	print("\n--------------------------------")
	root = add_new_node(root, info6, "tail")
	print("\n--------------------------------")
	root = add_new_node(root, info7, "right")
	print("\n--------------------------------\n\n\n")
	
	display_all_node(root)

