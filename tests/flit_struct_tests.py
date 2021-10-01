# External Dependencies
import pytest

# Package imports
from src.structs.utils import (
    Biterator,
    BitField,
    BitStruct,
    FlitStruct
)

CHECKERBOARD_BYTES = bytearray(b"\xAA\x55"*8)
CHECKERBOARD_BITS = "1010101001010101" * 8
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

BYTE_ALIGNED_32BIT_STRUCT = BitStruct(
    bitfields=[
        BitField(size=4,    name="Apple"),
        BitField(size=4,    name="Banana"),
        BitField(size=8,    name="Carrot"),
        BitField(size=16,   name="Durian")
    ],
    name="Byte Aligned 32bit Struct"
)

NON_BYTE_ALIGNED_27BIT_STRUCT = BitStruct(
    bitfields=[
        BitField(size=7,    name="Elderberry"),
        BitField(size=5,    name="Fig"),
        BitField(size=2,    name="Grapefruit"),
        BitField(size=13,   name="Honeydew")
    ],
    name="Non Byte Aligned 27bit Struct"
)

OVERLAPPING_BOUNDARY_STRUCT = BitStruct(
    bitfields=[
        BitField(size=20,   name="Jackfruit"),
        BitField(size=30,   name="Kumquat"),
        BitField(size=20,   name="Lemon")
    ],
    name="Overlapping BitFields"
)

# specifically sized structs
EIGHT_BIT_STRUCT = BitStruct(
    bitfields=[
        BitField(size=2, name="OMG"),
        BitField(size=1, name="OHLAWD"),
        BitField(size=5, name="HE COMIN'!")
    ]
)

TEN_BIT_STRUCT = BitStruct(
    bitfields=[
        BitField(size=3, name="Apple"),
        BitField(size=4, name="Banana"),
        BitField(size=3, name="Carrot")
    ], name="10 bits"
)

FIFTEEN_BIT_STRUCT = BitStruct(
    bitfields=[
        BitField(size=7, name="Durian"),
        BitField(size=8, name="Elderberry"),
    ], name="15 bits"
)

TWENTY_BIT_STRUCT = BitStruct(
    bitfields=[
        BitField(size=14, name="Fig"),
        BitField(size=2,  name="Grapefruit"),
        BitField(size=4,  name="Honeydew")
    ], name="20 bits"
)

THIRTY_BIT_STRUCT = BitStruct(
    bitfields=[
        BitField(size=14, name="Jackfruit"),
        BitField(size=5,  name="Kumquat"),
        BitField(size=11, name="Lemon")
    ], name="30 bits"
)

FOURTY_BIT_STRUCT = BitStruct(
    bitfields=[
        BitField(size=7, name="Mango"),
        BitField(size=13, name="Nugget"),
        BitField(size=15, name="Orange"),
        BitField(size=5,  name="Pear")
    ], name="40 bits"
)


