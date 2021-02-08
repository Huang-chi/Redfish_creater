############ Parameter  #################
HOST = '127.0.0.1'
SERVER_PORT = 8000
TOOL_VERSION = "1.1.4"

############## C code ###################
LIB_TEST = "./lib/private/output/libtest.so"

########### Python code #################
JSON_PATH = "./test/index.json"
REDFISH_DATA = "./redfish_data"
XML_PATH = "./test/index.xml"
CONFIG_PATH = "./test/explorer_config.json"
RESOURCE_XML_PATH = "./resource"
SPECIAL_RESOURCE = ['Settings','RedfishExtensions']
ALL_COLLECTIONS = ['AccountService','Chassis','EventService','SessionService','ComputerSystem','TaskService','ManagerAccount','Role','Power','Thermal','Session','EventDestination','VirtualMedia','ManagerNetworkProtocol','LogService','LogEntry','Processor','Bios']

ERROR = ['EthernetInterface','Storage','Volume','Drive','Memory','Manger','SerialInterface']

resource_domain = "http://redfish.dmtf.org/schemas/v1/"
REFERENCE_PROPERTY_TARGET = ['NavigationProperty','Property']

########### Redfish data  ###############
COPYRIGHT = "@Redfish.Copyright"
COPYRIGHT_CONTENT = "Copyright 2014-2019 DMTF. For the full DMTF copyright policy, see http://www.dmtf.org/about/policies/copyright."
INFO_FILENAME = "index.json"
REDFISH_DIR = "/redfish/v1"

########### Component command  ###############
COMMAND_DARWIN = "sysctl -n machdep.cpu.brand_string"
COMMAND_CPU_LINUX_CAT = "cat /proc/cpuinfo"
COMMAND_CPU_LINUX_LS = "lscpu"
COMMAND_MEMORY_LINUX_CAT = "cat /proc/meminfo"



