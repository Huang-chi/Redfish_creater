# Product library
import re, sys, os
import argparse
import threading

import ssl
import logging
from http.server import HTTPServer

# Setting
from setting import *
# Private library
sys.path.append(os.path.join(os.path.dirname(__file__),'lib/opensource'))
from verify import verify_short_is_exist
from RfMockupModule import RfMockupServer

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
logger.addHandler(ch)


def main():

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
        parser.add_argument('-P', '--ssdp', action='store_true',
                            help='make mockup SSDP discoverable')

        args = parser.parse_args()
        hostname = args.host
        port = args.port
        mockDirPath = args.dir
        headers = args.headers
        responseTime = args.time
        timefromJson = args.T
        sslMode = args.ssl
        sslCert = args.cert
        sslKey = args.key
        ssdpStart = args.ssdp

        shortForm = True

        # check if mockup path was specified.  If not, use the built-in mockup
        if mockDirPath is None:
            mockDirPath = 'public-rackmount1'
            shortForm = True

        logger.info('Hostname: {}'.format(hostname))
        logger.info('Port: {}'.format(port))
        logger.info("Mockup directory path specified: {}".format(mockDirPath))
        logger.info("Response time: {} seconds".format(responseTime))

        # create the full path to the top directory holding the Mockup
        mockDir = os.path.realpath(mockDirPath)  # creates real full path including path for CWD to the -D<mockDir> dir path
        logger.info("Serving Mockup in absolute path: {}".format(mockDir))

        logger.info("ShortForm: {}".format(shortForm))
        verify_short_is_exist(logger, mockDir, shortForm)

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

        try:
            myServer.responseTime = float(responseTime)
        except ValueError as e:
            logger.info("Enter an integer or float value")
            sys.exit(2)

        mySSDP = None
        print("### ssdpStart: ",ssdpStart)
        if ssdpStart:
            from gevent import monkey
            monkey.patch_all()
            # construct path "mockdir/path/to/resource/<filename>"
            path, filename, jsonData = '/redfish/v1', 'index.json', None
            apath = myServer.mockDir
            rpath = clean_path(path, myServer.shortForm)
            fpath = os.path.join(apath, rpath, filename) if filename not in ['', None] else os.path.join(apath, rpath)
            if os.path.isfile(fpath):
                with open(fpath) as f:
                    jsonData = json.load(f)
                    f.close()
            else:
                jsonData = None
            protocol = '{}://'.format('https' if sslMode else 'http')
            mySSDP = RfSSDPServer(jsonData, '{}{}:{}{}'.format(protocol, hostname, port, '/redfish/v1'), hostname)

        logger.info("Serving Redfish mockup on port: {}".format(port))
        try:
            if mySSDP is not None:
                t2 = threading.Thread(target=mySSDP.start)
                t2.daemon = True
                t2.start()
            logger.info('running Server...')
            myServer.serve_forever()

        except KeyboardInterrupt:
            pass

        myServer.server_close()
        logger.info("Shutting down http server")

if __name__ == "__main__":
    main()
