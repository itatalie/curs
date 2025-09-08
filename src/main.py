import json
from datetime import datetime

from src.reports import spending_by_category
from src.services import simple_search
from src.utils import load_excel_data
from src.views import home_page


def main():
    """главная функция для входа в программу"""

    try:

        transactions = load_excel_data()

        if transactions.empty:

            print("Ошибка: не удалось загрузить данные транзакций")

            return

        print("\n1. Анализ расходов за последние 3 месяца:")

        report = spending_by_category(transactions, "Еда", "2024-05-15")

        print(json.loads(report))

        print("\n2. Поиск по операциям:")

        search_result = simple_search("магазин", transactions.to_dict("records"))

        print(json.loads(search_result))

        print("\n3. Главная страница (последний месяц):")

        homepage_data = home_page(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        print(json.loads(homepage_data))

    except Exception as e:

        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":

    print("=== ФИНАНСОВЫЙ АНАЛИЗАТОР ===")

    print("Загрузка данных...")

    main()
