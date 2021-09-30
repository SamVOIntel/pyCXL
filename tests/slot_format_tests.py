# External Dependencies
import pytest

# Python Imports
import importlib
import re

# Package Imports
from src.structs.utils import FlitParser

SLOT_FORMAT_IMPORT_PREFIX = r"src.structs."


@pytest.mark.parametrize(
    "slot_format_source", [
        "H2D_M2S", "D2H_S2M"
    ]
)
def test_CXL_cache_slot_formats_are_16_bytes(slot_format_source):
    """
    Tests if slot format structs are 16 bytes
    """
    module = importlib.import_module(SLOT_FORMAT_IMPORT_PREFIX + slot_format_source + "_formats")
    slot_formats_names = [sf for sf in dir(module) if sf.endswith('slot_format')]
    for slot_format_name in slot_formats_names:
        slot_format = getattr(module, slot_format_name)
        size = 0
        for struct in slot_format:
            for array_element in struct[1]:
                for field_tuple in array_element:
                    size += field_tuple[1]
        print(slot_format_name)
        assert size == 128


CHECKERBOARD_BITS = bytearray(b"\xAA\x55"*8)
"""
The following test checks if the SlotFormatParser class is correctly parsing bits.

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
    "struct", [
        [
            ["struct0", [[
                        ("Apples",          4),
                        ("Bananas",         4),
                        ("Carrots",         8),
                        ("Durian",          16),
                    ]]
             ],
            ["struct1", [[
                        ("Elderberries",    16),
                        ("Fig",             8),
                        ("Grapefruit",      4),
                        ("Honeydew",        4)
                    ]]
             ],
            ["struct2", [[
                        ("Jackfruit",       4),
                        ("Kumquat",         16),
                        ("Lemon",           4),
                        ("Mango",           8)
                    ]]
             ],
            ["struct3", [[
                        ("Nectarine",       8),
                        ("Olives",          4),
                        ("Papaya",          16),
                        ("Quince",          4)
                    ]]
             ],
        ],
    ]
)
def test_flitparser_init_as_zeros(struct):
    slot_format = FlitParser(struct)
    assert hasattr(slot_format, "struct0")
    assert hasattr(slot_format, "struct1")
    assert hasattr(slot_format, "struct2")
    assert hasattr(slot_format, "struct3")

    assert slot_format.struct0[0].Apples        == 0
    assert slot_format.struct0[0].Bananas       == 0
    assert slot_format.struct0[0].Carrots       == 0
    assert slot_format.struct0[0].Durian        == 0

    assert slot_format.struct1[0].Elderberries  == 0
    assert slot_format.struct1[0].Fig           == 0
    assert slot_format.struct1[0].Grapefruit    == 0
    assert slot_format.struct1[0].Honeydew      == 0

    assert slot_format.struct2[0].Jackfruit     == 0
    assert slot_format.struct2[0].Kumquat       == 0
    assert slot_format.struct2[0].Lemon         == 0
    assert slot_format.struct2[0].Mango         == 0

    assert slot_format.struct3[0].Nectarine     == 0
    assert slot_format.struct3[0].Olives        == 0
    assert slot_format.struct3[0].Papaya        == 0
    assert slot_format.struct3[0].Quince        == 0


@pytest.mark.parametrize(
    "struct", [
        [
            ["struct0", [[
                        ("Apples",          4),
                        ("Bananas",         4),
                        ("Carrots",         8),
                        ("Durian",          16),
                    ]]
             ],
            ["struct1", [[
                        ("Elderberries",    16),
                        ("Fig",             8),
                        ("Grapefruit",      4),
                        ("Honeydew",        4)
                    ]]
             ],
            ["struct2", [[
                        ("Jackfruit",       4),
                        ("Kumquat",         16),
                        ("Lemon",           4),
                        ("Mango",           8)
                    ]]
             ],
            ["struct3", [[
                        ("Nectarine",       8),
                        ("Olives",          4),
                        ("Papaya",          16),
                        ("Quince",          4)
                    ]]
             ],
        ],
    ]
)
def test_flitparser_init_as_zeros_converts_to_other_types(struct):
    slot_format = FlitParser(struct)
    assert int(slot_format)         == 0
    assert hex(slot_format)         == '0x0'
    assert bytes(slot_format)       == b"\x00" * 16


@pytest.mark.parametrize(
    "struct, data", [
        [[
            ["struct0", [[
                        ("Apples",          4),
                        ("Bananas",         4),
                        ("Carrots",         8),
                        ("Durian",          16),
                    ]]
             ],
            ["struct1", [[
                        ("Elderberries",    16),
                        ("Fig",             8),
                        ("Grapefruit",      4),
                        ("Honeydew",        4)
                    ]]
             ],
            ["struct2", [[
                        ("Jackfruit",       4),
                        ("Kumquat",         16),
                        ("Lemon",           4),
                        ("Mango",           8)
                    ]]
             ],
            ["struct3", [[
                        ("Nectarine",       8),
                        ("Olives",          4),
                        ("Papaya",          16),
                        ("Quince",          4)
                    ]]
             ],
        ], CHECKERBOARD_BITS],
    ]
)
def test_byte_aligned_is_addressible_slot_format(struct, data):
    slot_format = FlitParser(struct)
    slot_format.from_buffer(data)
    assert hasattr(slot_format, "struct0")
    assert hasattr(slot_format, "struct1")
    assert hasattr(slot_format, "struct2")
    assert hasattr(slot_format, "struct3")

    assert slot_format.struct0[0].Apples == 10
    assert slot_format.struct0[0].Bananas == 10
    assert slot_format.struct0[0].Carrots == 85
    assert slot_format.struct0[0].Durian == 43605

    assert slot_format.struct1[0].Elderberries == 43605
    assert slot_format.struct1[0].Fig == 170
    assert slot_format.struct1[0].Grapefruit == 5
    assert slot_format.struct1[0].Honeydew == 5

    assert slot_format.struct2[0].Jackfruit == 10
    assert slot_format.struct2[0].Kumquat == 42330
    assert slot_format.struct2[0].Lemon == 10
    assert slot_format.struct2[0].Mango == 85

    assert slot_format.struct3[0].Nectarine == 170
    assert slot_format.struct3[0].Olives == 5
    assert slot_format.struct3[0].Papaya == 23205
    assert slot_format.struct3[0].Quince == 5


@pytest.mark.parametrize(
    "struct, data", [
        [[
            ["struct0", [[
                        ("Apples",          1),
                        ("Bananas",         2),
                        ("Carrots",         3),
                        ("Durian",          4),
                    ]]
            ],
            ["struct1", [[
                        ("Elderberries",    5),
                        ("Fig",             6),
                        ("Grapefruit",      7),
                        ("Honeydew",        8)
                    ]]
            ],
            ["struct2", [[
                        ("Jackfruit",       9),
                        ("Kumquat",         10),
                        ("Lemon",           11),
                        ("Mango",           12)
                    ]]

            ],
            ["struct3", [[
                        ("Nectarine",       13),
                        ("Olives",          14),
                        ("Papaya",          15),
                        ("Quince",          8)
                    ]]
             ],
        ], CHECKERBOARD_BITS],
    ]
)
def test_non_byte_aligned_is_addressible_slot_format(struct, data):
    slot_format = FlitParser(struct)
    slot_format.from_buffer(data)

    assert slot_format.struct0[0].Apples == 1
    assert slot_format.struct0[0].Bananas == 1
    assert slot_format.struct0[0].Carrots == 2
    assert slot_format.struct0[0].Durian == 9

    assert slot_format.struct1[0].Elderberries == 10
    assert slot_format.struct1[0].Fig == 53
    assert slot_format.struct1[0].Grapefruit == 37
    assert slot_format.struct1[0].Honeydew == 90

    assert slot_format.struct2[0].Jackfruit == 330
    assert slot_format.struct2[0].Kumquat == 725
    assert slot_format.struct2[0].Lemon == 342
    assert slot_format.struct2[0].Mango == 2709

    assert slot_format.struct3[0].Nectarine == 3410
    assert slot_format.struct3[0].Olives == 11092
    assert slot_format.struct3[0].Papaya == 21930
    assert slot_format.struct3[0].Quince == 85


@pytest.mark.parametrize(
    "struct, data", [
        [[
            ["struct0", [[
                        ("Apples",          11),
                        ("Bananas",         23),
                        ("Carrots",          3),
                        ("Durian",           6),
                    ]] * 2
            ],
            ["struct1", [[
                        ("Elderberries",    15),
                        ("Fig",              2),
                        ("Grapefruit",       1),
                        ("Honeydew",         3)
                    ]] * 2
            ],
        ], CHECKERBOARD_BITS],
    ]
)
def test_non_byte_aligned_sequential_duplicate_structs_are_addressible_slot_format(struct, data):
    slot_format = FlitParser(struct)
    slot_format.from_buffer(data)
    assert len(slot_format.struct0) == 2
    assert len(slot_format.struct1) == 2

    assert slot_format.struct0[0].Apples == 1362
    assert slot_format.struct0[0].Bananas == 5679446
    assert slot_format.struct0[0].Carrots == 5
    assert slot_format.struct0[0].Durian == 18

    assert slot_format.struct0[1].Apples == 1386
    assert slot_format.struct0[1].Bananas == 4896074
    assert slot_format.struct0[1].Carrots == 5
    assert slot_format.struct0[1].Durian == 42

    assert slot_format.struct1[0].Elderberries == 19125
    assert slot_format.struct1[0].Fig == 1
    assert slot_format.struct1[0].Grapefruit == 0
    assert slot_format.struct1[0].Honeydew == 2

    assert slot_format.struct1[1].Elderberries == 22185
    assert slot_format.struct1[1].Fig == 1
    assert slot_format.struct1[1].Grapefruit == 0
    assert slot_format.struct1[1].Honeydew == 5


@pytest.mark.parametrize(
    "struct, data", [
        [[
            ["struct0", [[
                        ("Apples",          11),
                        ("Bananas",         23),
                        ("Carrots",          3),
                        ("Durian",           6),
                    ]]
            ],
            ["struct1", [[
                        ("Elderberries",    15),
                        ("Fig",              2),
                        ("Grapefruit",       1),
                        ("Honeydew",         3)
                    ]]
            ],
            ["struct0", [[
                        ("Apples",          11),
                        ("Bananas",         23),
                        ("Carrots",          3),
                        ("Durian",           6),
                    ]]
            ],
            ["struct1", [[
                        ("Elderberries",    15),
                        ("Fig",              2),
                        ("Grapefruit",       1),
                        ("Honeydew",         3)
                    ]]
            ],
        ], CHECKERBOARD_BITS],
    ]
)
def test_byte_aligned_non_sequential_duplicate_structs_are_addressible_slot_format(struct, data):
    slot_format = FlitParser(struct)
    slot_format.from_buffer(data)
    assert len(slot_format.struct0) == 2
    assert len(slot_format.struct1) == 2

    assert slot_format.struct0[0].Apples == 1362
    assert slot_format.struct0[0].Bananas == 5679446
    assert slot_format.struct0[0].Carrots == 5
    assert slot_format.struct0[0].Durian == 18

    assert slot_format.struct1[0].Elderberries == 22185
    assert slot_format.struct1[0].Fig == 1
    assert slot_format.struct1[0].Grapefruit == 0
    assert slot_format.struct1[0].Honeydew == 5

    assert slot_format.struct0[1].Apples == 1362
    assert slot_format.struct0[1].Bananas == 5679446
    assert slot_format.struct0[1].Carrots == 5
    assert slot_format.struct0[1].Durian == 18

    assert slot_format.struct1[1].Elderberries == 22185
    assert slot_format.struct1[1].Fig == 1
    assert slot_format.struct1[1].Grapefruit == 0
    assert slot_format.struct1[1].Honeydew == 5


@pytest.mark.parametrize(
    "struct, data", [
        [[
            ["struct0", [[
                        ("Apples",           7),
                        ("Bananas",          7),
                        ("Carrots",          7),
                        ("Durian",           7),
                    ]]
            ],
            ["struct1", [[
                        ("Elderberries",     1),
                        ("Fig",              45),
                        ("Grapefruit",       18),
                        ("Honeydew",         8)
                    ]]
            ],
            ["struct0", [[
                        ("Apples",           7),
                        ("Bananas",          7),
                        ("Carrots",          7),
                        ("Durian",           7),
                    ]]
            ],
        ], CHECKERBOARD_BITS],
    ]
)
def test_non_byte_aligned_non_sequential_duplicate_structs_are_addressible_slot_format(struct, data):
    slot_format = FlitParser(struct)
    slot_format.from_buffer(data)
    assert len(slot_format.struct0) == 2
    assert len(slot_format.struct1) == 1

    assert slot_format.struct0[0].Apples == 85
    assert slot_format.struct0[0].Bananas == 21
    assert slot_format.struct0[0].Carrots == 53
    assert slot_format.struct0[0].Durian == 37

    assert slot_format.struct1[0].Elderberries == 0
    assert slot_format.struct1[0].Fig == 24916559222441
    assert slot_format.struct1[0].Grapefruit == 88741
    assert slot_format.struct1[0].Honeydew == 90

    assert slot_format.struct0[1].Apples == 82
    assert slot_format.struct0[1].Bananas == 86
    assert slot_format.struct0[1].Carrots == 84
    assert slot_format.struct0[1].Durian == 85


@pytest.mark.parametrize(
    "struct, data", [
        [[
            ["struct0", [[
                        ("Apples",          4),
                        ("Bananas",         4),
                        ("Carrots",         8),
                        ("Durian",          16),
                    ]]
             ],
            ["struct1", [[
                        ("Elderberries",    16),
                        ("Fig",             8),
                        ("Grapefruit",      4),
                        ("Honeydew",        4)
                    ]]
             ],
            ["struct2", [[
                        ("Jackfruit",       4),
                        ("Kumquat",         16),
                        ("Lemon",           4),
                        ("Mango",           8)
                    ]]
             ],
            ["struct3", [[
                        ("Nectarine",       8),
                        ("Olives",          4),
                        ("Papaya",          16),
                        ("Quince",          4)
                    ]]
             ],
        ], CHECKERBOARD_BITS],
    ]
)
def test_slot_format_parse_values(struct, data):
    slot_format = FlitParser(struct)
    slot_format.from_buffer(data)

    text = str(slot_format)

    assert len(re.findall(r"Apples:\s*10", text)) == 1
    assert len(re.findall(r"Bananas:\s*10", text)) == 1
    assert len(re.findall(r"Carrots:\s*85", text)) == 1
    assert len(re.findall(r"Durian:\s*43605", text)) == 1

    assert len(re.findall(r"Elderberries:\s*43605", text)) == 1
    assert len(re.findall(r"Fig:\s*170", text)) == 1
    assert len(re.findall(r"Grapefruit:\s*5", text)) == 1
    assert len(re.findall(r"Honeydew:\s*5", text)) == 1

    assert len(re.findall(r"Jackfruit:\s*10", text)) == 1
    assert len(re.findall(r"Kumquat:\s*42330", text)) == 1
    assert len(re.findall(r"Lemon:\s*10", text)) == 1
    assert len(re.findall(r"Mango:\s*85", text)) == 1

    assert len(re.findall(r"Nectarine:\s*170", text)) == 1
    assert len(re.findall(r"Olives:\s*5", text)) == 1
    assert len(re.findall(r"Papaya:\s*23205", text)) == 1
    assert len(re.findall(r"Quince:\s*5", text)) == 1


@pytest.mark.parametrize(
    "struct, data", [
        [[
            ["struct0", [[
                        ("Apples",          4),
                        ("Bananas",         4),
                        ("Carrots",         8),
                        ("Durian",          16),
                    ]]
             ],
            ["RSVD", [[
                        ("RSVD",    32)
                    ]]
             ],
            ["struct2", [[
                        ("Jackfruit",       4),
                        ("Kumquat",         16),
                        ("Lemon",           4),
                        ("Mango",           8)
                    ]]
             ],
            ["RSVD", [[
                        ("RSVD",    32)
                    ]]
             ],
        ], CHECKERBOARD_BITS],
    ]
)
def test_slot_format_parse_values_excludes_RSVD_fields(struct, data):
    slot_format = FlitParser(struct)
    slot_format.from_buffer(data)

    text = str(slot_format)

    assert len(re.findall(r"Apples:\s*10", text)) == 1
    assert len(re.findall(r"Bananas:\s*10", text)) == 1
    assert len(re.findall(r"Carrots:\s*85", text)) == 1
    assert len(re.findall(r"Durian:\s*43605", text)) == 1

    assert len(re.findall(r"Jackfruit:\s*10", text)) == 1
    assert len(re.findall(r"Kumquat:\s*42330", text)) == 1
    assert len(re.findall(r"Lemon:\s*10", text)) == 1
    assert len(re.findall(r"Mango:\s*85", text)) == 1

    # RSVD not printed
    assert "RSVD" not in text

    # RSVD is still addressible
    assert len(slot_format.RSVD) == 2
    assert slot_format.RSVD[0].RSVD == 2857740885
    assert slot_format.RSVD[1].RSVD == 2857740885


@pytest.mark.parametrize(
    "struct, data", [
        [[
            ["struct0", [[
                        ("Apples",          4),
                        ("Bananas",         4),
                        ("Carrots",         8),
                        ("Durian",          16),
                    ]]
             ],
            ["struct1", [[
                        ("Elderberries",    16),
                        ("Fig",             8),
                        ("Grapefruit",      4),
                        ("Honeydew",        4)
                    ]]
             ],
            ["struct2", [[
                        ("Jackfruit",       4),
                        ("Kumquat",         16),
                        ("Lemon",           4),
                        ("Mango",           8)
                    ]]
             ],
            ["struct3", [[
                        ("Nectarine",       8),
                        ("Olives",          4),
                        ("Papaya",          16),
                        ("Quince",          4)
                    ]]
             ],
        ], CHECKERBOARD_BITS],
    ]
)
def test_slot_format_converts_to_int(struct, data):
    slot_format = FlitParser(struct)
    slot_format.from_buffer(data)

    data_as_int = int(data.hex(), 16)

    assert int(slot_format) == data_as_int
    assert hex(slot_format) == hex(data_as_int)
    assert bytes(slot_format) == data


@pytest.mark.parametrize(
    "struct", [
        [
            ["struct0", [[
                        ("Apples",          4),
                        ("Bananas",         4),
                        ("Carrots",         8),
                        ("Durian",          16),
                    ]]
             ],
            ["struct1", [[
                        ("Elderberries",    16),
                        ("Fig",             8),
                        ("Grapefruit",      4),
                        ("Honeydew",        4)
                    ]]
             ],
            ["struct2", [[
                        ("Jackfruit",       4),
                        ("Kumquat",         16),
                        ("Lemon",           4),
                        ("Mango",           8)
                    ]]
             ],
            ["struct3", [[
                        ("Nectarine",       8),
                        ("Olives",          4),
                        ("Papaya",          16),
                        ("Quince",          4)
                    ]]
             ],
        ],
    ]
)
def test_flitparser_can_output_from_valid_assignment(struct):
    slot_format = FlitParser(struct)

    slot_format.struct0[0].Apples        = 0
    slot_format.struct0[0].Bananas       = 1
    slot_format.struct0[0].Carrots       = 2
    slot_format.struct0[0].Durian        = 3

    slot_format.struct1[0].Elderberries  = 4
    slot_format.struct1[0].Fig           = 5
    slot_format.struct1[0].Grapefruit    = 6
    slot_format.struct1[0].Honeydew      = 7

    slot_format.struct2[0].Jackfruit     = 8
    slot_format.struct2[0].Kumquat       = 9
    slot_format.struct2[0].Lemon         = 10
    slot_format.struct2[0].Mango         = 11

    slot_format.struct3[0].Nectarine     = 12
    slot_format.struct3[0].Olives        = 13
    slot_format.struct3[0].Papaya        = 14
    slot_format.struct3[0].Quince        = 15

    expected_bin  = '0000'              # apples
    expected_bin += '0001'              # bananas
    expected_bin += '00000010'          # carrots
    expected_bin += '0000000000000011'  # durians

    expected_bin += '0000000000000100'  # elderberries
    expected_bin += '00000101'          # fig
    expected_bin += '0110'              # grapefruit
    expected_bin += '0111'              # honeydew

    expected_bin += '1000'              # jackfruit
    expected_bin += '0000000000001001'  # kumquat
    expected_bin += '1010'              # lemon
    expected_bin += '00001011'          # mango

    expected_bin += '00001100'          # nectarine
    expected_bin += '1101'              # olives
    expected_bin += '0000000000001110'  # papaya
    expected_bin += '1111'              # quince

    assert slot_format.__bin__() == expected_bin


@pytest.mark.parametrize(
    "struct", [
        [
            ["struct0", [[
                        ("Apples",          4),
                        ("Bananas",         4),
                        ("Carrots",         8),
                        ("Durian",          16),
                    ]]
             ],
            ["struct1", [[
                        ("Elderberries",    16),
                        ("Fig",             8),
                        ("Grapefruit",      4),
                        ("Honeydew",        4)
                    ]]
             ],
            ["struct2", [[
                        ("Jackfruit",       4),
                        ("Kumquat",         16),
                        ("Lemon",           4),
                        ("Mango",           8)
                    ]]
             ],
            ["struct3", [[
                        ("Nectarine",       8),
                        ("Olives",          4),
                        ("Papaya",          16),
                        ("Quince",          4)
                    ]]
             ],
        ],
    ]
)
def test_flitparser_raises_valueerror_on_invalid_assignment(struct):
    slot_format = FlitParser(struct)

    slot_format.struct0[0].Apples = 100

    try:
        slot_format.__bin__()
        assert False
    except ValueError:
        assert True
    except Exception:
        assert False
