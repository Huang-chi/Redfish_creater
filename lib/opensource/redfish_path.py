
def clean_path(path, isShort):
    """clean_path
    :param path:
    :param isShort:
    """
    path = path.strip('/')
    path = path.split('?', 1)[0]
    path = path.split('#', 1)[0]
    if isShort:
        path = path.replace('redfish/v1', '').strip('/')
    return path
