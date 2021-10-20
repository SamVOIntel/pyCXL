# External Dependencies
import pytest

# Package imports
from tests.test_utils import (
    CHECKERBOARD_BYTES,
    CHECKERBOARD_BITS,
    EIGHT_BIT_STRUCT,
    TEN_BIT_STRUCT,
    FIFTEEN_BIT_STRUCT,
    TWENTY_BIT_STRUCT,
    THIRTY_BIT_STRUCT,
    FORTY_BIT_STRUCT
)
from pyCXL.structs.bitcollections import BitCollection

# ============================= BitCollection Tests =============================
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
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
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
                FORTY_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ], 128
        ),
        (
            [
                FIFTEEN_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
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
def test_BitCollection_constructor_calculates_size(bitstructs, expected):
    testBitStruct = BitCollection(bitstructs=bitstructs, name="TEST COLLECTION")
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
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
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
                FORTY_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ]
        ),
        (
            [
                FIFTEEN_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
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
def test_BitCollection_properties_throw_on_reassingment(bitstructs):
    testBitStruct = BitCollection(bitstructs=bitstructs, name="TEST COLLECTION")
    # each assignment should throw
    try:
        testBitStruct.structs = 9
        assert False
    except AttributeError:
        assert True
    try:
        testBitStruct.name = "Jolly good show!"
        assert False
    except AttributeError:
        assert True
    try:
        testBitStruct.size = b"\x06"
        assert False
    except AttributeError:
        assert True
    try:
        testBitStruct.idx = set()
        assert False
    except AttributeError:
        assert True


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
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
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
                FORTY_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ], 6
        ),
        (
            [
                FIFTEEN_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
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
def test_BitCollection_iterates(bitstructs, expected):
    test_BitCollection = BitCollection(bitstructs=bitstructs, name="TEST Collection")
    iterations = 0
    for iteration in test_BitCollection:
        iterations += 1
    assert iterations == expected


@pytest.mark.parametrize(
    "bitstructs, bindata, expected", [
        (
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
            ], CHECKERBOARD_BITS,
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
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
            ], CHECKERBOARD_BITS,
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
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
            ], bin(255),
            False
        )
    ]
)
def test_BitCollection_from_binary_valid_assignment(bitstructs, bindata, expected):
    testBitCollection = BitCollection(bitstructs=bitstructs, name="TEST COLLECTION")
    try:
        testBitCollection.from_bin(bindata)
        assert_idx = 0
        for struct in testBitCollection:
            for field in struct:
                assert field.value == expected[assert_idx]
                assert_idx += 1
    except ValueError as err:
        assert str(err) == "Not enough bins to fill the BitCollection"


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
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
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
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
            ], bytearray(b"\xFF"),
            False
        )
    ]
)
def test_BitCollection_from_bytes_valid_assignment(bitstructs, bytedata, expected):
    testBitCollection = BitCollection(bitstructs=bitstructs, name="TEST COLLECTION")
    try:
        testBitCollection.from_bytes(bytedata)
        assert_idx = 0
        for struct in testBitCollection:
            for field in struct:
                assert field.value == expected[assert_idx]
                assert_idx += 1
    except ValueError as err:
        assert str(err) == "Not enough bytes to fill the BitCollection"


@pytest.mark.parametrize(
    "bitstructs, test_data, expected_int, expected_hex", [
        (
            # small
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
            ],
            CHECKERBOARD_BYTES,
            174422,
            "0x2a956"
        ),
        (
            # byte aligned
            [
                EIGHT_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                EIGHT_BIT_STRUCT()
            ],
            CHECKERBOARD_BYTES,
            47944936110839210,
            "0xaa55aa55aa55aa"
        ),
        (
            # HUGE
            [
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ],
            CHECKERBOARD_BYTES,
            863699185612310821477349097564821,
            "0x2a956a956a956a956a956a956a95"
        )
    ]
)
def test_BitCollection_converts_to_int_hex(bitstructs, test_data, expected_int, expected_hex):
    test_collection = BitCollection(bitstructs=bitstructs, name="TEST")
    # initialized should be 0
    assert int(test_collection) == 0
    assert hex(test_collection) == "0x0"

    test_collection.from_bytes(test_data)
    assert int(test_collection) == expected_int
    assert hex(test_collection) == expected_hex


