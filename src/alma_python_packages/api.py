import httplib2 as http
import xml.etree.ElementTree as ElementTree
import json


class AlmaAPIException(Exception):
    """Custom docstring"""


class AlmaAPI:

    def __init__(self, api, api_key):
        self.api_url = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/' + api + '/'
        self.api_key = '?apikey=' + api_key

    def get(self, *, request=False, query_params=None):
        if request is False:
            return False

        __query_params__ = ''
        if query_params is not None:
            for key, value in query_params.items():
                __query_params__ += '&' + key + '=' + value

        url = self.api_url + request + self.api_key + __query_params__

        try:
            (response, content) = http.Http().request(url)
        except TimeoutError as e:
            raise AlmaAPIException('GET - ' + str(e))

        try:
            if response.status != 200:
                if query_params['format'] == 'json':
                    error_data = json.loads(content)
                    try:
                        error_message = error_data['errorList']['error'][0]['errorMessage']
                    except KeyError as e:
                        error_message = 'Unknown Error'
                    raise AlmaAPIException('GET - ' + str(response.status) + ' - ' + error_message)
                else:
                    root = ElementTree.ElementTree(ElementTree.fromstring(content)).getroot()
                    error_message = root[1][0][1].text
                    raise AlmaAPIException('GET - ' + str(response.status) + ' - ' + error_message)
        except ElementTree.ParseError as e:
            raise AlmaAPIException('GET - ' + str(e))

        return content.decode('utf8')

    def put(self, *, request=False, body=False, query_params=None, content_type='application/xml'):
        if request is False or body is False:
            return False

        __query_params__ = ''
        if query_params is not None:
            for key, value in query_params.items():
                __query_params__ += '&' + key + '=' + value

        url = self.api_url + request + self.api_key + __query_params__
        headers = {'Content-type': content_type}

        try:
            (response, content) = http.Http().request(url, 'PUT', headers=headers, body=body)
        except TimeoutError as e:
            raise AlmaAPIException('PUT - ' + str(e))

        if response.status != 200:
            if query_params['format'] == 'json':
                error_data = json.loads(content)
                try:
                    error_message = error_data['errorList']['error'][0]['errorMessage']
                except KeyError as e:
                    error_message = 'Unknown Error'
                raise AlmaAPIException('PUT - ' + str(response.status) + ' - ' + error_message)
            else:
                root = ElementTree.ElementTree(ElementTree.fromstring(content)).getroot()
                error_message = root[1][0][1].text
                raise AlmaAPIException('PUT - ' + str(response.status) + ' - ' + error_message)

        return content.decode('utf8')

    def post(self, *, request=False, body=False, query_params=None, content_type='application/xml'):
        if request is False or body is False:
            return False

        __query_params__ = ''
        if query_params is not None:
            for key, value in query_params.items():
                __query_params__ += '&' + key + '=' + value

        url = self.api_url + request + self.api_key + __query_params__
        headers = {'Content-type': content_type}

        try:
            (response, content) = http.Http().request(url, 'POST', headers=headers, body=body)
        except TimeoutError as e:
            raise AlmaAPIException('POST - ' + str(e))

        if response.status != 200:
            if query_params['format'] == 'json':
                error_data = json.loads(content)
                try:
                    error_message = error_data['errorList']['error'][0]['errorMessage']
                except KeyError as e:
                    error_message = 'Unknown Error'
                raise AlmaAPIException('POST - ' + str(response.status) + ' - ' + error_message)
            else:
                root = ElementTree.ElementTree(ElementTree.fromstring(content)).getroot()
                error_message = root[1][0][1].text
                raise AlmaAPIException('POST - ' + str(response.status) + ' - ' + error_message)

        return content.decode('utf8')
