import pytest

import nested

def test_Dict():
    d = nested.Dict()
    d[['key1', 'key2', 'key3']] = 'val1'
    assert d['key1']['key2']['key3'] == 'val1'
    d[['key1', 'key2', 'key4']] = 'val2'
    assert d['key1']['key2']['key4'] == 'val2'
    d[['key1', 'key5']] = 'val3'
    assert d['key1']['key5'] == 'val3'
    d[['key6']] = 'val4'
    assert d['key6'] == 'val4'