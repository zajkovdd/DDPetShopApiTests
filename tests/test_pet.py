import allure
import jsonschema
import pytest
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3/'


@allure.feature('Pet')
class TestPet:
    @allure.title('Try to delete non-existent pet')
    def test_delete_nonexistent_pet(self):
        with allure.step('Send request to delete non-existent pet'):
            response = requests.delete(url=f'{BASE_URL}pet/9999')

        with allure.step('Check response code'):
            assert response.status_code == 200, 'Code is not correct with expected response'

        with allure.step('Check text from response'):
            assert response.text == 'Pet deleted', 'Text is not correct with expected response'

    @allure.title('Try to update non-existent pet')
    def test_update_nonexistent_pet(self):
        with allure.step('Send request to update non-existent pet'):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f'{BASE_URL}pet', json=payload)

        with allure.step('Check response code'):
            assert response.status_code == 404, 'Code is not correct with expected response'

        with allure.step('Check text from response'):
            assert response.text == 'Pet not found', 'Text is not correct with expected response'

    @allure.title('Try to get info about non-existent pet')
    def test_get_info_about_nonexistent_pet(self):
        with allure.step('Send request to get info about non-existent pet'):
            response = requests.get(url=f'{BASE_URL}pet/9999')

        with allure.step('Check response code'):
            assert response.status_code == 404, 'Code is not correct with expected response'

        with allure.step('Check text from response'):
            assert response.text == 'Pet not found', 'Text is not correct with expected response'

    @allure.title('Add new pet')
    def test_add_new_pet(self):
        with allure.step('Send request to add pet'):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
            response = requests.post(url=f'{BASE_URL}pet/', json=payload)
            response_json = response.json()

        with allure.step('Check response code and validate JSON_SCHEMA'):
            assert response.status_code == 200, 'Code is not correct with expected response'
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step('Check parameters of pet in response'):
            assert response_json["id"] == payload["id"], 'Pet id is not correct with expected response'
            assert response_json["name"] == payload["name"], 'Pet name is not correct with expected response'
            assert response_json["status"] == payload["status"], 'Pet status is not correct with expected response'

    @allure.title('Add new pet with all data')
    def test_add_new_pet_with_all_data(self):
        with allure.step('Send request to add pet'):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": [
                    "string"
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "status": "available"
            }
            response = requests.post(url=f'{BASE_URL}pet/', json=payload)
            response_json = response.json()

        with allure.step('Check response code and validate JSON_SCHEMA'):
            assert response.status_code == 200, 'Code is not correct with expected response'
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step('Check parameters of pet in response'):
            assert response_json["id"] == payload["id"], 'Pet id is not correct with expected response'
            assert response_json["name"] == payload["name"], 'Pet name is not correct with expected response'
            assert response_json["status"] == payload["status"], 'Pet status is not correct with expected response'
            assert response_json["category"] == payload["category"], 'Pet category is not correct with expected response'
            assert response_json["photoUrls"] == payload["photoUrls"], 'Pet photoUrls is not correct with expected response'
            assert response_json["tags"] == payload["tags"], 'Pet tags is correct with expected response'
            assert response_json["status"] == payload["status"], 'Pet status is not correct with expected response'

    @allure.title('Get info about pet with ID')
    def test_get_info_about_pet_with_id(self, create_pet):
        with allure.step('Get pet ID from response'):
            petId = create_pet['id']

        with allure.step('Send request to get pet info by ID'):
            response = requests.get(url=f'{BASE_URL}pet/{petId}')

        with allure.step('Check response code'):
            assert response.status_code == 200, 'Code is not correct with expected response'

        with allure.step('Check ID from response'):
            assert response.json()["id"] == petId, 'Pet ID is not correct with expected response'

    @allure.title('Update info about pet')
    def test_update_info_about_pet(self, create_pet):
        with allure.step('Get pet ID from response'):
            petId = create_pet['id']

        with allure.step('Send request to put new pet info'):
            payload = {
                "id": {petId},
                "name": "Buddy Updated",
                "status": "sold"
            }
            response = requests.put(url=f'{BASE_URL}pet',data=payload)

        with allure.step('Check response code'):
            assert response.status_code == 200, 'Code is not correct with expected response'

        with allure.step('Check updated info from response'):
            assert response.json()["name"] == payload["name"], 'Pet name is not correct with expected response'
            assert response.json()["status"] == payload["status"], 'Pet status is not correct with expected response'

    @allure.title('Delete pet with ID')
    def test_delete_pet_with_id(self, create_pet):
        with allure.step('Get pet ID from response'):
            petId = create_pet['id']

        with allure.step('Send request to delete pet by ID'):
            response = requests.delete(url=f'{BASE_URL}pet/{petId}')

        with allure.step('Check response code'):
            assert response.status_code == 200, 'Code is not correct with expected response'

        with allure.step('Send request to check pet by ID'):
            response = requests.get(url=f'{BASE_URL}pet/{petId}')

        with allure.step('Check response code'):
            assert response.status_code == 404, 'Code is not correct with expected response'

    @allure.title('Get list of pets by status')
    @pytest.mark.parametrize(
        'status, expected_status_code',
        [
            ('available', 200),
            ('pending', 200),
        ]
    )
    def test_get_list_of_pets_by_status(self, create_pet, status, expected_status_code):
        with allure.step('Send request to get list of pets by status'):
            response = requests.get(url=f'{BASE_URL}pet/findByStatus',params={'status': status})

        with allure.step('Check status code and data format'):
            assert response.status_code == expected_status_code, 'Code is not correct with expected response'
            assert isinstance(response.json(), list), 'Response is not a list'
