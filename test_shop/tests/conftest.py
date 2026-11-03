import pytest

from pages.registration_page import RegistrationPage


@pytest.fixture
def registration_page(driver, base_url) -> RegistrationPage:
    return RegistrationPage(driver, base_url).open_page()
