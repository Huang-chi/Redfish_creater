Copyright 2017-2019 DMTF. All rights reserved.

# Redfish Service Validator

## About

The Redfish Service Validator is a python3 tool for checking conformance of any "device" with a Redfish service interface against Redfish CSDL schema.  The tool is designed to be device agnostic and is driven based on the Redfish specifications and schema intended to be supported by the device.

## Introduction

The Redfish Service Validator is an open source framework for checking conformance of any generic device with Redfish interface enabled against the DMTF defined Redfish schema and specifications. The tool is designed to be device agnostic and is driven purely based on the Redfish specifications intended to be supported by the device.

## Pre-requisites

The Redfish Service Validator is based on Python 3 and the client system is required to have the Python framework installed before the tool can be installed and executed on the system. Additionally, the following packages are required to be installed and accessible from the python environment:
* beautifulsoup4  - https://pypi.python.org/pypi/beautifulsoup4
* requests  - https://github.com/kennethreitz/requests (Documentation is available at http://docs.python-requests.org/)
* lxml - https://pypi.python.org/pypi/lxml

You may install the prerequisites by running:

    pip3 install -r requirements.txt

If you have a previous beautifulsoup4 installation, please use the following command:

    pip3 install beautifulsoup4 --upgrade

There is no dependency based on Windows or Linux OS. The result logs are generated in HTML format and an appropriate browser (Chrome, Firefox, IE, etc.) is required to view the logs on the client system.

## Installation

Place the RedfishServiceValidator.py into the desired tool root directory.  Create the following subdirectories in the tool root directory: "config", "logs", "SchemaFiles".  Place the example config.ini file in the "config" directory.  Place the CSDL Schema files to be used by the tool in the root of the schema directory, or the directory given in config.ini.

## Execution Steps

The Redfish Interop Validator is designed to execute as a purely command line interface tool with no intermediate inputs expected during tool execution. However, the tool requires various inputs regarding system details, DMTF schema files etc. which are consumed by the tool during execution to generate the conformance report logs. Below are the step by step instructions on setting up the tool for execution on any identified Redfish device for conformance test:

Modify the config\config.ini file to enter the system details under below section

[SystemInformation]

TargetIP = \<IPv4 address of the system under test\>

SystemInfo = \<Describes the system\>

UserName = \<User ID of Administrator on the system\>

Password = \<Password of the Administrator\>

ForceAuth = \<Force authentication on otherwise unsecure communication\>

AuthType = \<Type of authorization for above credentials (None,Basic,Session)\>

UseSSL = \<True / False\>

CertificateCheck = \<True / False\>

