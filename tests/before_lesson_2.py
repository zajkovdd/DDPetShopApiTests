import json

import allure
import requests

BASE_URL = 'http://5.181.109.28:9090/api/v3/'

@allure.feature('Pet')
class TestPet:
    @allure.title('ID 31: Add new pet')
    def test_add_new_pet(self):
        with allure.step('Add data for new pet'):
            data = {"id": 1, "name": "Buddy", "status": "available"}

        with allure.step('Send request to add pet'):
            response = requests.post(url=f'{BASE_URL}pet/', json=data)

        with allure.step('Check response code'):
            assert response.status_code == 200, 'Code is not correct with expected response'

        with allure.step('Check text from response'):
            assert response.text == '{"id":1,"name":"Buddy","photoUrls":[],"tags":[],"status":"available"}', 'Text is not correct with expected response'

    @allure.title('ID 32: Get info about pet with ID')
    def test_get_info_about_pet_with_id(self):
        with allure.step('Add data for new pet'):
            data = {"id": 1, "name": "Buddy", "status": "available"}

        with allure.step('Send request to add pet'):
            response = requests.post(url=f'{BASE_URL}pet/', json=data)

        with allure.step('Get pet ID from response'):
            petId = response.json().get('id')

        with allure.step('Send request to get pet info by ID'):
            response = requests.get(url=f'{BASE_URL}pet/{petId}')

        with allure.step('Check response code'):
            assert response.status_code == 200, 'Code is not correct with expected response'

        with allure.step('Check text from response'):
            assert response.text == '{"id":1,"name":"Buddy","photoUrls":[],"tags":[],"status":"available"}', 'Text is not correct with expected response'

