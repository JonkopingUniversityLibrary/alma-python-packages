import unittest
import almaapi
from unittest.mock import patch


class AlmaAPITest(unittest.TestCase):

    def test_create_client(self):
        self.assertTrue(True, True)

        test_client = almaapi.AlmaAPI('test', '123456')
        self.assertEqual(test_client.api_url, 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/test/')
        self.assertEqual(test_client.api_key, '?apikey=123456')

    @patch('almaapi.http')
    def test_get_request(self, mock_http):

        def create_response(status, content):
            class Response(object):
                pass

            response = Response()
            response.status = status
            content = bytes(content, 'utf-8')
            return response, content

        test_client = almaapi.AlmaAPI('test', '123456')

        # Empty request should return False
        self.assertFalse(test_client.get())

        xml_content = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><web_service_result xmlns="http://com/exlibris/urm/general/xmlbeans"><errorsExist>true</errorsExist><errorList><error><errorCode>402203</errorCode><errorMessage>Test Error Message</errorMessage><trackingId>123456</trackingId></error></errorList></web_service_result>'

        mock_http.Http().request.return_value = create_response(400, xml_content)

        # Should raise AlmaAPIException when the request response status is not 200
        with self.assertRaises(almaapi.AlmaAPIException):
            test_client.get(request='request')
