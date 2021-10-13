# Package Imports
from src.structs.flitsubstructures import (
    # field structures
    LLCRD_flit_header_fields,
    RETRY_flit_header_fields,
    RETRY_REQ_LLCRTL_fields,
    RETRY_ACK_LLCRTL_fields,
    IDE_flit_header_fields,

    # constants
    FLIT_HEAD
)

Link_Layer_Control_RSVD_Payload = [
    ["Payload",         [[("Bytes",                 8)]] * 8]
]

LLCRD_Link_Layer_Control = [
    [FLIT_HEAD,         [LLCRD_flit_header_fields()]],
    ["LLCTRL",          [[("LLCTRL",                4)]]],
    ["SubType",         [[("SubType",               4)]]],
    ["RSVD_ZEROS",      [[("RSVD_ZEROS",            24)]]],
]

LLCRD_Link_Layer_Control_ACK_Payload = [
    ["Acknowledge",     [[("Acknowledge",           3)]]],
    ["RSVD",            [[("RSVD",                  1)]]],
    ["Acknowledge",     [[("Acknowledge",           4)]]],
    ["RSVD",            [[("RSVD",                  56)]]],
]

RETRY_Link_Layer_Control = [
    [FLIT_HEAD,         [RETRY_flit_header_fields()]],
    ["LLCTRL",          [[("LLCTRL",                4)]]],
    ["SubType",         [[("SubType",               4)]]],
    ["RSVD_ZEROS",      [[("RSVD_ZEROS",            24)]]],
]

RETRY_Request_Link_Layer_Control_Payload = [
    ["Payload",         [RETRY_REQ_LLCRTL_fields()]]
]

RETRY_ACK_Link_Layer_Control_Payload = [
    ["Payload",         [RETRY_ACK_LLCRTL_fields()]]
]

IDE_Link_Layer_Control = [
    [FLIT_HEAD,         [IDE_flit_header_fields()]],
    ["Payload",         [[("Bytes",             8)]]],
    ["LLCTRL",          [[("LLCTRL",            4)]]],
    ["SubType",         [[("SubType",           4)]]],
]

IDE_RSVD_Link_Layer_Control_Payload = [
    ["Payload",         [[("Bytes",             8)]] * 11]
]