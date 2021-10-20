"""
This file contains slot format 'substructs' which are common to the 16 byte slot format objects.
These substructs are not byte aligned and therefore CANNOT be defined as ctypes Structures. They
are instead defined as lists of ctypes fields which are later combined into ctypes structures.

All fields of all slot format substructs must be c_uint64.

From CXL 2.0:

    Drive to Host (D2H) Request carries new requests from the Device to the Host. The requests
    typically target memory. Each request will receive zero, one or two responses and at most one
    64-byte cacheline of data. The channel may be back pressured without issue. D2H
    Response carries all responses from the Device to the Host. Device responses to snoops
    indicate the state the line was left in the device caches, and may indicate that data is
    being returned to the Host to the provided data buffer. They may still be blocked
    temporarily for link layer credits, but should not require any other transaction to
    complete to free the credits. D2H Data carries all data and byte-enables from the
    Device to the Host. The data transfers can result either from implicit (as a result of
    snoop) or explicit write-backs (as a result of cache capacity eviction). In all cases a full
    64-byte cacheline of data will be transferred. D2H Data transfers must make progress
    or deadlocks may occur. They may be blocked temporarily for link layer credits, but
    must not require any other transaction to complete to free the credits.
"""
from bitstructs import (
    BitField,
    BitStruct
)
# used as the struct name
FLIT_HEAD       = "Flit Header"

H2D_REQ         = "H2D Request"
H2D_RESP        = "H2D Response"
H2D_HEAD        = "H2D Data_Header"

M2S_HEAD        = "M2S Header"
M2S_REQ         = "M2S Request"

D2H_REQ         = "D2H_Request"
D2H_RESP        = "D2H_Response"
D2H_HEAD        = "D2H_Data_Header"

S2M_NDR         = "S2M_NDR"
S2M_DRS         = "S2M_DRS"

DEVLOAD         = "Devload"


# ============================== Meta Fields ==============================
class FlitType(BitField):

    def __init__(self):
        super().__init__(
            size=1, name="Type", enums={
                0: "Protocol",
                1: "Control"
            }
        )


class RsvdField(BitField):
    """
    Rsvd fields of a given size
    """

    def __init__(self, size:int):
        super().__init__(
            size=size, name="Rsvd", rsvd=True
        )


class ChunkValid(BitField):

    def __init__(self):
        super().__init__(
            size=1,
            name="Chunk Valid",
            enums={
                0: "Lower 32B",
                1: "Upper 32B"
            }
        )


class Poison(BitField):

    def __init__(self):
        super().__init__(
            size=1,
            name="Poison",
            enums={
                    1: "Data is corrupted"
                }
        )


class LogicalDeviceIdentifier(BitField):

    def __init__(self):
        super().__init__(size=4, name="Logical Device Identifier")


# ============================== Flitsubstructures ==============================
class FlitHeader(BitStruct):
    # light blue/purple in the spec

    def __init__(self):
        super().__init__(
            bitfields=[
                FlitType(),
                RsvdField(size=1),
                BitField(size=1, name="Acknowledge"),
                BitField(size=1, name="Byte Enabled"),
                BitField(size=1, name="Size"),
                BitField(size=3, name="Slot 0"),
                BitField(size=3, name="Slot 1"),
                BitField(size=3, name="Slot 2"),
                BitField(size=3, name="Slot 3"),
                RsvdField(size=1),
                BitField(size=8, name="Response Credit"),
                BitField(size=4, name="Data Credit")
            ],
            name=FLIT_HEAD
        )


class H2DRequest(BitStruct):
    # red in the spec

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=1,    name="Valid"),
                BitField(size=3,    name="OpCode"),
                BitField(size=46,   name="Address"),
                RsvdField(size=1)
            ],
            name=H2D_REQ
        )


class H2DResponse(BitStruct):
    # orange in the spec

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=1,    name="Valid"),
                BitField(size=4,    name="OpCode"),
                BitField(size=12,   name="Response Data"),
                BitField(size=1,    name="RSP_PRE", enums={
                    0: "Host Cache Miss to Local CPU socket memory",
                    1: "Host Cache Hit",
                    2: "Host Cache Miss to Remote CPU socket memory",
                }),
                BitField(size=12,   name="Command Queue ID")
            ],
            name=H2D_RESP
        )


class H2DDataHeader(BitStruct):
    # light pink in the spec

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=1,    name="Valid"),
                BitField(size=12,   name="Command Queue ID"),
                ChunkValid(),
                Poison(),
                BitField(size=1,    name="GO-Err", enums={
                    1: "Data is result of an error condition"
                }),
                RsvdField(size=8)
            ],
            name=H2D_HEAD
        )


