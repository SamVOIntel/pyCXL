import pytest

from pyCXL.structs.bitfields import BitField
from pyCXL.structs.bitstructs import BitStruct, LittleEndianBitStruct, BigEndianBitStruct
from test_utils import (
    CHECKERBOARD_BYTES,
    CHECKERBOARD_BITS
)


class Length(BitField):

    def __init__(self):
        super().__init__(size=10, name="Length")


class AT(BitField):

    def __init__(self):
        super().__init__(size=2, name="AT")


class Attribute(BitField):

    def __init__(self):
        super().__init__(size=2, name="Attribute")


class EP(BitField):

    def __init__(self):
        super().__init__(size=1, name="EP")


class TD(BitField):

    def __init__(self):
        super().__init__(size=1, name="TD")


class MCTP_BIG_END_TEST(BigEndianBitStruct):

    def __init__(self):
        super().__init__(
            bitfields=[
                Length(),
                AT(),
                Attribute(),
                EP(),
                TD()
            ],
            name="MCTP BIG ENDIAN TEST"
        )


test_obj = MCTP_BIG_END_TEST()

print(test_obj)
test_obj.from_bin(CHECKERBOARD_BITS)
print(test_obj)