import json
import logging
import os
from datetime import datetime

import pandas as pd
import requests

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_user_settings():
    """згружает настройки из файла user_settings.json"""

    try:

        with open(
            os.path.join(os.path.dirname(__file__), "..", "user_settings.json"), "r"
        ) as file:

            return json.load(file)

    except Exception as e:

        logging.error(f"Ошибка при чтении user_settings.json: {e}")

        return {"user_currencies": [], "user_stocks": []}


def load_excel_data():
    """загружает данные из Excel-файла my_operations.xlsx"""

    try:

        file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "my_operations.xlsx"
        )

        transactions_df = pd.read_excel(file_path)

        required_columns = {"Date", "Category", "Amount"}

        if not required_columns.issubset(transactions_df.columns):

            logging.error(
                f"Файл Excel не содержит всех необходимых столбцов: {required_columns}"
            )

            return pd.DataFrame()

        logging.info(f"Данные успешно загружены из файла: {file_path}")

        return transactions_df

    except Exception as e:

        logging.error(f"Ошибка при загрузке данных из Excel: {e}")

        return pd.DataFrame()


def filter_data_by_date_range(df, start_date, end_date):
    """фильтрует данные по диапазону дат"""

    try:

        df["Date"] = pd.to_datetime(df["Date"])

        start_date = datetime.strptime(start_date, "%Y-%m-%d")

        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)

        filtered_data = df.loc[mask]

        logging.info(f"Данные отфильтрованы за период: {start_date} - {end_date}")

        return filtered_data

    except Exception as e:

        logging.error(f"Ошибка при фильтрации данных: {e}")

        return pd.DataFrame()


def get_currency_data(start_date, end_date):
    """получает данные о курсах валют за указанный диапазон дат"""

    user_settings = load_user_settings()

    currencies = user_settings.get("user_currencies", [])

    api_url = "https://api.exchangerate-api.com/v4/timeseries"

    params = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "symbols": ",".join(currencies),
    }

    try:

        response = requests.get(api_url, params=params)

        response.raise_for_status()

        data = response.json()

        if not data or "rates" not in data:

            logging.error("Некорректный ответ от API курсов валют.")

            return {}

        logging.info(f"Данные о курсах валют получены: {data}")

        return data

    except Exception as e:

        logging.error(f"Ошибка при запросе данных о валютах: {e}")

        return {}


def get_stock_data(start_date, end_date):
    """получает данные о ценах на акции за указанный диапазон дат"""

    user_settings = load_user_settings()

    stocks = user_settings.get("user_stocks", [])

    api_url = "https://www.alphavantage.co/query"

    params = {
        "function": "TIME_SERIES_DAILY",
        "apikey": os.getenv("API_STOCKS_KEY"),
        "symbols": ",".join(stocks),
        "date_from": start_date.strftime("%Y-%m-%d"),
        "date_to": end_date.strftime("%Y-%m-%d"),
    }

    try:

        response = requests.get(api_url, params=params)

        response.raise_for_status()

        data = response.json()

        if not data or "Time Series (Daily)" not in data:

            logging.error("Некорректный ответ от API цен на акции.")

            return {}

        logging.info(f"Данные о ценах на акции получены: {data}")

        return data

    except Exception as e:

        logging.error(f"Ошибка при запросе данных об акциях: {e}")

        return {}


def convert_date_string(date_str):
    """преобразует строку даты в объект datetime"""

    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


def get_month_start_date(date_obj):
    """возвращает дату начала месяца для заданной даты"""

    return date_obj.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
