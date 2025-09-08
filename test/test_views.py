import json
from unittest.mock import patch

import pandas as pd

from src.views import home_page


def test_home_page_success():
    """тест для правильного формирования ответа"""
    test_data = {
        "Дата": ["2023-01-01"],
        "Номер карты": ["1234"],
        "Сумма операции": [-100],
        "Категория": ["Еда"],
    }

    with (
        patch("src.views.load_excel_data", return_value=pd.DataFrame(test_data)),
        patch(
            "src.views.filter_data_by_date_range", return_value=pd.DataFrame(test_data)
        ),
        patch("src.views.get_currency_data", return_value={"USD": 75.0}),
        patch("src.views.get_stock_data", return_value={"AAPL": 150.0}),
    ):
        result = home_page("2023-01-15 12:00:00")
        data = json.loads(result)

        assert data["currencies"] == {"USD": 75.0}
        assert data["stocks"] == {"AAPL": 150.0}
        assert data["transactions"][0]["Категория"] == "Еда"


def test_home_page_invalid_date():
    """тест для обработки неверного формата даты"""
    result = home_page("неправильная дата")
    assert json.loads(result)["error"] == "Неверный формат даты."


def test_home_page_empty_excel():
    """тест для пустого Excel-файла"""
    with patch("src.views.load_excel_data", return_value=pd.DataFrame()):
        result = home_page("2023-01-15 12:00:00")
        assert json.loads(result)["error"] == "Не удалось загрузить данные из Excel."


def test_home_page_api_error():
    """тест ошибки API"""
    test_df = pd.DataFrame(
        {
            "Дата": ["2023-01-01"],
            "Номер карты": ["1234"],
            "Сумма операции": [-100],
            "Категория": ["Еда"],
        }
    )

    with (
        patch("src.views.load_excel_data", return_value=test_df),
        patch("src.views.get_currency_data", side_effect=Exception("API error")),
    ):
        result = home_page("2023-01-15 12:00:00")
        assert "Произошла ошибка" in json.loads(result)["error"]
