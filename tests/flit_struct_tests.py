# External Dependencies
import pytest

# Package imports
from src.structs.utils import (
    Biterator,
    BitField,
    BitStruct,
    FlitStruct
)

CHECKERBOARD_BITS = bytearray(b"\xAA\x55"*8)
"""
CHECKERBOARD_BITS should look like this in a bit map:

    1 0 1 0  1 0 1 0
    0 1 0 1  0 1 0 1
    1 0 1 0  1 0 1 0
    0 1 0 1  0 1 0 1
    
    1 0 1 0  1 0 1 0
    0 1 0 1  0 1 0 1
    1 0 1 0  1 0 1 0
    0 1 0 1  0 1 0 1
    
    1 0 1 0  1 0 1 0
    0 1 0 1  0 1 0 1
    1 0 1 0  1 0 1 0
    0 1 0 1  0 1 0 1
    
    1 0 1 0  1 0 1 0
    0 1 0 1  0 1 0 1
    1 0 1 0  1 0 1 0
    0 1 0 1  0 1 0 1
    
"""

@pytest.mark.parametrize(
    "bytedata", [
        CHECKERBOARD_BITS
    ]
)
def test_Biterator_outputs_bins(bytedata):
    data = Biterator(bytedata)
    test_str = next(data)
    assert test_str == '10101010'
    test_str = next(data)
    assert test_str == '01010101'
    test_str = next(data)
    assert test_str == '10101010'
    test_str = next(data)
    assert test_str == '01010101'
    test_str = next(data)
    assert test_str == '10101010'
    test_str = next(data)
    assert test_str == '01010101'
    test_str = next(data)
    assert test_str == '10101010'
    test_str = next(data)
    assert test_str == '01010101'


@pytest.mark.parametrize(
    "bytedata", [
        CHECKERBOARD_BITS
    ]
)
def test_Biterator_outputs_bins(bytedata):
    test_str = ""
    for bins in Biterator(bytedata):
        test_str += bins
    assert int(test_str, 2).to_bytes(len(test_str) // 8, 'big') == bytedata

