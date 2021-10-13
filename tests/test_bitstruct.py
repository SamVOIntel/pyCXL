# External Dependencies
import pytest

# Package imports
from tests.test_utils import (
    CHECKERBOARD_BYTES,
    CHECKERBOARD_BITS,
    BYTE_ALIGNED_32BIT_STRUCT,
    NON_BYTE_ALIGNED_27BIT_STRUCT,
    OVERLAPPING_BOUNDARY_STRUCT,
    INCLUDES_RSVD_STRUCT,
    INCLUDES_ENUMS_STRUCT
)

# ============================= BitStruct Tests =============================
@pytest.mark.parametrize(
    "bitstruct, test_data, expected_values, expected_bins", [
        # sufficient bits
        (BYTE_ALIGNED_32BIT_STRUCT(),     CHECKERBOARD_BITS,  (10, 10, 85, 43605), "10101010010101011010101001010101"),
        (NON_BYTE_ALIGNED_27BIT_STRUCT(), CHECKERBOARD_BITS,  (85, 5, 1, 3410),    "101010100101010110101010010"),
        (OVERLAPPING_BOUNDARY_STRUCT(),   CHECKERBOARD_BITS,  (697690, 693545302, 693610), "1010101001010101101010100101010110101010010101011010101001010101101010"),

        # insufficent bits / should throw
        (BYTE_ALIGNED_32BIT_STRUCT(),     "1010101001010101",     False, None),
        (NON_BYTE_ALIGNED_27BIT_STRUCT(), "1010101001010101",     False, None),
        (OVERLAPPING_BOUNDARY_STRUCT(),   "1010101001010101",     False, None)

    ]
)
def test_BitStruct_outputs_from_binary(bitstruct, test_data, expected_values, expected_bins):
    try:
        bitstruct.from_bin(test_data)
        for idx, val in enumerate(expected_values):
            assert bitstruct[idx].value == val

        assert bitstruct.to_bin() == expected_bins
    except ValueError as err:
        assert str(err) == "Not enough bins to fill the BitStruct"


# converting a bit struct to a bytearray is often extremely misleading.
@pytest.mark.parametrize(
    "bitstruct, test_data, expected_values, expected_bytes", [
        # sufficient Bytes
        (BYTE_ALIGNED_32BIT_STRUCT(),     CHECKERBOARD_BYTES,       (10, 10, 85, 43605), b"\xAA\x55\xAA\x55"),
        (NON_BYTE_ALIGNED_27BIT_STRUCT(), CHECKERBOARD_BYTES,       (85, 5, 1, 3410),    b"\x05\x52\xAD\x52"),
        (OVERLAPPING_BOUNDARY_STRUCT(),   CHECKERBOARD_BYTES,       (697690, 693545302, 693610), b"\x2A\x95\x6A\x95\x6A\x95\x6A\x95\x6A"),

        # insufficent bytes / should throw
        (BYTE_ALIGNED_32BIT_STRUCT(),     b"\xAA\x55",     False, None),
        (NON_BYTE_ALIGNED_27BIT_STRUCT(), b"\xAA\x55",     False, None),
        (OVERLAPPING_BOUNDARY_STRUCT(),   b"\xAA\x55",     False, None)

    ]
)
def test_BitStruct_outputs_from_bytes(bitstruct, test_data, expected_values, expected_bytes):
    try:
        bitstruct.from_bytes(test_data)
        for idx, val in enumerate(expected_values):
            assert bitstruct[idx].value == val
        assert bytes(bitstruct) == expected_bytes
    except ValueError as err:
        assert str(err) == "Not enough bytes to fill the BitStruct"


# unclear why you would want to do this outside of an exercise in math
@pytest.mark.parametrize(
    "bitstruct, test_data, expected_int, expected_hex", [
        # sufficient Bytes
        (BYTE_ALIGNED_32BIT_STRUCT(),     CHECKERBOARD_BYTES,       2857740885, "0xaa55aa55"),
        (NON_BYTE_ALIGNED_27BIT_STRUCT(), CHECKERBOARD_BYTES,       89304402,    "0x552ad52"),
        (OVERLAPPING_BOUNDARY_STRUCT(),   CHECKERBOARD_BYTES,       785529833239989622122, "0x2a956a956a956a956a"),
    ]
)
def test_BitStruct_converts_to_int_hex(bitstruct, test_data, expected_int, expected_hex):
    bitstruct.from_bytes(test_data)
    assert int(bitstruct) == expected_int
    assert hex(bitstruct) == expected_hex


