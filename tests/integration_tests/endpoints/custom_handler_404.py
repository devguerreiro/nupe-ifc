from json import loads

from rest_framework.test import APITestCase

from resources.const.messages.custom_handler_404 import ENDPOINT_NOT_FOUND
from tests.integration_tests.endpoints.setup.user import create_user_with_permissions_and_do_authentication


class CustomHandler404APITestCase(APITestCase):
    def test_endpoint_not_found(self):
        client = create_user_with_permissions_and_do_authentication()
        url = "not-found/"

        response = client.get(path=url)
        response_data = response.content.decode()

        self.assertEqual(loads(response_data).get("detail"), ENDPOINT_NOT_FOUND)
