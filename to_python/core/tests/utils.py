def compare_lists(actual, expected):
    assert len(actual) == len(expected)

    for i in range(len(actual)):
        act = actual[i]
        exp = expected[i]
        if act != exp:
            print('\n')
            print('Index: ', i)
            print('Actual: ', act)
            print('Expected: ', exp)

            assert act == exp
