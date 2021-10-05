# External Dependencies
import pytest

# Package imports
from src.structs.utils import (
    Biterator,
    BitField,
    BitStruct,
    BitStructCollection,
    FlitStruct
)

# Test Data
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


# Test Structs
class BYTE_ALIGNED_32BIT_STRUCT(BitStruct):

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=4,    name="Apple"),
                BitField(size=4,    name="Banana"),
                BitField(size=8,    name="Carrot"),
                BitField(size=16,   name="Durian")
            ], name="Byte Aligned 32bit Struct"
        )


class NON_BYTE_ALIGNED_27BIT_STRUCT(BitStruct):

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=7, name="Elderberry"),
                BitField(size=5, name="Fig"),
                BitField(size=2, name="Grapefruit"),
                BitField(size=13, name="Honeydew")
            ],
            name="Non Byte Aligned 27bit Struct"
        )


class OVERLAPPING_BOUNDARY_STRUCT(BitStruct):

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=20, name="Jackfruit"),
                BitField(size=30, name="Kumquat"),
                BitField(size=20, name="Lemon")
            ],
            name="Overlapping BitFields"
        )


# specifically sized structs
class EIGHT_BIT_STRUCT(BitStruct):
    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=2, name="OMG"),
                BitField(size=1, name="OHLAWD"),
                BitField(size=5, name="HE COMIN'!")
            ], name="8 bits"
        )

class TEN_BIT_STRUCT(BitStruct):
    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=3, name="Apple"),
                BitField(size=4, name="Banana"),
                BitField(size=3, name="Carrot")
            ], name="10 bits"
        )


class FIFTEEN_BIT_STRUCT(BitStruct):
    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=7, name="Durian"),
                BitField(size=8, name="Elderberry"),
            ], name="15 bits"
        )


class TWENTY_BIT_STRUCT(BitStruct):
    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=14, name="Fig"),
                BitField(size=2, name="Grapefruit"),
                BitField(size=4, name="Honeydew")
            ], name="20 bits"
        )


class THIRTY_BIT_STRUCT(BitStruct):
    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=14, name="Jackfruit"),
                BitField(size=5, name="Kumquat"),
                BitField(size=11, name="Lemon")
            ], name="30 bits"
        )


class FOURTY_BIT_STRUCT(BitStruct):
    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=7, name="Mango"),
                BitField(size=13, name="Nugget"),
                BitField(size=15, name="Orange"),
                BitField(size=5, name="Pear")
            ], name="40 bits"
        )


@pytest.mark.parametrize(
    "bytedata, expected_iterations, expected_output", [
        (CHECKERBOARD_BYTES, 16, CHECKERBOARD_BITS),
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
    except Exception:
        assert False


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
    assert bytes(bitfield) == expected


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
    except Exception:
        assert False


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
    except Exception:
        assert False


@pytest.mark.parametrize(
    "bitstruct, bin_input, byte_input, expected_int, expected_hex", [
        (BYTE_ALIGNED_32BIT_STRUCT(),     CHECKERBOARD_BITS, CHECKERBOARD_BYTES,  2857740885, "0xaa55aa55"),
        (NON_BYTE_ALIGNED_27BIT_STRUCT(), CHECKERBOARD_BITS, CHECKERBOARD_BYTES,  89304402,   "0x552ad52"),
        (OVERLAPPING_BOUNDARY_STRUCT(),   CHECKERBOARD_BITS, CHECKERBOARD_BYTES, 785529833239989622122, "0x2a956a956a956a956a")
    ]
)
def test_BitStruct_converts_to_int_hex(bitstruct, bin_input, byte_input, expected_int, expected_hex):
    bitstruct.from_bin(bin_input)
    assert int(bitstruct) == expected_int
    assert hex(bitstruct) == expected_hex

    bitstruct.from_bytes(byte_input)
    assert int(bitstruct) == expected_int
    assert hex(bitstruct) == expected_hex


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
    "bitstructs, expected", [
        (
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
            ], 128
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
            ], 128
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT()
            ], 128
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ], 128
        ),
        (
            [
                FIFTEEN_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ], 120
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                EIGHT_BIT_STRUCT(),
            ], 136
        )
    ]
)
def test_BitStructCollection_constructor_calculates_size(bitstructs, expected):
    testBitStruct = BitStructCollection(bitstructs=bitstructs)
    assert testBitStruct.size == expected


@pytest.mark.parametrize(
    "bitstructs", [
        (
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
            ]
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
            ]
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT()
            ]
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ]
        ),
        (
            [
                FIFTEEN_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ]
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                EIGHT_BIT_STRUCT(),
            ]
        )
    ]
)
def test_BitStructCollection_properties_throw_on_reassingment(bitstructs):
    testBitStruct = BitStructCollection(bitstructs=bitstructs)
    # each assignment should throw
    try:
        testBitStruct.structs = 9
        assert False
    except AttributeError:
        assert True
    except Exception:
        assert False
    try:
        testBitStruct.name = "Jolly good show!"
        assert False
    except AttributeError:
        assert True
    except Exception:
        assert False
    try:
        testBitStruct.size = b"\x06"
        assert False
    except AttributeError:
        assert True
    except Exception:
        assert False


