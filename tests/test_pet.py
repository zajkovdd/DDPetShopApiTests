
import allure
import requests

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