@pytest.mark.parametrize(
    "bitstructs, test_data, expected_bytes", [
        (
            # small
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
            ],
            CHECKERBOARD_BYTES,
            b"\x02\xA9\x56"
        ),
        (
            # byte aligned
            [
                EIGHT_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                EIGHT_BIT_STRUCT()
            ],
            CHECKERBOARD_BYTES,
            b"\xAA\x55\xAA\x55\xAA\x55\xAA"
        ),
        (
            # HUGE
            [
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ],
            CHECKERBOARD_BYTES,
            b"\x2A\x95\x6A\x95\x6A\x95\x6A\x95\x6A\x95\x6A\x95\x6A\x95"
        )
    ]
)
def test_BitCollection_converts_to_bytes(bitstructs, test_data, expected_bytes):
    test_collection = BitCollection(bitstructs=bitstructs, name="TEST")
    # initialized should be 0
    assert bytes(test_collection) == b"\x00" * (len(expected_bytes))

    test_collection.from_bytes(test_data)
    assert bytes(test_collection) == expected_bytes


@pytest.mark.parametrize(
    "bitstructs, test_data, expected_str", [
        (
            # small
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
            ],
            CHECKERBOARD_BYTES,
            (
                # 8 bit
                2, 1, 10,
                # 10 bit
                2, 10, 6
            ),
        ),
        (
            # byte aligned
            [
                EIGHT_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                EIGHT_BIT_STRUCT()
            ],
            CHECKERBOARD_BYTES,
            (
                # 8 bit
                2, 1, 10,
                # 40 bit
                42, 6821, 11602, 21,
                # 8 bit
                2, 1, 10
            ),
        ),
        (
            # HUGE
            [
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ],
            CHECKERBOARD_BYTES,
            (
                # 40 bit
                85, 1370, 21165, 10,
                # 40 bit
                42, 6821, 11602, 21,
                # 30 bit
                10901, 13, 661
            ),
        )
    ]
)
def test_BitCollection_converts_to_str(bitstructs, test_data, expected_str):
    test_collection = BitCollection(bitstructs=bitstructs, name="TEST COLLECTION")
    empty_str = str(test_collection)
    assert f"{test_collection.name}:\n" in empty_str
    for struct in test_collection:
        print_width = max([len(field.name) for field in struct])
        for field in struct:
            padding = " " * (print_width - len(field.name) + 4)
            # initialized should be 0
            assert f"\t\t{field.name}:{padding}0\n" in empty_str

    test_collection.from_bytes(test_data)
    filled_str = str(test_collection)
    assert f"{test_collection.name}:\n" in filled_str
    for struct in test_collection:
        print_width = max([len(field.name) for field in struct])
        for field in struct:
            padding = " " * (print_width - len(field.name) + 4)
            # with data should now be expected number
            assert f"\t\t{field.name}:{padding}{field.value}\n" in filled_str


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
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
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
def test_BitCollection_to_dict(bitstructs, bytedata, expected):
    # test collection should be initialized as all zeros
    testBitCollection = BitCollection(bitstructs=bitstructs, name="TEST")
    # make dictionary
    testDict = testBitCollection.to_dict()

    # the dictionary is keyed with the name
    assert testBitCollection.name in testDict
    # each struct is represented in the dictionary (no overwrites)
    assert len(testBitCollection) == len(testDict[testBitCollection.name])
    # order is preserved
    for i in range(len(testBitCollection)):
        assert testBitCollection[i].name in testDict[testBitCollection.name][i]
        # each field has the expected value (which should be 0)
        for field in testBitCollection[i]:
            assert field.value == 0 == testDict[testBitCollection.name][i][testBitCollection[i].name][field.name]

    # fill BitStructionCollection with actual data
    testBitCollection.from_bytes(bytedata)
    # remake dictionary
    testDict = testBitCollection.to_dict()

    # the dictionary is keyed with the name
    assert testBitCollection.name in testDict
    # each struct is represented in the dictionary (no overwrites)
    assert len(testBitCollection) == len(testDict[testBitCollection.name])
    # order is preserved
    for i in range(len(testBitCollection)):
        assert testBitCollection[i].name in testDict[testBitCollection.name][i]
        # each field has the expected value
        for field in testBitCollection[i]:
            assert field.value == testDict[testBitCollection.name][i][testBitCollection[i].name][
                field.name]