@pytest.mark.parametrize(
    "bitstructs, expected", [
        (
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
            ], 7
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
            ], 4
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT()
            ], 7
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ], 6
        ),
        (
            [
                FIFTEEN_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ], 5
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                EIGHT_BIT_STRUCT(),
            ], 8
        )
    ]
)
def test_BitStructCollection_iterates(bitstructs, expected):
    test_BitStructCollection = BitStructCollection(bitstructs=bitstructs)
    iterations = 0
    for iteration in test_BitStructCollection:
        iterations += 1
    assert iterations == expected


@pytest.mark.parametrize(
    "bitstructs, bytedata, expected", [
        (
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
            ], CHECKERBOARD_BYTES,
            (
                # 8 bits
                2, 1, 10,
                # 10 bits
                2, 10, 6,
                # 15 bits
                84, 171,
                # 15 bits
                42, 85,
                # 20 bits
                10901, 1, 10,
                # 30 bits
                10582, 21, 342,
                # 30 bits
                10837, 21, 597
            )
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
            ], CHECKERBOARD_BYTES,
            (
                # 8 bits
                2, 1, 10,
                # 40 bit
                42, 6821, 11602, 21,
                # 40 bit
                85, 1370, 21165, 10,
                # 40 bit
                42, 6821, 11602, 21
            )
        ),
        (
            # too small
            [
                EIGHT_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
            ], bytearray(b"\xFF"),
            False
        )
    ]
)
def test_BitStructCollection_from_bytes_correct_assignment(bitstructs, bytedata, expected):
    testBitStructCollection = BitStructCollection(bitstructs=bitstructs)
    try:
        testBitStructCollection.from_bytes(bytedata)
        assert_idx = 0
        for struct in testBitStructCollection:
            for field in struct:
                assert field.value == expected[assert_idx]
                assert_idx += 1
    except ValueError as err:
        assert str(err) == "Not enough bytes to fill the BitStructCollection"
    except Exception:
        assert False


@pytest.mark.parametrize(
    "bitstructs, bytedata, expected", [
        (
            # alternating 1s and 0s
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
            ], CHECKERBOARD_BYTES,
            (
                # 8 bits
                2, 1, 10,
                # 10 bits
                2, 10, 6,
                # 15 bits
                84, 171,
                # 15 bits
                42, 85,
                # 20 bits
                10901, 1, 10,
                # 30 bits
                10582, 21, 342,
                # 30 bits
                10837, 21, 597
            )
        ),
        (
            # just enough bytes of all zeros
            [
                EIGHT_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
            ], CHECKERBOARD_BYTES,
            (
                # 8 bits
                2, 1, 10,
                # 40 bit
                42, 6821, 11602, 21,
                # 40 bit
                85, 1370, 21165, 10,
                # 40 bit
                42, 6821, 11602, 21
            )
        ),
    ]
)
def test_BitStructCollection_to_dict(bitstructs, bytedata, expected):
    # test collection should be initialized as all zeros
    testBitStructCollection = BitStructCollection(bitstructs=bitstructs, name="TEST")
    # make dictionary
    testDict = testBitStructCollection.to_dict()

    # the dictionary is keyed with the name
    assert testBitStructCollection.name in testDict
    # each struct is represented in the dictionary (no overwrites)
    assert len(testBitStructCollection) == len(testDict[testBitStructCollection.name])
    # order is preserved
    for i in range(len(testBitStructCollection)):
        assert testBitStructCollection[i].name in testDict[testBitStructCollection.name][i]
        # each field has the expected value (which should be 0)
        for field in testBitStructCollection[i]:
            assert field.value == 0 == testDict[testBitStructCollection.name][i][testBitStructCollection[i].name][field.name]

    # fill BitStructionCollection with actual data
    testBitStructCollection.from_bytes(bytedata)
    # remake dictionary
    testDict = testBitStructCollection.to_dict()

    # the dictionary is keyed with the name
    assert testBitStructCollection.name in testDict
    # each struct is represented in the dictionary (no overwrites)
    assert len(testBitStructCollection) == len(testDict[testBitStructCollection.name])
    # order is preserved
    for i in range(len(testBitStructCollection)):
        assert testBitStructCollection[i].name in testDict[testBitStructCollection.name][i]
        # each field has the expected value
        for field in testBitStructCollection[i]:
            assert field.value == testDict[testBitStructCollection.name][i][testBitStructCollection[i].name][
                field.name]


@pytest.mark.parametrize(
    "bitstructs, expected", [
        (
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
            ], True
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
            ], True
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                TWENTY_BIT_STRUCT()
            ], True
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ], True
        ),
        (
            # too small
            [
                FIFTEEN_BIT_STRUCT(),
                FOURTY_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ], False
        ),
        (
            # too big
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                EIGHT_BIT_STRUCT(),
            ], False
        )
    ]
)
def test_FlitStruct_must_be_128_bits(bitstructs, expected):
    try:
        FlitStruct(bitstructs=bitstructs, name="")
        assert expected
    except ValueError as err:
        assert f"FlitStructs MUST be 128 bits, was" in str(err)
        assert expected is False
    except Exception:
        assert False