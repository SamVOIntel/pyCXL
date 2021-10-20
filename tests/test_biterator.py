# External Dependencies
import pytest

# Package Imports
from tests.test_utils import (
    CHECKERBOARD_BYTES,
    CHECKERBOARD_BITS
)
from pyCXL.structs.biterator import Biterator

# ============================= Biterator Tests =============================
@pytest.mark.parametrize(
    "bytedata, expected_iterations, expected_output", [
        (CHECKERBOARD_BYTES, 16, CHECKERBOARD_BITS[2:]),
        (bytearray(b""), 0, "")
    ]
)
def test_Biterator_outputs_bins(bytedata, expected_iterations, expected_output):
    test_str = ""
    iterations = 0
    for available_bins in Biterator(bytedata):
        test_str += available_bins
        iterations += 1
    assert iterations == expected_iterations
    assert test_str == expected_output


def test_Biterator_throws_on_empty_next():
    data = Biterator(bytearray(b""))
    try:
        next(data)
        assert False
    except StopIteration:
        assert True


@pytest.mark.parametrize(
    "bytestring, expected", [
        (b"\xFF\x00", ["11111111", "00000000"]),
        (b"\xAA\x55", ["10101010", "01010101"]),
        (b"\x01", ["00000001"]),
        (b"\x01\x02\x03", ["00000001", "00000010", "00000011"]),
        (b"\xF0" * 100, ["11110000"]*100)
    ]
)
def test_Biterator_generates(bytestring, expected):
    # generator is a classmethod and does not need to be instantiated
    idx = 0
    for bins in Biterator.generator(bytestring):
        assert bins == expected[idx]
        idx += 1
