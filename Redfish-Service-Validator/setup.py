import argparse
from io import StringIO

from setting import *

def arg_setting(arglist=None):
 
    """
    Main program
    """
    argget = argparse.ArgumentParser(description='tool to test a service against a     collection of Schema, version {}'.format(TOOL_VERSION))
 
    # config
    argget.add_argument('-c', '--config', type=str, help='config file')
 
    # tool
    argget.add_argument('--desc', type=str, default='No desc', help='sysdescription for identifying logs')
    argget.add_argument('--payload', type=str, help='mode to validate payloads [Tr    ee, Single, SingleFile, TreeFile] followed by resource/filepath', nargs=2)
    argget.add_argument('-v', action='store_const', const=True, default=None, help    ='verbose log output to stdout (parameter-only)')
    argget.add_argument('--logdir', type=str, default='./logs', help='directory fo    r log files')
    argget.add_argument('--debug_logging', action="store_const", const=True, default=None, help='Output debug statements to text log, otherwise it only uses INFO (parameter-only)')
    argget.add_argument('--verbose_checks', action="store_const", const=True, default=None,
             help='Show all checks in logging (parameter-only)')
    argget.add_argument('--nooemcheck', action='store_const', const=True, default=    None, help='Don\'t check OEM items')
    argget.add_argument('--csv_report', action='store_true', help='print a csv rep    ort at the end of the log')
 
    # service
    argget.add_argument('-i', '--ip', type=str, help='ip to test on [host:port]')
    argget.add_argument('-u', '--user', type=str, help='user for basic auth')
    argget.add_argument('-p', '--passwd', type=str, help='pass for basic auth')
    argget.add_argument('--linklimit', type=str, help='Limit the amount of links i    n collections, formatted TypeName:## TypeName:## ..., default LogEntry:20 ', nargs    ='*')
    argget.add_argument('--sample', type=int, help='sample this number of members     from large collections for validation; default is to validate all members')
    argget.add_argument('--timeout', type=int, help='requests timeout in seconds')
    argget.add_argument('--nochkcert', action='store_const', const=True, default=None, help='ignore check for certificate')
    argget.add_argument('--nossl', action='store_const', const=True, default=None,     help='use http instead of https')
    argget.add_argument('--forceauth', action='store_const', const=True, default=None, help='force authentication on unsecure connections')
    argget.add_argument('--authtype', type=str, help='authorization type (None|Basic|Session|Token)')
    argget.add_argument('--localonly', action='store_const', const=True, default=None, help='only use locally stored schema on your harddrive')
    argget.add_argument('--preferonline', action='store_const', const=True, default=None, help='use online schema')
    argget.add_argument('--service', action='store_const', const=True, default=None, help='only use uris within the service')
    argget.add_argument('--ca_bundle', type=str, help='path to Certificate Authority bundle file or directory')
    argget.add_argument('--token', type=str, help='bearer token for authtype Token')
    argget.add_argument('--http_proxy', type=str, help='URL for the HTTP proxy')
    argget.add_argument('--https_proxy', type=str, help='URL for the HTTPS proxy')
    argget.add_argument('--cache', type=str, help='cache mode [Off, Fallback, Prefer] followed by directory to fallback or override problem service JSON payloads',nargs=2)
    argget.add_argument('--version_check', type=str, help='Change default tool configuration based on the version provided (default use target version)')

    # metadata
    argget.add_argument('--schemadir', type=str, help='directory for local schemafiles')
    argget.add_argument('--schema_pack', type=str, help='Deploy DMTF schema from zip distribution, for use with --localonly (Specify url or type "latest", overwrites current schema)')
    argget.add_argument('--suffix', type=str, help='suffix of local schema files ( for version differences)')

    args = argget.parse_args(arglist)
    return args


