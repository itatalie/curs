import json
import logging


def simple_search(query, transactions):
    """функция принимает строку в формате списка словарей и возвращает json-ответ"""
    try:
        query = query.lower()
        filtered_transactions = [
            transaction
            for transaction in transactions
            if query in transaction.get("Категория", "").lower() or query in transaction.get("Описание", "").lower()
        ]
        return json.dumps(filtered_transactions, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Ошибка при выполнении поиска: {e}")
        return json.dumps({"error": "Произошла ошибка при выполнении поиска"}, ensure_ascii=False, indent=4)
