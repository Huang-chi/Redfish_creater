import os,sys

def verify_mockdir_is_exist(logger, mockDir,shortForm):
    if not shortForm:
            slashRedfishDir = os.path.join(mockDir, "redfish")
            if os.path.isdir(slashRedfishDir) is not True:
                logger.info("ERROR: Invalid Mockup Directory--no /redfish directory at top. Aborting")
                sys.stderr.flush()
                sys.exit(1)

    if shortForm:
        if os.path.isdir(mockDir) is not True or os.path.isfile(os.path.join(mockDir, "index.json")) is not True:
            logger.info("ERROR: Invalid Mockup Directory--dir or index.json does not exist")
            sys.stderr.flush()
            sys.exit(1)