@pytest.mark.parametrize(
    "bytedata", [
        CHECKERBOARD_BYTES
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
    "bitfield, expected", [
        # small and simple
        (BitField(size=1,    name="Apple",           value=0), "0"),
        (BitField(size=2,    name="Banana",          value=1), "01"),
        (BitField(size=3,    name="Carrot",          value=2), "010"),
        (BitField(size=4,    name="Durian",          value=3), "0011"),

        # somewhat larger
        (BitField(size=8,    name="Elderberry",      value=128), "10000000"),
        (BitField(size=9,    name="Fig",             value=255), "011111111"),
        (BitField(size=10,   name="Grapefruit",      value=37),  "0000100101"),
        (BitField(size=11,   name="Honeydew",        value=177), "00010110001"),

        # whacky
        (BitField(size=47,   name="Jackfruit",       value=2314286), "00000000000000000000000001000110101000000101110"),
        (BitField(size=21,   name="Kumquat",         value=98765),   "000011000000111001101"),
        (BitField(size=30,   name="Lemon",           value=6),       "000000000000000000000000000110"),
        (BitField(size=17,   name="Mango",           value=111111),  "11011001000000111")
    ]
)
def test_BitField_outputs_valid_bin(bitfield, expected):
    assert bitfield.to_bin() == expected


@pytest.mark.parametrize(
    "bitfield, expected", [
        # small and simple
        (BitField(size=1,    name="Apple",           value=0), b"\x00"),
        (BitField(size=2,    name="Banana",          value=1), b"\x01"),
        (BitField(size=3,    name="Carrot",          value=2), b"\x02"),
        (BitField(size=4,    name="Durian",          value=3), b"\x03"),

        # somewhat larger
        (BitField(size=8,    name="Elderberry",      value=128), b"\x80"),
        (BitField(size=9,    name="Fig",             value=255), b"\x00\xFF"),
        (BitField(size=10,   name="Grapefruit",      value=37),  b"\x00\x25"),
        (BitField(size=11,   name="Honeydew",        value=177), b"\x00\xB1"),

        # whacky
        (BitField(size=47,   name="Jackfruit",       value=2314286), b"\x00\x00\x00\x23\x50\x2E"),
        (BitField(size=21,   name="Kumquat",         value=98765),   b"\x01\x81\xCD"),
        (BitField(size=30,   name="Lemon",           value=6),       b"\x00\x00\x00\x06"),
        (BitField(size=17,   name="Mango",           value=111111),  b"\01\xB2\x07")
    ]
)
def test_BitField_outputs_valid_bytes(bitfield, expected):
    assert bitfield.to_bytes() == expected


@pytest.mark.parametrize(
    "bitfield, setval", [
        # small and simple
        (BitField(size=1, name="Apple"),    2),
        (BitField(size=2, name="Banana"),   4),
        (BitField(size=3, name="Carrot"),   8),
        (BitField(size=4, name="Durian"),   16),

        # somewhat larger
        (BitField(size=8, name="Elderberry"),   256),
        (BitField(size=9, name="Fig"),          512),
        (BitField(size=10, name="Grapefruit"),  1024),
        (BitField(size=11, name="Honeydew"),    2048),

        # whacky
        (BitField(size=47, name="Jackfruit"),   140737488355328),
        (BitField(size=21, name="Kumquat"),     2097152),
        (BitField(size=30, name="Lemon"),       1073741824),
        (BitField(size=17, name="Mango"),       131072)
    ]
)
def test_BitField_throws_invalid_assignment(bitfield, setval):
    try:
        bitfield.value = setval
        assert False
    except ValueError as err:
        assert str(err) == f"{setval} is too large for the field size: {bitfield.size} bits"
    except Exception as err:
        assert False

@pytest.mark.parametrize(
    "bitstruct, test_data, expected_values, expected_bins", [
        (BYTE_ALIGNED_32BIT_STRUCT,     CHECKERBOARD_BITS,      (10, 10, 85, 43605), "10101010010101011010101001010101"),
        (NON_BYTE_ALIGNED_27BIT_STRUCT, CHECKERBOARD_BITS,      (85, 5, 1, 3410),    "101010100101010110101010010"),
        # need more bits for this one
        (OVERLAPPING_BOUNDARY_STRUCT,   CHECKERBOARD_BITS * 2,  (697690, 693545302, 693610), "1010101001010101101010100101010110101010010101011010101001010101101010"),
    ]
)
def test_BitStruct_outputs_from_valid_binary(bitstruct, test_data, expected_values, expected_bins):
    bitstruct.from_binary(test_data)

    for idx, val in enumerate(expected_values):
        assert bitstruct.fields[idx].value == val

    assert bitstruct.to_bin() == expected_bins


# converting a bit struct to a bytearray is often extremely misleading. DO NOT DO THIS.
@pytest.mark.parametrize(
    "bitstruct, test_data, expected_values, expected_bytes", [
        (BYTE_ALIGNED_32BIT_STRUCT,     CHECKERBOARD_BYTES,      (10, 10, 85, 43605), b"\xAA\x55\xAA\x55"),
        (NON_BYTE_ALIGNED_27BIT_STRUCT, CHECKERBOARD_BYTES,      (85, 5, 1, 3410),    b"\x05\x52\xAD\x52"),
        (OVERLAPPING_BOUNDARY_STRUCT,   CHECKERBOARD_BYTES,  (697690, 693545302, 693610), b"\x2A\x95\x6A\x95\x6A\x95\x6A\x95\x6A"),
    ]
)
def test_BitStruct_outputs_from_valid_bytes(bitstruct, test_data, expected_values, expected_bytes):
    bitstruct.from_bytes(test_data)
    assert bitstruct.to_bytes() == expected_bytes


@pytest.mark.parametrize(
    "bitstruct, bin_input, byte_input, expected_int, expected_hex", [
        (BYTE_ALIGNED_32BIT_STRUCT,     CHECKERBOARD_BITS, CHECKERBOARD_BYTES,  2857740885, "0xaa55aa55"),
        (NON_BYTE_ALIGNED_27BIT_STRUCT, CHECKERBOARD_BITS, CHECKERBOARD_BYTES,  89304402,   "0x552ad52"),
        # need more bits for this one
        (OVERLAPPING_BOUNDARY_STRUCT,   CHECKERBOARD_BITS * 2, CHECKERBOARD_BYTES, 785529833239989622122, "0x2a956a956a956a956a")
    ]
)
def test_BitStruct_converts_to_int_hex(bitstruct, bin_input, byte_input, expected_int, expected_hex):
    bitstruct.from_binary(bin_input)
    assert int(bitstruct) == expected_int
    assert hex(bitstruct) == expected_hex

    bitstruct.from_bytes(byte_input)
    assert int(bitstruct) == expected_int
    assert hex(bitstruct) == expected_hex


@pytest.mark.parametrize(
    "bitstruct, expected_bin", [
        (BYTE_ALIGNED_32BIT_STRUCT,     "00010001000000010000000000000001"),
        (NON_BYTE_ALIGNED_27BIT_STRUCT, "000000100001010000000000001"),
        (OVERLAPPING_BOUNDARY_STRUCT,   "0000000000000000000100000000000000000000000000000100000000000000000001")
    ]
)
def test_BitStruct_supports_assignment_output(bitstruct, expected_bin):
    for field in bitstruct.fields:
        field.value = 1
    assert bitstruct.to_bin() == expected_bin


@pytest.mark.parametrize(
    "bitstructs, expected", [
        (
            [
                EIGHT_BIT_STRUCT,
                TEN_BIT_STRUCT,
                FIFTEEN_BIT_STRUCT,
                FIFTEEN_BIT_STRUCT,
                TWENTY_BIT_STRUCT,
                THIRTY_BIT_STRUCT,
                THIRTY_BIT_STRUCT,
            ], True
        ),
        (
            [
                EIGHT_BIT_STRUCT,
                FOURTY_BIT_STRUCT,
                FOURTY_BIT_STRUCT,
                FOURTY_BIT_STRUCT,
            ], True
        ),
        (
            [
                EIGHT_BIT_STRUCT,
                TWENTY_BIT_STRUCT,
                TWENTY_BIT_STRUCT,
                TWENTY_BIT_STRUCT,
                TWENTY_BIT_STRUCT,
                TWENTY_BIT_STRUCT,
                TWENTY_BIT_STRUCT
            ], True
        ),
        (
            [
                EIGHT_BIT_STRUCT,
                FIFTEEN_BIT_STRUCT,
                FOURTY_BIT_STRUCT,
                FIFTEEN_BIT_STRUCT,
                TWENTY_BIT_STRUCT,
                THIRTY_BIT_STRUCT
            ], True
        ),
        (
            # too small
            [
                FIFTEEN_BIT_STRUCT,
                FOURTY_BIT_STRUCT,
                FIFTEEN_BIT_STRUCT,
                TWENTY_BIT_STRUCT,
                THIRTY_BIT_STRUCT
            ], False
        ),
        (
            # too big
            [
                EIGHT_BIT_STRUCT,
                TEN_BIT_STRUCT,
                FIFTEEN_BIT_STRUCT,
                FIFTEEN_BIT_STRUCT,
                TWENTY_BIT_STRUCT,
                THIRTY_BIT_STRUCT,
                THIRTY_BIT_STRUCT,
                EIGHT_BIT_STRUCT,
            ], False
        )
    ]
)
def test_FlitStruct_must_be_128_bits(bitstructs, expected):
    try:
        FlitStruct(bitstructs=bitstructs, name="")
        assert expected
    except ValueError as err:
        assert f"Expected 128 bits, was" in str(err)
        assert expected is False
    except Exception:
        assert False