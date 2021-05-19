# Product library
import re, sys, os
import argparse
import threading

import ssl
import logging
from http.server import HTTPServer

# Setting
from setting import *

from CLI import CLI_setup

# Private library
sys.path.append(os.path.join(os.path.dirname(__file__),'lib/opensource'))
from redfish_verify import verify_mockdir_is_exist
from RfMockupModule import RfMockupServer
from rfSsdpServer import RfSSDPServer
from redfish_path import clean_path

# Logging
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

# ssl (For target future needs to implement the secret function)
context = ssl.create_default_context()

def init():
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

        return parser.parse_args()

def set_server(args, root, response):

        hostname = args.host
        port = args.port
        mockDirPath = args.dir
        headers = args.headers
        responseTime = args.time
        timefromJson = args.T
        sslMode = args.ssl
        sslCert = args.cert
        sslKey = args.key
        shortForm = args.short_form
        ssdpStart = args.ssdp

        # check if mockup path was specified.  If not, use the built-in mockup
        if mockDirPath is None:
            print("Add the default path.")
            #mockDirPath = 'public-rackmount1'
            shortForm = True

        logger.info('Hostname: {}'.format(hostname))
        logger.info('Port: {}'.format(port))
        logger.info("Mockup directory path specified: {}".format(mockDirPath))
        logger.info("Response time: {} seconds".format(responseTime))

        # create the full path to the top directory holding the Mockup
        mockDir = os.path.realpath(mockDirPath)  # creates real full path including path for CWD to the -D<mockDir> dir path
        logger.info("Serving Mockup in absolute path: {}".format(mockDir))

        logger.info("ShortForm: {}".format(shortForm))
        verify_mockdir_is_exist(logger, mockDir, shortForm)

        myServer = HTTPServer((hostname, port), RfMockupServer)
        
        if sslMode:
            logger.info("Using SSL with certfile: {}".format(sslCert))
            myServer.socket = ssl.wrap_socket(myServer.socket, certfile=sslCert, keyfile=sslKey, server_side=True)

        # save the test flag, and real path to the mockup dir for the handler to use

        myServer.mockDir = mockDir
        # myServer.testEtagFlag = testEtagFlag
        myServer.headers = headers
        myServer.timefromJson = timefromJson
        myServer.shortForm = shortForm
        myServer.root = root
        myServer.response = response

        try:
            myServer.responseTime = float(responseTime)
        except ValueError as e:
            logger.info("Enter an integer or float value")
            sys.exit(2)

        mySSDP = None
        
        if ssdpStart:
            from gevent import monkey
            monkey.patch_all()  
            # construct path "mockdir/path/to/resource/<filename>"
            path, filename, jsonData = '/redfish/v1', 'index.json', None
            apath = myServer.mockDir
            rpath = clean_path(path, myServer.shortForm)
            fpath = os.path.join(apath, rpath, filename) if filename not in ['', None] else os.path.join(apath, rpath)

				
            #sys.path.append(os.path.join(os.path.dirname(__file__),'lib'))
            from redfish_get import get_json_info
            
            jsonData = get_json_info(fpath)

            protocol = '{}://'.format('https' if sslMode else 'http')
            mySSDP = RfSSDPServer(jsonData, '{}{}:{}{}'.format(protocol, hostname, port, '/redfish/v1'), hostname)
        
        logger.info("Serving Redfish mockup on port: {}".format(port))

        return myServer

def run_server(myServer):
        try:
            logger.info('running Server...')
            myServer.serve_forever()

        except KeyboardInterrupt:
            pass

        myServer.server_close()
        logger.info("Shutting down http server")

if __name__ == "__main__":
	
	root, response = setup()
	myserver = set_server(init(), root)
	run_server(myserver)
	
	print("666666666666666666666")

