import allure
import jsonschema
import requests

from .schemas.inventory_schema import INVENTORY_SCHEMA
from .schemas.order_schema import ORDER_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3/'


@allure.feature('Store')
class TestStore:
    @allure.title('Add new order')
    def test_add_new_order(self):
        with allure.step('Send request to add order'):
            payload = {
                "id": 1,
                "petId": 2,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
            response = requests.post(url=f'{BASE_URL}store/order', json=payload)
            response_json = response.json()

        with allure.step('Check response code and validate JSON_SCHEMA'):
            assert response.status_code == 200, 'Code is not correct with expected response'
            jsonschema.validate(response_json, ORDER_SCHEMA)

        with allure.step('Check parameters of order in response'):
            assert response_json["id"] == payload["id"], 'Order id is not correct with expected response'
            assert response_json["petId"] == payload["petId"], 'Pet ID is not correct with expected response'
            assert response_json["quantity"] == payload["quantity"], 'Quantity is not correct with expected response'
            assert response_json["status"] == payload["status"], 'Status is not correct with expected response'
            assert response_json["complete"] == payload["complete"], 'Complete is not correct with expected response'

    @allure.title('Get info about order with ID = 1')
    def test_get_info_about_order_with_id_1(self, create_order):
        with allure.step('Send request to get order info by ID'):
            response = requests.get(url=f'{BASE_URL}store/order/1')
            response_json = response.json()

        with allure.step('Check response code and validate JSON_SCHEMA'):
            assert response.status_code == 200, 'Code is not correct with expected response'
            jsonschema.validate(response_json, ORDER_SCHEMA)

        with allure.step('Check parameters of order in response'):
            assert response_json["id"] == create_order["id"], 'Order id is not correct with expected response'
            assert response_json["petId"] == create_order["petId"], 'Pet ID is not correct with expected response'
            assert response_json["quantity"] == create_order["quantity"], 'Quantity is not correct with expected response'
            assert response_json["status"] == create_order["status"], 'Status is not correct with expected response'
            assert response_json["complete"] == create_order["complete"], 'Complete is not correct with expected response'

    @allure.title('Delete order with ID = 1')
    def test_delete_order_with_id_1(self):
        with allure.step('Send request to delete order with ID = 1'):
            response = requests.delete(url=f'{BASE_URL}store/order/1')

        with allure.step('Check response code'):
            assert response.status_code == 200, 'Code is not correct with expected response'

        with allure.step('Send request to check order with ID = 1'):
            response = requests.get(url=f'{BASE_URL}store/order/1')

        with allure.step('Check response code'):
            assert response.status_code == 404, 'Code is not correct with expected response'

    @allure.title('Try to get info about non-existent order')
    def test_get_info_about_nonexistent_order(self):
        with allure.step('Send request to get info about non-existent order'):
            response = requests.get(url=f'{BASE_URL}store/order/9999')

        with allure.step('Check response code'):
            assert response.status_code == 404, 'Code is not correct with expected response'

    @allure.title('Get inventory from store')
    def test_get_inventory_from_store(self):
        with allure.step('Send request to get inventory from store'):
            response = requests.get(url=f'{BASE_URL}store/inventory')
            response_json = response.json()

        with allure.step('Check response code and validate JSON_SCHEMA'):
            assert response.status_code == 200, 'Code is not correct with expected response'
            jsonschema.validate(response_json, INVENTORY_SCHEMA)
            assert isinstance(response_json, dict), 'Response is not a dictionary'