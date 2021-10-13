# External Dependencies
import pytest

# Package Imports
from src.structs.bitfields import BitField

# ============================= BitField Tests =============================
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
    "bitfield, expected_int, expected_hex", [
        # small and simple
        (BitField(size=1,    name="Apple",           value=0), 0, "0x0"),
        (BitField(size=2,    name="Banana",          value=1), 1, "0x1"),
        (BitField(size=3,    name="Carrot",          value=2), 2, "0x2"),
        (BitField(size=4,    name="Durian",          value=3), 3, "0x3"),

        # somewhat larger
        (BitField(size=8,    name="Elderberry",      value=128), 128, "0x80"),
        (BitField(size=9,    name="Fig",             value=255), 255, "0xff"),
        (BitField(size=10,   name="Grapefruit",      value=37),  37, "0x25"),
        (BitField(size=11,   name="Honeydew",        value=177), 177, "0xb1"),

        # whacky
        (BitField(size=47,   name="Jackfruit",       value=2314286), 2314286, "0x23502e"),
        (BitField(size=21,   name="Kumquat",         value=98765),   98765, "0x181cd"),
        (BitField(size=30,   name="Lemon",           value=6),       6, "0x6"),
        (BitField(size=17,   name="Mango",           value=111111),  111111, "0x1b207")
    ]
)
def test_BitField_converts_to_int_hex(bitfield, expected_int, expected_hex):
    assert int(bitfield) == expected_int
    assert hex(bitfield) == expected_hex


@pytest.mark.parametrize(
    "bitfield, expected_str", [
        # small and simple
        (BitField(size=1,   name="Apple",           value=0), "Apple:\t0\n"),
        (BitField(size=2,   name="Banana",          value=1), "Banana:\t1\n"),
        (BitField(size=3,   name="Carrot",          value=2), "Carrot:\t2\n"),
        (BitField(size=4,   name="Durian",          value=3), "Durian:\t3\n"),

        # somewhat larger
        (BitField(size=8,   name="Elderberry",      value=128), "Elderberry:\t128\n"),
        (BitField(size=9,   name="Fig",             value=255), "Fig:\t255\n"),
        (BitField(size=10,  name="Grapefruit",      value=37),  "Grapefruit:\t37\n"),
        (BitField(size=11,  name="Honeydew",        value=177), "Honeydew:\t177\n"),

        # whacky
        (BitField(size=47,  name="Jackfruit",       value=2314286), "Jackfruit:\t2314286\n"),
        (BitField(size=21,  name="Kumquat",         value=98765),   "Kumquat:\t98765\n"),
        (BitField(size=30,  name="Lemon",           value=6),       "Lemon:\t6\n"),
        (BitField(size=17,  name="Mango",           value=111111),  "Mango:\t111111\n"),

        # rsvd
        (BitField(size=4,   name="Nectarine",       value=6, rsvd=True),    ""),
        (BitField(size=4,   name="Olive",           value=6, rsvd=False),   "Olive:\t6\n"),

        # enums
        (BitField(size=4,   name="Papaya",          value=6, enums={6: "six"}),    "Papaya:\t6\tsix\n"),
        (BitField(size=4,   name="Quince",          value=6, enums={5: "five"}),   "Quince:\t6\n"),

    ]
)
def test_BitField_converts_to_str(bitfield, expected_str):
    assert str(bitfield) == expected_str


@pytest.mark.parametrize(
    "bitfield, expected_dict", [
        # small and simple
        (BitField(size=1,    name="Apple",           value=0), {"Apple": 0}),
        (BitField(size=2,    name="Banana",          value=1), {"Banana": 1}),
        (BitField(size=3,    name="Carrot",          value=2), {"Carrot": 2}),
        (BitField(size=4,    name="Durian",          value=3), {"Durian": 3}),

        # somewhat larger
        (BitField(size=8,    name="Elderberry",      value=128), {"Elderberry": 128}),
        (BitField(size=9,    name="Fig",             value=255), {"Fig": 255}),
        (BitField(size=10,   name="Grapefruit",      value=37),  {"Grapefruit": 37}),
        (BitField(size=11,   name="Honeydew",        value=177), {"Honeydew": 177}),

        # whacky
        (BitField(size=47,   name="Jackfruit",       value=2314286), {"Jackfruit": 2314286}),
        (BitField(size=21,   name="Kumquat",         value=98765),   {"Kumquat": 98765}),
        (BitField(size=30,   name="Lemon",           value=6),       {"Lemon": 6}),
        (BitField(size=17,   name="Mango",           value=111111),  {"Mango": 111111})
    ]
)
def test_BitField_converts_to_dict(bitfield, expected_dict):
    assert bitfield.to_dict() == expected_dict


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
    # each value should be too large for the field size
    try:
        bitfield.value = setval
        assert False
    except ValueError as err:
        assert str(err) == f"{setval} is too large for the field size: {bitfield.size} bits"
    # these properties should be immutable, will always throw
    try:
        bitfield.name = "TEST NAME"
        assert False
    except AttributeError as err:
        assert str(err) == "name field cannot be modified"
    try:
        bitfield.size = setval
    except AttributeError as err:
        assert str(err) == "size field cannot be modified"
    try:
        bitfield.rsvd = setval
    except AttributeError as err:
        assert str(err) == "rsvd field cannot be modified"
    try:
        bitfield.enums = setval
    except AttributeError as err:
        assert str(err) == "enums field cannot be modified"