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

# used as the struct name
FLIT_HEAD       = "Flit_Header"

H2D_REQ         = "H2D_Request"
H2D_RESP        = "H2D_Response"
H2D_HEAD        = "H2D_Data_Header"

M2S_RWD_HEAD    = "M2S_RwD_Header"
M2S_RWD_REQ     = "M2S_RwD_Request"

D2H_REQ         = "D2H_Request"
D2H_RESP        = "D2H_Response"
D2H_HEAD        = "D2H_Data_Header"

S2M_NDR         = "S2M_NDR"
S2M_DRS         = "S2M_DRS"

DEVLOAD         = "Devload"


# todo the flit header has a different order in the definition from the examples
# light blue/purple in the spec
def flit_header_fields():
    return [
        ("Type",            1),
        ("RV",              1),
        ("Ak",              1),
        ("ByteEnabled",     1),
        ("Size",            1),
        ("Slot0",           3),
        ("Slot1",           3),
        ("Slot2",           3),
        ("Slot3",           3),
        ("RSVD",            3),
        ("ResponseCredit",  8),
        ("DataCredit",      4),
    ]


# red in the spec
def H2D_request_fields():
    return [
        ("Valid",           1),
        ("Opcode",          3),
        ("Address",        46),
        ("UQUID",          12),
        ("rsvd_62_63",      2),
    ]


# orange in the spec
def H2D_response_fields():
    return [
        ("Valid",          1),
        ("Opcode",         4),
        ("RspData",       12),
        ("RSP_PRE",        2),
        ("CQID",          12),
        ("rsvd_31",        1),
    ]


# light pink in the spec
def H2D_data_header_fields():
    return [
        ("Valid",           1),
        ("CQID",           12),
        ("ChunkValid",      1),
        ("Poison",          1),
        ("GO_Err",          1),
        ("rsvd_16_23",      8),
    ]


# light yellow in spec w/o poison field: 1 bit too small for byte alignment
def M2S_request_fields():
    return [
        ("Valid",         1),
        ("MemOp",         4),
        ("SnpType",       3),
        ("MetaField",     2),
        ("MetaValue",     2),
        ("Tag",          16),
        ("Addr",         47),
        ("TC",            2),
        ("LD_ID",         4),
        ("rsvd_81_86",    6),
    ]


# light yellow in spec w/ poison field: 1 bit too small for byte alignment
def M2S_RwD_header_fields():
    return [
        ("Valid",           1),
        ("MemOp",           4),
        ("SnpType",         3),
        ("MetaField",       2),
        ("MetaValue",       2),
        ("Tag",            16),
        ("Addr",           46),
        ("Poison",          1),
        ("TC",              2),
        ("LD_ID",           4),
        ("rsvd_81_86",      6),
    ]


# red in the spec
def D2H_request_fields():
    return [
        ("Valid",               1),
        ("OpCode",              5),
        ("CommandQueueID",     12),
        ("NonTemporal",         1),
        ("RSVD_0",              7),
        ("Address",            46),
        ("RSVD_1",              7)
    ]


# green in the spec
def D2H_response_fields():
    return [
        ("Valid",           1),
        ("OpCode",          5),
        ("UniqueQueueID",  12),
        ("RSVD",            2)
    ]


# orange in the spec
def D2H_data_header_fields():
    return [
        ("Valid",           1),
        ("UniqueQueueID",  12),
        ("ChunkValid",      1),
        ("Bogus",           1),
        ("Poison",          1),
        ("RSVD",            1)
    ]


# caucasian flesh tone in the spec
def S2M_NDR_fields():
    return [
        ("Valid",           1),
        ("MemOp",           3),
        ("MetaField",       2),
        ("MetaValue",       2),
        ("Tag",            16),
        ("LogicalDeviceID", 4),
        ("DevLoad",         2)
    ]


# red checkered color in spec because fields are split
def S2M_NDR_fields_minus_devload():
    return [
        ("Valid",           1),
        ("MemOp",           3),
        ("MetaField",       2),
        ("MetaValue",       2),
        ("Tag",             16),
        ("LogicalDeviceID", 4),
    ]


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
