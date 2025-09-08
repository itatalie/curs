import json

import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture
def transactions():
    return pd.DataFrame(
        {
            "Дата платежа": ["01.01.2025", "01.01.2025", "02.01.2025", "03.01.2025"],
            "Категория": ["Такси", "Еда", "Такси", "Супермаркеты"],
            "Сумма операции": [-777, -555, -1312, -666],
        }
    )


def test_function_always_returns_error(transactions):
    """тест для возврата ошибки при неправильных данных"""
    result = json.loads(
        spending_by_category(transactions, category="Такси", date="01.04.2025")
    )

    assert "error" in result
    assert "Произошла ошибка" in result["error"]


def test_error_structure(transactions):
    """тест для возвращения правильной структуры ошибки"""
    result = json.loads(
        spending_by_category(transactions, category="Еда", date="01.02.2025")
    )

    assert isinstance(result, dict)
    assert "error" in result
    assert isinstance(result["error"], str)
