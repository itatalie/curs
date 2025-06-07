import json
import logging
from datetime import datetime, timedelta


def spending_by_category(transactions, category, date=None):
    """принимает на вход DataFrame с транзакциями, название категории и дату, а возвращает json-ответ с тратами"""
    try:
        if date is None:
            date_obj = datetime.now()
        else:
            date_obj = datetime.strptime(date, "%Y-%m-%d")

        start_date = date_obj - timedelta(days=90)

        filtered_transactions = transactions[
            (transactions["category"] == category)
            & (transactions["Date"] >= start_date)(transactions["Date"] <= date_obj)
        ]

        total_spending = filtered_transactions["amount"].sum()

        response = {
            "category": category,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": date_obj.strftime("%Y-%m-%d"),
            "total_spending": total_spending,
            "transactions": filtered_transactions.to_dict(orient="records"),
        }

        return json.dumps(response, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при формировании отчета: {e}")
        return json.dumps({"error": "Произошла ошибка при формировании отчета"}, ensure_ascii=False, indent=4)