class M2SRequest(BitStruct):
    # light yellow in spec w/o poison field: 1 bit too small for byte alignment

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=1,    name="Valid"),
                BitField(size=4,    name="MemOpcode"),
                BitField(size=3,    name="Snoop Type"),
                BitField(size=2,    name="MetaField"),
                BitField(size=2,    name="MetaValue"),
                BitField(size=16,   name="Tag"),
                BitField(size=47,   name="Address"),
                BitField(size=2,    name="Traffic Class"),
                LogicalDeviceIdentifier(),
                RsvdField(size=6)
            ],
            name=M2S_REQ
        )


class M2SHeader(BitStruct):
    # light yellow in spec w/ poison field: 1 bit too small for byte alignment

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=1,    name="Valid"),
                BitField(size=4,    name="MemOpcode"),
                BitField(size=3,    name="Snoop Type"),
                BitField(size=2,    name="MetaField"),
                BitField(size=2,    name="MetaValue"),
                BitField(size=16,   name="Tag"),
                BitField(size=46,   name="Address"),
                Poison(),
                BitField(size=2,    name="Traffic Class"),
                LogicalDeviceIdentifier(),
                RsvdField(size=6)
            ],
            name=M2S_HEAD
        )


class D2HRequest(BitStruct):
    # red in the spec

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=1,    name="Valid"),
                BitField(size=5,    name="Opcode"),
                BitField(size=12,   name="Command Queue ID"),
                BitField(size=1,    name="NonTemporal"),
                RsvdField(size=7),
                BitField(size=46,   name="Address"),
                RsvdField(size=7)
            ],
            name=D2H_REQ
        )


class D2HResponse(BitStruct):
    # green in the spec

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=1,    name="Valid"),
                BitField(size=5,    name="Opcode"),
                BitField(size=12,   name="Unique Queue ID"),
                RsvdField(size=2)
            ],
            name=D2H_RESP
        )


class D2HHeader(BitStruct):
    # orange in the spec

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=1,    name="Valid"),
                BitField(size=12,   name="Unique Queue ID"),
                ChunkValid(),
                BitField(size=1,    name="Bogus"),
                Poison(),
                RsvdField(size=1)
            ],
            name=D2H_HEAD
        )


class S2MNDR(BitStruct):
    # caucasian flesh tone in the spec

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=1,    name="Valid"),
                BitField(size=3,    name="MemOpcode"),
                BitField(size=2,    name="MetaField"),
                BitField(size=2,    name="MetaValue"),
                BitField(size=16,   name="Tag"),
                LogicalDeviceIdentifier(),
                BitField(size=2,    name="Devload")
            ],
            name=S2M_NDR
        )


class S2MNDR_MinusDevload(BitStruct):
    # red checkered color in spec because fields are split

    def __init__(self):
        super().__init__(
            bitfields=[
                BitField(size=1,    name="Valid"),
                BitField(size=3,    name="MemOpcode"),
                BitField(size=2,    name="MetaField"),
                BitField(size=2,    name="MetaValue"),
                BitField(size=16,   name="Tag"),
                LogicalDeviceIdentifier()
            ],
            name=S2M_NDR
        )


def S2M_NDR_devload_array_fields():
    return [
        ("Devload",         2)
    ]


# yellow in the spec
def S2M_DRS_fields():
    return [
        ("Valid",           1),
        ("MemOp",           3),
        ("MetaField",       2),
        ("MetaValue",       2),
        ("Tag",            16),
        ("Poison",          1),
        ("LogicalDeviceID", 4),
        ("DevLoad",         2),
        ("RSVD",            9)
    ]


# light blue in spec
def LLCRD_flit_header_fields():
    return [
        ("Type",            1),
        ("RSVD_0",          1),
        ("Acknowledge",     1),
        ("RSVD_1",          2),
        ("ControlFormat",   3),
        ("RSVD_2",          12),
        ("ResponseCredit",  4),
        ("RequestCredit",   4),
        ("DataCredit",      4)
    ]


# light blue in spec
def RETRY_flit_header_fields():
    return [
        ("Type",            1),
        ("RSVD_0",          4),
        ("ControlFormat",   3),
        ("RSVD_2",          24),
    ]


def RETRY_REQ_LLCRTL_fields():
    return [
        ("SequenceNumber",  8),
        ("RSVD_0",          8),
        ("Retry",           5),
        ("PhyReinit",       5),
        ("RSVD_1",          38)
    ]


def RETRY_ACK_LLCRTL_fields():
    return [
        ("Empty",           1),
        ("Viral",           1),
        ("RSVD_0",          1),
        ("Retry",           5),
        ("WrPtr",           8),
        ("SequenceNumber",  8),
        ("NumFreeBuf",      8),
        ("LDID",            16),
        ("RSVD_1",          16)
    ]


def IDE_flit_header_fields():
    return [
        ("Type",            1),
        ("RSVD_0",          4),
        ("ControlFormat",   3),
        ("RSVD_2",          16),
    ]


def LLCRTL_SubType_fields():
    return [
        ("LLCTRL",          4),
        ("SubType",         4)
    ]
