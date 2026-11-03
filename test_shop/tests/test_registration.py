import allure
import pytest

from data.user import UserData


@allure.epic("ParaBank")
@allure.feature("Регистрация")
class TestRegistration:

    @allure.story("Позитивные сценарии")
    @allure.title("Успешная регистрация с валидными данными")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.registration
    def test_successful_registration(self, registration_page):
        user = UserData.random()
        (registration_page
         .fill_form(user)
         .submit()
         .should_be_registered(user.username))

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация без имени")
    @pytest.mark.negative
    @pytest.mark.registration
    def test_empty_first_name(self, registration_page):
        (registration_page
         .fill_form(UserData.random(first_name=""))
         .submit()
         .should_have_error("first_name", "First name is required.")
         .should_stay_on_registration())

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация без фамилии")
    @pytest.mark.negative
    @pytest.mark.registration
    def test_empty_last_name(self, registration_page):
        (registration_page
         .fill_form(UserData.random(last_name=""))
         .submit()
         .should_have_error("last_name", "Last name is required.")
         .should_stay_on_registration())

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация без адреса")
    @pytest.mark.negative
    @pytest.mark.registration
    def test_empty_address(self, registration_page):
        (registration_page
         .fill_form(UserData.random(address=""))
         .submit()
         .should_have_error("address", "Address is required.")
         .should_stay_on_registration())

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация без SSN")
    @pytest.mark.negative
    @pytest.mark.registration
    def test_empty_ssn(self, registration_page):
        (registration_page
         .fill_form(UserData.random(ssn=""))
         .submit()
         .should_have_error("ssn", "Social Security Number is required.")
         .should_stay_on_registration())

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация без логина")
    @pytest.mark.negative
    @pytest.mark.registration
    def test_empty_username(self, registration_page):
        (registration_page
         .fill_form(UserData.random(username=""))
         .submit()
         .should_have_error("username", "Username is required.")
         .should_stay_on_registration())

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с несовпадающими паролями")
    @pytest.mark.negative
    @pytest.mark.registration
    def test_passwords_do_not_match(self, registration_page):
        (registration_page
         .fill_form(UserData.random(confirm="Different123"))
         .submit()
         .should_have_error("confirm", "Passwords did not match.")
         .should_stay_on_registration())

    @allure.story("Негативные сценарии")
    @allure.title("Отправка полностью пустой формы")
    @pytest.mark.negative
    @pytest.mark.registration
    def test_empty_form(self, registration_page):
        (registration_page
         .submit()
         .should_have_error("first_name", "First name is required.")
         .should_have_error("last_name", "Last name is required.")
         .should_have_error("password", "Password is required.")
         .should_stay_on_registration())
