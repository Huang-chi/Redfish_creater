
class rfService():
    def __init__(self, config, default_entries=[]):
        traverseLogger.info('Setting up service...')
        global currentService
        currentService = self
        self.config = config
        self.proxies = dict()
        self.active = False

        config['configuri'] = ('https' if config.get('usessl', True) else 'http') + '://' + config['targetip']
        httpprox = config['httpproxy']
        httpsprox = config['httpsproxy']
        self.proxies['http'] = httpprox if httpprox != "" else None
        self.proxies['https'] = httpsprox if httpsprox != "" else None

        # Convert list of strings to dict
        self.chkcertbundle = config['certificatebundle']
        chkcertbundle = self.chkcertbundle
        if chkcertbundle not in [None, ""] and config['certificatecheck']:
            if not os.path.isfile(chkcertbundle) and not os.path.isdir(chkcertbundle):
                self.chkcertbundle = None
                traverseLogger.error('ChkCertBundle is not found, defaulting to None')
        else:
            config['certificatebundle'] = None

        ChkCert = config['certificatecheck']
        AuthType = config['authtype']

        self.currentSession = None
        if not config.get('usessl', True) and not config['forceauth']:
            if config['username'] not in ['', None] or config['password'] not in ['', None]:
                traverseLogger.warning('Attempting to authenticate on unchecked http/https protocol is insecure, if necessary please use ForceAuth option.  Clearing auth credentials...')
                config['username'] = ''
                config['password'] = ''
        if AuthType == 'Session':
            certVal = chkcertbundle if ChkCert and chkcertbundle is not None else ChkCert
            # no proxy for system under test
            self.currentSession = rfSession(config['username'], config['password'], config['configuri'], None, certVal, self.proxies)
            self.currentSession.startSession()
        self.metadata = md.Metadata(traverseLogger)

        target_version = self.config.get('versioncheck')

        # get Version
        success, data, status, delay = self.callResourceURI('/redfish/v1')
        if not success:
            traverseLogger.warn('Could not get ServiceRoot')
        elif target_version in [None, '']:
            if 'RedfishVersion' not in data:
                traverseLogger.warn('Could not get RedfishVersion from ServiceRoot')
            else:
                traverseLogger.info('Redfish Version of Service: {}'.format(data['RedfishVersion']))
                target_version = data['RedfishVersion']

        # with Version, get default and compare to user defined values
        default_config_target = defaultconfig_by_version.get(target_version, dict())
        override_with = {k: default_config_target[k] for k in default_config_target if k in default_entries}
        if len(override_with) > 0:
            traverseLogger.info('CONFIG: RedfishVersion {} has augmented these tool defaults {}'.format(target_version, override_with))
        self.config.update(override_with)

        self.active = True

    def close(self):
        if self.currentSession is not None and self.currentSession.started:
            self.currentSession.killSession()
        self.active = False

    def getFromCache(URILink, CacheDir):
        CacheDir = os.path.join(CacheDir + URILink)
        payload = None
        if os.path.isfile(CacheDir):
            with open(CacheDir) as f:
                payload = f.read()
        if os.path.isfile(os.path.join(CacheDir, 'index.xml')):
            with open(os.path.join(CacheDir, 'index.xml')) as f:
                payload = f.read()
        if os.path.isfile(os.path.join(CacheDir, 'index.json')):
            with open(os.path.join(CacheDir, 'index.json')) as f:
                payload = json.loads(f.read())
            payload = navigateJsonFragment(payload, URILink)
        return payload

    @lru_cache(maxsize=128)
    def callResourceURI(self, URILink):
        """
        Makes a call to a given URI or URL

        param arg1: path to URI "/example/1", or URL "http://example.com"
        return: (success boolean, data, request status code)
        """
        # rs-assertions: 6.4.1, including accept, content-type and odata-versions
        # rs-assertion: handle redirects?  and target permissions
        # rs-assertion: require no auth for serviceroot calls
        if URILink is None:
            traverseLogger.warn("This URI is empty!")
            return False, None, -1, 0

        config = currentService.config
        proxies = currentService.proxies
        ConfigIP, UseSSL, AuthType, ChkCert, ChkCertBundle, timeout, Token = config['targetip'], config['usessl'], config['authtype'], \
                config['certificatecheck'], config['certificatebundle'], config['timeout'], config['token']
        CacheMode, CacheDir = config['cachemode'], config['cachefilepath']
        scheme, netloc, path, params, query, fragment = urlparse(URILink)
        inService = scheme is '' and netloc is ''
        scheme = ('https' if UseSSL else 'http') if scheme is '' else scheme
        netloc = ConfigIP if netloc is '' else netloc
        URLDest = urlunparse((scheme, netloc, path, params, query, fragment))

        payload, statusCode, elapsed, auth, noauthchk = None, '', 0, None, True

        isXML = False
        if "$metadata" in URILink or ".xml" in URILink[:-5]:
            isXML = True
            traverseLogger.debug('Should be XML')

        ExtraHeaders = None
        if 'extrajsonheaders' in config and not isXML:
            ExtraHeaders = config['extrajsonheaders']
        elif 'extraxmlheaders' in config and isXML:
            ExtraHeaders = config['extraxmlheaders']

        # determine if we need to Auth...
        if inService:
            noauthchk =  URILink in ['/redfish', '/redfish/v1', '/redfish/v1/odata'] or\
                '/redfish/v1/$metadata' in URILink

            auth = None if noauthchk else (config['username'], config['password'])
            traverseLogger.debug('dont chkauth' if noauthchk else 'chkauth')

            if CacheMode in ["Fallback", "Prefer"]:
                payload = rfService.getFromCache(URILink, CacheDir)

        if not inService and config['servicemode']:
            traverseLogger.debug('Disallowed out of service URI ' + URILink)
            return False, None, -1, 0

        # rs-assertion: do not send auth over http
        # remove UseSSL if necessary if you require unsecure auth
        if (not UseSSL and not config['forceauth']) or not inService or AuthType != 'Basic':
            auth = None
        # only send token when we're required to chkauth, during a Session, and on Service and Secure
        headers = {}
        headers.update(commonHeader)
        if not noauthchk and inService and UseSSL:
            traverseLogger.debug('successauthchk')
            if AuthType == 'Session':
                currentSession = currentService.currentSession
                headers.update({"X-Auth-Token": currentSession.getSessionKey()})
            elif AuthType == 'Token':
                headers.update({"Authorization": "Bearer " + Token})

        if ExtraHeaders is not None:
            headers.update(ExtraHeaders)

        certVal = ChkCertBundle if ChkCert and ChkCertBundle not in [None, ""] else ChkCert

        # rs-assertion: must have application/json or application/xml
        traverseLogger.debug('callingResourceURI {}with authtype {} and ssl {}: {} {}'.format(
            'out of service ' if not inService else '', AuthType, UseSSL, URILink, headers))
        response = None

        try:
            if payload is not None and CacheMode == 'Prefer':
                return True, payload, -1, 0
            response = requests.get(URLDest,
                                    headers=headers, auth=auth, verify=certVal, timeout=timeout)
                                    # proxies=proxies if not inService else None)  # only proxy non-service
            print("### response: ",response)
            expCode = [200]
            elapsed = response.elapsed.total_seconds()
            statusCode = response.status_code
            traverseLogger.debug('{}, {}, {},\nTIME ELAPSED: {}'.format(statusCode,
                                 expCode, response.headers, elapsed))
            if statusCode in expCode:
                contenttype = response.headers.get('content-type')
                if contenttype is None:
                    traverseLogger.error("Content-type not found in header: {}".format(URILink))
                    contenttype = ''
                if 'application/json' in contenttype:
                    traverseLogger.debug("This is a JSON response")
                    decoded = response.json(object_pairs_hook=OrderedDict)
                    # navigate fragment
                    decoded = navigateJsonFragment(decoded, URILink)
                    if decoded is None:
                        traverseLogger.error(
                                "The JSON pointer in the fragment of this URI is not constructed properly: {}".format(URILink))
                elif 'application/xml' in contenttype:
                    decoded = response.text
                elif 'text/xml' in contenttype:
                    # non-service schemas can use "text/xml" Content-Type
                    if inService:
                        traverseLogger.warn(
                                "Incorrect content type 'text/xml' for file within service {}".format(URILink))
                    decoded = response.text
                else:
                    traverseLogger.error(
                            "This URI did NOT return XML or Json contenttype, is this not a Redfish resource (is this redirected?): {}".format(URILink))
                    decoded = None
                    if isXML:
                        traverseLogger.info('Attempting to interpret as XML')
                        decoded = response.text
                    else:
                        try:
                            json.loads(response.text)
                            traverseLogger.info('Attempting to interpret as JSON')
                            decoded = response.json(object_pairs_hook=OrderedDict)
                        except ValueError:
                            pass

                return decoded is not None, decoded, statusCode, elapsed
            elif statusCode == 401:
                if inService and AuthType in ['Basic', 'Token']:
                    if AuthType == 'Token':
                        cred_type = 'token'
                    else:
                        cred_type = 'username and password'
                    raise AuthenticationError('Error accessing URI {}. Status code "{} {}". Check {} supplied for "{}" authentication.'
                                              .format(URILink, statusCode, responses[statusCode], cred_type, AuthType))

        except requests.exceptions.SSLError as e:
            traverseLogger.error("SSLError on {}: {}".format(URILink, repr(e)))
            traverseLogger.debug("output: ", exc_info=True)
        except requests.exceptions.ConnectionError as e:
            traverseLogger.error("ConnectionError on {}: {}".format(URILink, repr(e)))
            traverseLogger.debug("output: ", exc_info=True)
        except requests.exceptions.Timeout as e:
            traverseLogger.error("Request has timed out ({}s) on resource {}".format(timeout, URILink))
            traverseLogger.debug("output: ", exc_info=True)
        except requests.exceptions.RequestException as e:
            traverseLogger.error("Request has encounted a problem when getting resource {}: {}".format(URILink, repr(e)))
            traverseLogger.debug("output: ", exc_info=True)
        except AuthenticationError as e:
            raise e  # re-raise exception
        except Exception as e:
            traverseLogger.error("A problem when getting resource {} has occurred: {}".format(URILink, repr(e)))
            traverseLogger.debug("output: ", exc_info=True)
            if response and response.text:
                traverseLogger.debug("payload: {}".format(response.text))

        if payload is not None and CacheMode == 'Fallback':
            return True, payload, -1, 0
        return False, None, statusCode, elapsed