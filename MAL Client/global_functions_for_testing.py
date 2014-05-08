import base64
from os import path
import constants_for_testing


def connection_for_testing(url, data=None, headers=None):
    base64_url = base64.encodebytes(url.encode('utf-8')).replace(b'\n', b'').decode('utf-8')
    local_path = path.join(constants_for_testing.EXAMPLES_DIRECTORY, base64_url + '.html')
    with open(local_path, 'rb') as f:
        data = f.read()
    return data