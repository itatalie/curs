from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import (
    convert_date_string,
    filter_data_by_date_range,
    get_currency_data,
    get_month_start_date,
    get_stock_data,
    load_excel_data,
    load_user_settings,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "Date": ["2023-01-01", "2023-01-15"],
            "Category": ["Еда", "Такси"],
            "Amount": [-100, -200],
        }
    )


def test_load_excel_data(sample_df):
    """тест для загрузки данных из Excel"""
    with patch("pandas.read_excel", return_value=sample_df):
        result = load_excel_data()
        assert result.iloc[0]["Category"] == "Еда"
        assert result.iloc[1]["Category"] == "Такси"


def test_load_excel_data_missing_columns():
    """тест для загрузки Excel-файла с отсутствующими столбцами"""
    invalid_df = pd.DataFrame({"Invalid_Column": ["2023-01-01"], "Amount": [-100]})

    with patch("pandas.read_excel", return_value=invalid_df):
        result = load_excel_data()
        assert result.empty


def test_load_user_settings():
    """тест для загрузки пользовательских настроек"""
    mock_settings = '{"user_currencies": ["USD"], "user_stocks": ["AAPL"]}'
    with patch("builtins.open", mock_open(read_data=mock_settings)):
        result = load_user_settings()
        assert result["user_currencies"] == ["USD"]
        assert result["user_stocks"] == ["AAPL"]


def test_load_user_settings_error():
    """тест для обработки ошибки user_settings.json"""
    with patch("builtins.open", side_effect=Exception("File not found")):
        result = load_user_settings()
        assert result == {"user_currencies": [], "user_stocks": []}


def test_filter_data_by_date_range(sample_df):
    """тест для фильтра данных по диапазону дат"""
    sample_df["Date"] = pd.to_datetime(sample_df["Date"])
    filtered_data = filter_data_by_date_range(sample_df, "2023-01-01", "2023-01-10")
    assert len(filtered_data) == 1
    assert filtered_data.iloc[0]["Category"] == "Еда"


def test_get_currency_data():
    """тест для данных о курсах валют"""
    mock_response = {
        "start_date": "2023-01-01",
        "end_date": "2023-01-31",
        "rates": {"USD": {"2023-01-01": 75.0}},
    }

    start_date = convert_date_string("2023-01-01 00:00:00")
    end_date = convert_date_string("2023-01-31 00:00:00")

    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        result = get_currency_data(start_date, end_date)
        assert result["rates"]["USD"]["2023-01-01"] == 75.0


def test_get_currency_data_error():
    """тест для обработки ошибкок о валютах"""
    start_date = convert_date_string("2023-01-01 00:00:00")
    end_date = convert_date_string("2023-01-31 00:00:00")

    with patch("requests.get", side_effect=Exception("API error")):
        result = get_currency_data(start_date, end_date)
        assert result == {}


def test_get_stock_data():
    """тест для данных о ценах на акции"""
    mock_response = {"Time Series (Daily)": {"2023-01-31": {"4. close": "150.0"}}}

    start_date = convert_date_string("2023-01-01 00:00:00")
    end_date = convert_date_string("2023-01-31 00:00:00")

    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        result = get_stock_data(start_date, end_date)
        assert result["Time Series (Daily)"]["2023-01-31"]["4. close"] == "150.0"


def test_get_stock_data_error():
    """тест для обработки ошибок данных об акциях"""
    # Преобразуем строки в объекты datetime
    start_date = convert_date_string("2023-01-01 00:00:00")
    end_date = convert_date_string("2023-01-31 00:00:00")

    with patch("requests.get", side_effect=Exception("API error")):
        result = get_stock_data(start_date, end_date)
        assert result == {}


def test_convert_date_string():
    """тест для преобразования строки даты в объект datetime"""
    result = convert_date_string("2023-01-15 12:00:00")
    assert result.year == 2023
    assert result.month == 1
    assert result.day == 15
    assert result.hour == 12
    assert result.minute == 0
    assert result.second == 0


def test_convert_date_string_invalid_format():
    """тест для обработки ошибки при некорректном формате даты"""
    with pytest.raises(ValueError):
        convert_date_string("неправильная дата")


def test_get_month_start_date():
    """тест для получения даты начала месяца"""
    date_obj = convert_date_string("2023-01-15 12:00:00")
    result = get_month_start_date(date_obj)
    assert result.year == 2023
    assert result.month == 1
    assert result.day == 1
    assert result.hour == 0
    assert result.minute == 0
    assert result.second == 0
