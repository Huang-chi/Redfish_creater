
def clean_path(path, isShort):
    """clean_path
    :param path:
    :param isShort:
    """
    path = path.strip('/')
    path = path.split('?', 1)[0]
    path = path.split('#', 1)[0]
    print("### Path: ",path)
    if isShort:
        path = path.replace('redfish/v1', '').strip('/')
    return path