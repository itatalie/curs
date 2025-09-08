import json

import pytest

from src.services import simple_search


@pytest.fixture
def example_data():
    return [
        {"Категория": "Магазин 1", "Описание": "Покупка продуктов", "Сумма": 1000},
        {"Категория": "Магазин 2", "Описание": "Оплата услуг", "Сумма": 500},
    ]


def test_simple_search_with_valid_data(example_data):
    """тест для поиска по валидным данным"""
    result_json = simple_search("магазин", example_data)
    result = json.loads(result_json)

    assert len(result) == 2
    assert any(
        item["Категория"] == "Магазин 1"
        and item["Описание"] == "Покупка продуктов"
        and item["Сумма"] == 1000
        for item in result
    )
    assert any(
        item["Категория"] == "Магазин 2"
        and item["Описание"] == "Оплата услуг"
        and item["Сумма"] == 500
        for item in result
    )


def test_simple_search_with_empty_data():
    """тест для поиска по пустым данным"""
    result_json = simple_search("магазин", [])
    result = json.loads(result_json)
    assert result == []


def test_search_case_insensitive(example_data):
    """тест для поиска без учета регистра"""
    result_json = simple_search("МАГАЗИН", example_data)
    result = json.loads(result_json)
    assert len(result) == 2
