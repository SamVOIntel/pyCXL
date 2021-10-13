# Package imports
from src.structs.bitfields import BitField
from src.structs.bitstructs import BitStruct


CHECKERBOARD_BYTES = bytearray(b"\xAA\x55" * 8)
CHECKERBOARD_BITS = "0b" + "1010101001010101" * 8
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
                BitField(size=4, name="Apple"),
                BitField(size=4, name="Banana"),
                BitField(size=8, name="Carrot"),
                BitField(size=16, name="Durian")
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


class INCLUDES_RSVD_STRUCT(BitStruct):

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=4, name="Mango"),
                BitField(size=4, name="Nectarine", rsvd=True),
                BitField(size=8, name="Olive"),
                BitField(size=16, name="Papaya", rsvd=True)
            ],
            name="Includes Rsvd BitFields"
        )


class INCLUDES_ENUMS_STRUCT(BitStruct):

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=4, name="Quince", enums={10: "Ten"}),
                BitField(size=4, name="Raspberry", enums={20: "Twenty"}),
                BitField(size=8, name="Strawberry", enums={170: "Hundred and seventy"}),
                BitField(size=16, name="Tomato", enums={0: "Zero"})
            ],
            name="Includes Enums BitFields"
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