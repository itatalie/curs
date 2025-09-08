import json
import logging

from src.utils import (
    convert_date_string,
    filter_data_by_date_range,
    get_currency_data,
    get_month_start_date,
    get_stock_data,
    load_excel_data,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def home_page(date_str):
    """функция создана для главной страницы"""
    try:
        parsed_date = convert_date_string(date_str)
        month_start_date = get_month_start_date(parsed_date)

        transactions_df = load_excel_data()
        if transactions_df.empty:
            return create_error_response("Не удалось загрузить данные из Excel.")

        filtered_transactions = filter_data_by_date_range(
            transactions_df,
            month_start_date.strftime("%Y-%m-%d"),
            parsed_date.strftime("%Y-%m-%d"),
        )

        currency_info = get_currency_data(month_start_date, parsed_date)
        stock_info = get_stock_data(month_start_date, parsed_date)

        response_data = {
            "currencies": currency_info,
            "stocks": stock_info,
            "transactions": filtered_transactions.to_dict(orient="records"),
        }

        return create_success_response(response_data)

    except ValueError:
        logging.error("Неверный формат даты.")
        return create_error_response("Неверный формат даты.")
    except Exception as e:
        logging.error(f"Ошибка при обработке запроса: {e}")
        return create_error_response("Произошла ошибка при обработке запроса.")


def create_error_response(message):
    """генерирует json-ответ с ошибкой"""
    return json.dumps({"error": message}, ensure_ascii=False, indent=4)


def create_success_response(data):
    """генерирует json-ответ с успешными данными"""
    return json.dumps(data, ensure_ascii=False, indent=4)
