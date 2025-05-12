import json

import allure
import requests

BASE_URL = 'http://5.181.109.28:9090/api/v3/'

@allure.feature('Pet')
class TestPet:
    @allure.title('ID 31: Add new pet')
    def test_add_new_pet(self):
        with allure.step('Send request to add pet'):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
            response = requests.post(url=f'{BASE_URL}pet/', json=payload)

        with allure.step('Check response code'):
            assert response.status_code == 200, 'Code is not correct with expected response'

        with allure.step('Check text from response'):
            assert response.text == '{"id":1,"name":"Buddy","photoUrls":[],"tags":[],"status":"available"}', 'Text is not correct with expected response'

    @allure.title('ID 32: Get info about pet with ID')
    def test_get_info_about_pet_with_id(self):
        with allure.step('Send request to add pet'):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
            response = requests.post(url=f'{BASE_URL}pet/', json=payload)

        with allure.step('Get pet ID from response'):
            petId = response.json().get('id')

        with allure.step('Send request to get pet info by ID'):
            response = requests.get(url=f'{BASE_URL}pet/{petId}')

        with allure.step('Check response code'):
            assert response.status_code == 200, 'Code is not correct with expected response'

        with allure.step('Check text from response'):
            assert response.text == '{"id":1,"name":"Buddy","photoUrls":[],"tags":[],"status":"available"}', 'Text is not correct with expected response'

    @allure.title('ID 33: Update info about pet')
    def test_update_info_about_pet(self):
        with allure.step('Send request to add pet'):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
            response = requests.post(url=f'{BASE_URL}pet/', json=payload)

        with allure.step('Check response code'):
            assert response.status_code == 200, 'Code is not correct with expected response'

        with allure.step('Get pet ID from response'):
            petId = response.json().get('id')

        with allure.step('Send request to put new pet info'):
            payload = {
                "id": {petId},
                "name": "Buddy Updated",
                "status": "sold"
            }
            response = requests.put(url=f'{BASE_URL}pet',data=payload)

        with allure.step('Check response code'):
            assert response.status_code == 200, 'Code is not correct with expected response'

        with allure.step('Check text from response'):
            assert response.text == '{"id":1,"name":"Buddy Updated","status":"sold"}', 'Text is not correct with expected response'

    @allure.title('ID 34: Delete pet with ID')
    def test_delete_pet_with_id(self):
        with allure.step('Send request to add pet'):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
            response = requests.post(url=f'{BASE_URL}pet/', json=payload)

        with allure.step('Get pet ID from response'):
            petId = response.json().get('id')

        with allure.step('Send request to delete pet by ID'):
            response = requests.delete(url=f'{BASE_URL}pet/{petId}')

        with allure.step('Check response code'):
            assert response.status_code == 200, 'Code is not correct with expected response'

        with allure.step('Send request to check pet by ID'):
            response = requests.get(url=f'{BASE_URL}pet/{petId}')

    @allure.title('ID 37 Try to get info about non-existent pet')
    def test_get_info_about_nonexistent_pet(self):
        with allure.step('Send request to get info about non-existent pet'):
            response = requests.get(url=f'{BASE_URL}pet/9999')

        with allure.step('Check response code'):
            assert response.status_code == 404, 'Code is not correct with expected response'

        with allure.step('Check text from response'):
            assert response.text == 'Pet not found', 'Text is not correct with expected response'

    @allure.title('ID 38 Try to update non-existent pet')
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