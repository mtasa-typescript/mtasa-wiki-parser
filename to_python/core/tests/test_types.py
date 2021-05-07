from to_python.core.types import CompoundFunctionData


def test_compound_function_data():
    data = CompoundFunctionData(server=[], client=[])
    assert len([side for side, _ in data]) == 0

    data = CompoundFunctionData(server=[], client=[''])
    assert [side for side, _ in data] == ['client']