CertificateBundle = ca_bundle   Specify a bundle (file or directory) with certificates of trusted CAs. See [SelfSignedCerts.md](https://github.com/DMTF/Redfish-Service-Validator/blob/master/SelfSignedCerts.md) for tips on creating the bundle.

The Tool has an option to ignore SSL certificate check if certificate is not installed on the client system. The certificate check can be switched on or off using the below parameter of the config.ini file. By default the parameter is set to `False`.  UseSSL determines whether or not the https protocol is used.  If it is `False`, it will also disable certification.

[Options]

OemCheck = \<True / False\>    Specify if we want to check OEM properties

UriCheck = \<True / False\>    Specify if we want to compare resource URI with Redfish.Uris

VersionCheck = (string)     Specify version to test the service against, toggling protocol specific configuration (leave blank for automatic version)

LocalOnlyMode - (boolean) Only test properties against Schema placed in the root of MetadataFilePath.

ServiceMode - (boolean) Only test properties against Resources/Schema that exist on the Service

PreferOnline - (boolean) Prefer online/service schema over local schema.  This will also disable downloading all schema to specified metadata directory 

MetadataFilePath - (string) This attribute points to the location of the DMTF schema file location, populated by xml files

Schema_Pack - (string) URL path to an official zipped pack of DMTF Schema, to be extracted over the user's local schema directory.  Use 'latest' to pull the latest zip.  (To be used with option LocalOnlyMode)

Timeout - (integer) Interval of time before timing out a request

SchemaSuffix - (string) When searching for local hard drive schema, append this if unable to derive the expected xml from the service's metadata

HttpProxy - (URL) Proxy for HTTP requests to external URLs (example: `HttpProxy = http://192.168.1.1:8888`)

HttpsProxy - (URL) Proxy for HTTPS requests to external URLs (example: `HttpsProxy = http://192.168.1.1:8888`)

Note: HttpProxy/HttpsProxy do not apply to requests to the system under test, only to URLs external to the system.

Additional options are available for cached files, link limits, sampling and target payloads:

CacheMode = [Off, Prefer, Fallback] -- Options for using a cache, which will allow a user to override or fallback to a file on disk during a resource call on a service, replacing json response with local payload

CacheFilePath = Path to cache directory.  Default './cache'.  Consider using CacheMode if you need to test minor changes to a service's response on a particular payload's json

LinkLimit = TypeName:## -- Option to limit the amount of links accepted from collections, default LogEntry:20

Sample = (integer) Number of random members from large collections to validate. The default is to validate all members. All members will be validated if a value of zero or a negative number is specified. If a LinkLimit and Sample apply to a given collection, the LinkLimit takes precedence.

[Validator]

LogPath - (string) Path to store the logs for the generator

PayloadMode = [Default, Tree, Single, TreeFile, SingleFile] -- Options for the target of validation, allowing to specify a file or specific URI and traversal behavior

PayloadFilePath = Path to URI/File

Once the above details are updated for the system under test, the Redfish Service Validator can be triggered from a command prompt by typing the below command, with the option of verbosity:

    python3 RedfishServiceValidator.py -c config/config.ini (-v) (--verbose_checks) (--debug_logging)

Alternatively, all of these options are available through the command line.  __You may choose to overwrite some config entries through the command line__  In order to review these options, please run the command:

    python3 RedfishServiceValidator.py -h (-v) (--verbose_checks) (--debug_logging)

In order to run without a configuration file, the option --ip must be specified.

    python3 RedfishServiceValidator.py --ip host:port [...]

A GUI is also available to let a user fill in configuration options using a form, and then press a button to execute the test.  The following command will launch the GUI for the tool.

    python3 RedfishServiceValidatorGui.py

To run unittests, use the command:
    
    python3 -m unittest tests/*.py

In order to print a csv report out to the text log, the command --csv_report may be added to the command line.  To convert a previous HTML log into a csv file, use the following command:

    python3 tohtml.py htmllogfile

## Execution flow

1. Redfish Service Validator starts with the Service root Resource Schema by querying the service with the service root URI and getting all the device information, the resources supported and their links. Once the response of the Service root query is verified against its schema, the tool traverses through all the collections and Navigation properties returned by the service.
    * From the Metadata, collect all XML specified possible from the service, and store them in a tool-specified directory
2. For each navigation property/Collection of resource returned, it does following operations:
    * Reads all the Navigation/collection of resources from the respective resource collection schema file.
    * Reads the schema file related to the particular resource, collects all the information about individual properties from the resource schema file and stores them into a dictionary
    * Queries the service with the individual resource uri and validates all the properties returned against the properties collected from the schema file using a GET method making sure all the Mandatory properties are supported
3. Step 2 repeats until all of the URIs and resources are covered.

Upon validation of a resource, the following types of tests may occur:
* Upon reaching any resource, validate its @odata entries inside of its payload with regex.  If it fails, return a "failPayloadError".
* Attempt to initiate a Resource object, which requires an @odata.type and Schema of a valid JSON payload, otherwise return a "problemResource" or "exceptionResource" and terminate, otherwise "passGet"
* With the Resource initiated, begin to validate each Property available based on its Schema definition (sans annotations, additional props, is Case-Sensitive):
    * Check whether a Property is at first able to be nulled or is mandatory, and pass based on its Requirement or Nullability
    * For collections, validate each property inside of itself, and expects a list rather than a single Property, otherwise validate normally:
        * For basic types such as Int, Bool, DateTime, GUID, String, etc, check appropriate types, regex and ranges.
        * For Complex types, validate each property inside of the Complex, including annotations and additional properties
        * For Enum types, check and see if the given value exists in Schema's defined EnumType (Case-Sensitive)
        * For Entity types, check if the link given by @odata.id sends the client to an appropriate resource by the correct type, by performing a GET
* After reaching completion, perform the same routine with all Annotations available in the payload.
* If any unvalidated entries exist in the payload, determine whether or not additional properties are legitimate for this resource, otherwise throw a "failAdditional" error. 
 
## Conformance Logs - Summary and Detailed Conformance Report

The Redfish Service Validator generates an html report under the “logs” folder, named as ConformanceHtmlLog_MM_DD_YYYY_HHMMSS.html The report gives the detailed view of the individual properties checked, with the Pass/Fail/Skip/Warning status for each resource checked for conformance.

Additionally, there is a verbose log file that may be referenced to diagnose tool or schema problems when the HTML log is insufficient. 

## The Test Status

The test result for each GET operation will be reported as follows:
* PASS: If the operation is successful and returns a success code (E.g. 200, 204)
* FAIL: If the operation failed for reasons mentioned in GET method execution, or some configuration.
* SKIP: If the property or method being checked is not mandatory is not supported by the service.

## Limitations

Redfish Service Validator covers all the GET execution on the service. Below are certain points which are not in this scope.
* Patch/Post/Skip/Top/Head is not covered as part of Redfish Service Validator due to dependency on internal factor of the service.
* Redfish Service Validator does not cover testing of multiple service at once. To execute this, we have to re-run the tool by running it separately.
* Tool doesn't support @odata.context which use complex $entity path

## Building a Standalone Windows Executable

The module pyinstaller is used to package the environment as a standlone executable file; this can be installed with the following command:

    pip3 install pyinstaller

From a Windows system, the following command can be used to build a Windows executable file named RedfishServiceValidator.exe, which will be found in dist folder:

    pyinstaller -F -w -i redfish.ico -n RedfishServiceValidator.exe RedfishServiceValidatorGui.py

## Release Process

1. Update `CHANGELOG.md` with the list of changes since the last release
2. Update the `tool_version` variable in `RedfishServiceValidator.py` to reflect the new tool version
3. Push changes to Github
4. Create the standalone executable as described in the [above section](#building-a-standalone-windows-executable)
5. Create the zip file for the release containing the generated exe file and `README.md`
    * Name format: Redfish-Service-Validator-X.Y.Z-Windows.zip
6. Create a new release in Github with the zip file attached
