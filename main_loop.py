import sys,os
import threading
import logging
import argparse

# Setting
from setting import *

# Private library
from redfishMockupServer import set_server
from redfishMockupServer import run_server
from CLI import CLI_setup
from CLI import CLI_main
from nodelist import add_new_node
import redfish_node as Rf
from init import create_collections
from init import get_resource_uri
from init import create_define_entity
#from init import create_

# Logging
logger = logging.getLogger(__name__)


def setup():

	logger.info("Redfish Mockup Server, version {}".format(TOOL_VERSION))

	parser = argparse.ArgumentParser(description='Serve a static Redfish mockup.')
	parser.add_argument('-H', '--host', '--Host', default=HOST,
                            help='hostname or IP address (default 127.0.0.1)')
	parser.add_argument('-p', '--port', '--Port', default=int(SERVER_PORT), type=int,
                            help='host port (default 8000)')
	parser.add_argument('-D', '--dir', '--Dir',
                            help='path to mockup dir (may be relative to CWD)')
	parser.add_argument('-X', '--headers', action='store_true',
                            help='load headers from headers.json files in mockup')
	parser.add_argument('-t', '--time', default=0,
                            help='delay in seconds added to responses (float or int)')
	parser.add_argument('-T', action='store_true',
                            help='delay response based on times in time.json files in mockup')
	parser.add_argument('-s', '--ssl', action='store_true',
                            help='place server in SSL (HTTPS) mode; requires a cert and key')
	parser.add_argument('--cert', help='the certificate for SSL')
	parser.add_argument('--key', help='the key for SSL')
	parser.add_argument('-S', '--short-form', '--shortForm', action='store_true', help='apply short form to mockup (omit filepath /redfish/v1)')
	parser.add_argument('-P', '--ssdp', action='store_true',
                            help='make mockup SSDP discoverable')
#	parser.add_argument('-U', '--uri', type=str, help='Enter the specified domain.')
	parser.add_argument('-R', '--resource', action = 'store_true', help="Install resource.")
	
	args = parser.parse_args()  
#	domain = args.uri   
	install_resource_gate = args.resource
	data = {}   
	collection_path = []
	root = None

	root = add_new_node(root, Rf.RedfishNode(REDFISH_DATA[2:], REDFISH_DIR, uri = REDFISH_DATA))

	root = create_collections(root)
	responses = get_resource_uri(install_resource_gate)
	root = create_define_entity(root)
	
	return root, responses, args

if __name__ =="__main__":
	
	root, responses, args = setup()
	myServer = set_server(args, root, responses)   # The dir must be exit
	server_thread = threading.Thread(target = run_server, args = (myServer,))
	server_thread.start()
	
	CLI_thread = threading.Thread(target = CLI_main, args = (root, responses,))
	#CLI_main(root, responses)
	CLI_thread.start()

	CLI_thread.join()
	server_thread.join()
