from src.fetch.function import ListType
from src.fetch.fetch_function_list import get_function_list


def test_function_list_client_correct_partial_check():
    result = get_function_list(ListType.CLIENT)
    assert len(result) > 1000  # At 2021.02.09

    for fun in result:
        assert '#' not in fun.url
