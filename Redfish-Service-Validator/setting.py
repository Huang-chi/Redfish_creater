import re

TOOL_VERSION = '1.3.9'
VERBO_NUM = 15

#######################################################

# default config
argparse2configparser = {
         'user': 'username', 'nochkcert': '!certificatecheck', 'ca_bundle': 'certificatebundle', 'schemamode': 'schemamode',
         'suffix': 'schemasuffix', 'schemadir': 'metadatafilepath', 'nossl': '!usessl', 'timeout': 'timeout', 'service': 'servicemode',
         'http_proxy': 'httpproxy', 'localonly': 'localonlymode', 'https_proxy': 'httpsproxy', 'passwd': 'password',
          'ip': 'targetip', 'logdir': 'logpath', 'desc': 'systeminfo', 'authtype': 'authtype',
          'payload': 'payloadmode+payloadfilepath', 'cache': 'cachemode+cachefilepath', 'token': 'token',
          'linklimit': 'linklimit', 'sample': 'sample', 'nooemcheck': '!oemcheck', 'preferonline': 'preferonline',
          'uri_check': 'uricheck', 'version_check': 'versioncheck'
          }
  
configset = {
         "targetip": str, "username": str, "password": str, "authtype": str, "usessl": bool, "certificatecheck": bool, "certificatebundle": str,
         "metadatafilepath": str, "cachemode": (bool, str), "cachefilepath": str, "schemasuffix": str, "timeout": int, "httpproxy": str, "httpsproxy": str,
         "systeminfo": str, "localonlymode": bool, "servicemode": bool, "token": str, 'linklimit': dict, 'sample': int, 'extrajsonheaders': str, 'extraxmlheaders': str, "schema_pack": str,
         "forceauth": bool, "oemcheck": bool, 'preferonline': bool, 'uricheck': bool, 'versioncheck': str
         }

defaultconfig = {
         'authtype': 'Basic',
         'username': "",
         'password': "",
         'token': "",
         'oemcheck': True,
         'certificatecheck': True,
         'certificatebundle': "",
         'metadatafilepath': './SchemaFiles/metadata',
         'cachemode': 'Off',
         'cachefilepath': './cache',
         'schemasuffix': '_v1.xml',
         'httpproxy': "",
         'httpsproxy': "",
         'localonlymode': False,
         'servicemode': False,
         'preferonline': False,
         'linklimit': {'LogEntry': 20},
         'sample': 0,
         'usessl': True,
         'timeout': 30,
         'schema_pack': None,
         'forceauth': False,
         'uricheck': False,
         'versioncheck': '',
         }
 
defaultconfig_by_version = {
         '1.0.0': {'schemasuffix': '.xml'},
         '1.0.6': {'uricheck': True}
         }
 
customval = {
         'linklimit': lambda v: re.findall('[A-Za-z_]+:[0-9]+', v)
         }
 
configSet = False
 
config = dict(defaultconfig)