@pytest.mark.parametrize(
    "bitstruct, test_data, expected_values", [
        (BYTE_ALIGNED_32BIT_STRUCT(),       CHECKERBOARD_BYTES,         (10, 10, 85, 43605)),
        (NON_BYTE_ALIGNED_27BIT_STRUCT(),   CHECKERBOARD_BYTES,         (85, 5, 1, 3410)),
        (OVERLAPPING_BOUNDARY_STRUCT(),     CHECKERBOARD_BYTES,         (697690, 693545302, 693610)),
        (INCLUDES_RSVD_STRUCT(),            CHECKERBOARD_BYTES,         (10, 170)),
        (INCLUDES_ENUMS_STRUCT(),           CHECKERBOARD_BYTES,         (10, 170))
    ]
)
def test_BitStruct_converts_to_str(bitstruct, test_data, expected_values):
    empty_string = str(bitstruct)
    print_width = max([len(field.name) for field in bitstruct])
    assert f"\t{bitstruct.name}:\n" in empty_string
    for field in bitstruct:
        padding = " " * (print_width - len(field.name) + 4)

        if field.rsvd:
            assert f"{field.name}:{padding}0" not in empty_string
        else:
            assert f"{field.name}:{padding}0" in empty_string

        if field.enums:
            additional_print = field.enums.get(field.value, '')
            if additional_print:
                assert f"{field.name}:{padding}0\t{additional_print}" in empty_string

    bitstruct.from_bytes(test_data)
    filled_string = str(bitstruct)
    assert f"\t{bitstruct.name}:\n" in filled_string
    for field in bitstruct:
        padding = " " * (print_width - len(field.name) + 4)
        if field.rsvd:
            assert f"{field.name}:{padding}{field.value}" not in filled_string
        else:
            assert f"{field.name}:{padding}{field.value}" in filled_string

        if field.enums:
            additional_print = field.enums.get(field.value, '')
            if additional_print:
                assert f"{field.name}:{padding}{field.value}\t{additional_print}" in filled_string


@pytest.mark.parametrize(
    "bitstruct", [
        (BYTE_ALIGNED_32BIT_STRUCT()),
        (NON_BYTE_ALIGNED_27BIT_STRUCT()),
        (OVERLAPPING_BOUNDARY_STRUCT())
    ]
)
def test_BitStruct_throws_invalid_assignment(bitstruct):
    try:
        bitstruct.fields = 11
        assert False
    except AttributeError as err:
        assert str(err) == "Cannot modify BitStruct's fields"
    try:
        bitstruct.name = "TEST NAME"
        assert False
    except AttributeError as err:
        assert str(err) == "Cannot modify BitStruct's name"
    try:
        bitstruct.size = {"TEST KEY": "TEST VALUE"}
        assert False
    except AttributeError as err:
        assert str(err) == "Cannot modify BitStruct's size"
    try:
        bitstruct.idx = 0xFF
        assert False
    except AttributeError as err:
        assert str(err) == "Cannot modify BitStruct's index"


@pytest.mark.parametrize(
    "bitstruct, expected_bin", [
        (BYTE_ALIGNED_32BIT_STRUCT(),     "00010001000000010000000000000001"),
        (NON_BYTE_ALIGNED_27BIT_STRUCT(), "000000100001010000000000001"),
        (OVERLAPPING_BOUNDARY_STRUCT(),   "0000000000000000000100000000000000000000000000000100000000000000000001")
    ]
)
def test_BitStruct_supports_assignment_output(bitstruct, expected_bin):
    for field in bitstruct:
        field.value = 1
    assert bitstruct.to_bin() == expected_bin
