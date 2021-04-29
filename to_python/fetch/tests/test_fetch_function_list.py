from typing import Set, Optional

import pytest

from fetch.fetch_function_list import get_function_list
from fetch.structures import ListType


@pytest.fixture
def get_function_list_fixture():
    return get_function_list(ListType.CLIENT)


def test_function_list_client_correct_partial_check(get_function_list_fixture):
    assert len(get_function_list_fixture) > 1000  # At 2021.02.09

    for fun in get_function_list_fixture:
        assert '#' not in fun.url


def test_function_list_client_grouped_by_categories(get_function_list_fixture):
    categories: Set[str] = set()
    current_category: Optional[str] = None

    for fun in get_function_list_fixture:
        if current_category != fun.category:
            if current_category:
                categories.add(current_category)

            assert fun.category not in categories
            current_category = fun.category

    assert True
