# External Dependencies
import pytest

# Package imports
from tests.test_utils import (
    CHECKERBOARD_BYTES,
    CHECKERBOARD_BITS,

    TINY_STRUCT,
    BYTE_ALIGNED_32BIT_STRUCT,
    lilBYTE_ALIGNED_32BIT_STRUCT,
    bigBYTE_ALIGNED_32BIT_STRUCT,

    NON_BYTE_ALIGNED_27BIT_STRUCT,
    lilNON_BYTE_ALIGNED_27BIT_STRUCT,
    bigNON_BYTE_ALIGNED_27BIT_STRUCT,

    OVERLAPPING_BOUNDARY_STRUCT,
    lilOVERLAPPING_BOUNDARY_STRUCT,
    bigOVERLAPPING_BOUNDARY_STRUCT,

    INCLUDES_RSVD_STRUCT,
    lilINCLUDES_RSVD_STRUCT,
    bigINCLUDES_RSVD_STRUCT,

    INCLUDES_ENUMS_STRUCT,
    lilINCLUDES_ENUMS_STRUCT,
    bigINCLUDES_ENUMS_STRUCT
)

# ============================= BitStruct Tests =============================
@pytest.mark.parametrize(
    "bitstruct, test_data, expected_values, expected_bins", [
        # struct so small only 1 byte is enough / no endianness required
        (TINY_STRUCT(),                   "0b101010",     (2, 5), "10101"),

        # struct size too big for no endianness / should throw
        (BYTE_ALIGNED_32BIT_STRUCT(),     "0b10101010",     False, None),
        (NON_BYTE_ALIGNED_27BIT_STRUCT(), "0b10101010",     False, None),
        (OVERLAPPING_BOUNDARY_STRUCT(),   "0b10101010",     False, None),

        # insufficent bits / should throw
        (lilBYTE_ALIGNED_32BIT_STRUCT(),     "0b1010101001010101",     False, None),
        (lilNON_BYTE_ALIGNED_27BIT_STRUCT(), "0b1010101001010101",     False, None),
        (lilOVERLAPPING_BOUNDARY_STRUCT(),   "0b1010101001010101",     False, None),
        (bigBYTE_ALIGNED_32BIT_STRUCT(),     "0b1010101001010101",     False, None),
        (bigNON_BYTE_ALIGNED_27BIT_STRUCT(), "0b1010101001010101",     False, None),
        (bigOVERLAPPING_BOUNDARY_STRUCT(),   "0b1010101001010101",     False, None),

        # sufficient bits, valid LE structs
        (lilBYTE_ALIGNED_32BIT_STRUCT(),     CHECKERBOARD_BITS(),  (10, 10, 85, 43605),           "10101010010101011010101001010101"),
        (lilNON_BYTE_ALIGNED_27BIT_STRUCT(), CHECKERBOARD_BITS(),  (85, 5, 1, 3410),              "101010100101010110101010010"),
        (lilOVERLAPPING_BOUNDARY_STRUCT(),   CHECKERBOARD_BITS(),  (697690, 693545302, 693610),   "1010101001010101101010100101010110101010010101011010101001010101101010"),

        # sufficient bits, valid BE structs
        (bigBYTE_ALIGNED_32BIT_STRUCT(),     CHECKERBOARD_BITS(),  (10, 10, 85, 21930),           "10101010010101011010101001010101"),
        (bigNON_BYTE_ALIGNED_27BIT_STRUCT(), CHECKERBOARD_BITS(),  (42, 11, 1, 2729),             "101010100101010110101010010"),
        (bigOVERLAPPING_BOUNDARY_STRUCT(),   CHECKERBOARD_BITS(),  (677290, 626697562, 693610),   "1010101001010101101010100101010110101010010101011010101001010101101010"),
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
    except NotImplementedError as err:
        assert str(err) == "You must specify an Endianness by using eiter LittleEndianBitStruct or BigEndianBitStruct"


# converting a bit struct to a bytearray is often extremely misleading.
@pytest.mark.parametrize(
    "bitstruct, test_data, expected_values, expected_bytes", [
        # struct so small only 1 byte is enough / no endianness required
        (TINY_STRUCT(),                   b"\xAA",     (2, 5), b"\x15"),

        # struct size too big for no endianness / should throw
        (BYTE_ALIGNED_32BIT_STRUCT(),     b"\xAA",     False, None),
        (NON_BYTE_ALIGNED_27BIT_STRUCT(), b"\xAA",     False, None),
        (OVERLAPPING_BOUNDARY_STRUCT(),   b"\xAA",     False, None),

        # insufficent bytes / should throw
        (BYTE_ALIGNED_32BIT_STRUCT(),           b"\xAA\x55",    False, None),
        (lilBYTE_ALIGNED_32BIT_STRUCT(),        b"\xAA\x55",    False, None),
        (bigBYTE_ALIGNED_32BIT_STRUCT(),        b"\xAA\x55",    False, None),
        (NON_BYTE_ALIGNED_27BIT_STRUCT(),       b"\xAA\x55",    False, None),
        (lilNON_BYTE_ALIGNED_27BIT_STRUCT(),    b"\xAA\x55",    False, None),
        (bigNON_BYTE_ALIGNED_27BIT_STRUCT(),    b"\xAA\x55",    False, None),
        (OVERLAPPING_BOUNDARY_STRUCT(),         b"\xAA\x55",    False, None),
        (lilOVERLAPPING_BOUNDARY_STRUCT(),      b"\xAA\x55",    False, None),
        (bigOVERLAPPING_BOUNDARY_STRUCT(),      b"\xAA\x55",    False, None),

        # sufficient Bytes / lil endian
        (lilBYTE_ALIGNED_32BIT_STRUCT(),     CHECKERBOARD_BYTES(),    (10, 10, 85, 43605), b"\xAA\x55\xAA\x55"),
        (lilNON_BYTE_ALIGNED_27BIT_STRUCT(), CHECKERBOARD_BYTES(),    (85, 5, 1, 3410),    b"\x05\x52\xAD\x52"),
        (lilOVERLAPPING_BOUNDARY_STRUCT(),   CHECKERBOARD_BYTES(),    (697690, 693545302, 693610), b"\x2A\x95\x6A\x95\x6A\x95\x6A\x95\x6A"),

        # sufficient Bytes / big endian
        (bigBYTE_ALIGNED_32BIT_STRUCT(),     CHECKERBOARD_BYTES(),    (10, 10, 85, 21930),  b"\xAA\x55\xAA\x55"),
        (bigNON_BYTE_ALIGNED_27BIT_STRUCT(), CHECKERBOARD_BYTES(),    (42, 11, 1, 2729),    b"\x05\x52\xAD\x52"),
        (bigOVERLAPPING_BOUNDARY_STRUCT(),   CHECKERBOARD_BYTES(),    (677290, 626697562, 693610), b"\x2A\x95\x6A\x95\x6A\x95\x6A\x95\x6A"),
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
    except NotImplementedError as err:
        assert str(err) == "You must specify an Endianness by using eiter LittleEndianBitStruct or BigEndianBitStruct"


# unclear why you would want to do this outside of an exercise in math
@pytest.mark.parametrize(
    "bitstruct, test_data, expected_int, expected_hex", [
        # lil endian
        (lilBYTE_ALIGNED_32BIT_STRUCT(),     CHECKERBOARD_BYTES(),       2857740885, "0xaa55aa55"),
        (lilNON_BYTE_ALIGNED_27BIT_STRUCT(), CHECKERBOARD_BYTES(),       89304402,    "0x552ad52"),
        (lilOVERLAPPING_BOUNDARY_STRUCT(),   CHECKERBOARD_BYTES(),       785529833239989622122, "0x2a956a956a956a956a"),

        # big endian
        (bigBYTE_ALIGNED_32BIT_STRUCT(),     CHECKERBOARD_BYTES(),       2857740885, "0xaa55aa55"),
        (bigNON_BYTE_ALIGNED_27BIT_STRUCT(), CHECKERBOARD_BYTES(),       89304402,    "0x552ad52"),
        (bigOVERLAPPING_BOUNDARY_STRUCT(),   CHECKERBOARD_BYTES(),       785529833239989622122, "0x2a956a956a956a956a"),
    ]
)
def test_BitStruct_converts_to_int_hex(bitstruct, test_data, expected_int, expected_hex):
    bitstruct.from_bytes(test_data)
    assert int(bitstruct) == expected_int
    assert hex(bitstruct) == expected_hex


@pytest.mark.parametrize(
    "bitstruct, test_data, expected_values", [
        # lil endian
        (lilBYTE_ALIGNED_32BIT_STRUCT(),       CHECKERBOARD_BYTES(),         (10, 10, 85, 43605)),
        (lilNON_BYTE_ALIGNED_27BIT_STRUCT(),   CHECKERBOARD_BYTES(),         (85, 5, 1, 3410)),
        (lilOVERLAPPING_BOUNDARY_STRUCT(),     CHECKERBOARD_BYTES(),         (697690, 693545302, 693610)),
        (lilINCLUDES_RSVD_STRUCT(),            CHECKERBOARD_BYTES(),         (10, 170)),
        (lilINCLUDES_ENUMS_STRUCT(),           CHECKERBOARD_BYTES(),         (10, 170)),

        # big endian
        (bigBYTE_ALIGNED_32BIT_STRUCT(),       CHECKERBOARD_BYTES(),         (10, 10, 85, 21930)),
        (bigNON_BYTE_ALIGNED_27BIT_STRUCT(),   CHECKERBOARD_BYTES(),         (42, 11, 1, 2729)),
        (bigOVERLAPPING_BOUNDARY_STRUCT(),     CHECKERBOARD_BYTES(),         (677290, 626697562, 693610)),
        (bigINCLUDES_RSVD_STRUCT(),            CHECKERBOARD_BYTES(),         (10, 170)),
        (bigINCLUDES_ENUMS_STRUCT(),           CHECKERBOARD_BYTES(),         (10, 170))
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

@pytest.mark.parametrize(
    "bitstruct, test_data, expected_values", [
        # sufficient Bytes / lil endian
        (lilBYTE_ALIGNED_32BIT_STRUCT(),     CHECKERBOARD_BYTES(),    (10, 10, 85, 43605)),
        (lilNON_BYTE_ALIGNED_27BIT_STRUCT(), CHECKERBOARD_BYTES(),    (85, 5, 1, 3410)),
        (lilOVERLAPPING_BOUNDARY_STRUCT(),   CHECKERBOARD_BYTES(),    (697690, 693545302, 693610)),

        # sufficient Bytes / big endian
        (bigBYTE_ALIGNED_32BIT_STRUCT(),     CHECKERBOARD_BYTES(),    (10, 10, 85, 21930)),
        (bigNON_BYTE_ALIGNED_27BIT_STRUCT(), CHECKERBOARD_BYTES(),    (42, 11, 1, 2729)),
        (bigOVERLAPPING_BOUNDARY_STRUCT(),   CHECKERBOARD_BYTES(),    (677290, 626697562, 693610)),
    ]
)
def test_BitStruct_supports_to_dict(bitstruct, test_data, expected_values):
    test_dict = bitstruct.to_dict()
    assert bitstruct.name in test_dict
    for field in bitstruct:
        assert field.name not in test_dict
    for val in test_dict[bitstruct.name].values():
        assert val == 0

    bitstruct.from_bytes(test_data)
    test_dict = bitstruct.to_dict()
    assert bitstruct.name in test_dict
    for field in bitstruct:
        assert field.name not in test_dict
    assert_idx = 0
    for val in test_dict[bitstruct.name].values():
        assert val == expected_values[assert_idx]
        assert_idx += 1

