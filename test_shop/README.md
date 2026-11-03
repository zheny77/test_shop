# ParaBank: UI-тесты регистрации

Стек: Python, Selenium, Pytest, Allure.

## Запуск
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest                                  # chrome + firefox
pytest --browser chrome --headless      # один браузер, без окна
pytest -m negative                      # по маркеру
allure serve allure-results             # отчёт
```

## Структура
- `pages/` — BasePage и RegistrationPage (Page Object)
- `data/` — тестовые данные
- `tests/` — тесты (цепочки вызовов)
- `conftest.py` — фикстуры driver / base_url, мультибраузерность, скриншот + логи + сеть при падении
- `pytest.ini` — allure и маркеры
