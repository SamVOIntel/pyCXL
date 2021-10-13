# Package Imports
from src.structs.flitsubstructures import (
    flit_header_fields,
    H2D_request_fields,
    H2D_response_fields,
    H2D_data_header_fields,
    M2S_RwD_header_fields,
    M2S_request_fields,

    # Constants
    FLIT_HEAD,
    H2D_REQ,
    H2D_RESP,
    H2D_HEAD,
    M2S_RWD_HEAD,
    M2S_RWD_REQ,
)


H0_slot_format = [
    [FLIT_HEAD, [flit_header_fields()]],
    [H2D_REQ,   [H2D_request_fields()]],
    [H2D_RESP,  [H2D_response_fields()]]
]


H1_slot_format = [
    [FLIT_HEAD, [flit_header_fields()]],
    [H2D_HEAD,  [H2D_data_header_fields()]],
    [H2D_RESP,  [H2D_response_fields()] * 2],
    ["RSVD",    [[("RSVD",          8)]]],
]


H2_slot_format = [
    [FLIT_HEAD, [flit_header_fields()]],
    [H2D_REQ,   [H2D_request_fields()]],
    [H2D_HEAD,  [H2D_data_header_fields()]],
    ["RSVD",    [[("RSVD",          8)]]],
]


H3_slot_format = [
    [FLIT_HEAD, [flit_header_fields()]],
    [H2D_HEAD,  [H2D_data_header_fields()] * 4],
]


H4_slot_format = [
    [FLIT_HEAD,     [flit_header_fields()]],
    [M2S_RWD_HEAD,  [M2S_RwD_header_fields()]],
    ["RSVD",    [[("RSVD",          9)]]],
]


H5_slot_format = [
    [FLIT_HEAD,     [flit_header_fields()]],
    [M2S_RWD_REQ,   [M2S_request_fields()]],
    ["RSVD",    [[("RSVD",          9)]]],
]

H6_slot_format = [
    [FLIT_HEAD,     [flit_header_fields()]],
    ["MAC",         [[("MAC",          96)]]]
]

G0_Data_slot_format = [
    ["DATA",        [[("DATA",        128)]]]
]

G0_Byte_Enable_slot_format = [
    ["ByteEnable",  [[("ByteEnable",    64)]]],
    ["RSVD",        [[("RSVD",          64)]]],
]

G1_slot_format = [
    [H2D_RESP,      [(H2D_response_fields())] * 4]
]

G2_slot_format = [
    [H2D_REQ,       [H2D_request_fields()]],
    [H2D_HEAD,      [H2D_data_header_fields()]],
    [H2D_RESP,      [H2D_response_fields()]],
    ["RSVD",        [[("RSVD",          8)]]],
]

G3_slot_format = [
    [H2D_HEAD,      [H2D_data_header_fields()] * 4],
    [H2D_RESP,      [H2D_response_fields()]],
]

G4_slot_format = [
    [M2S_RWD_REQ,   [M2S_request_fields()]],
    ["RSVD",        [[("RSVD",          1)]]],
    [H2D_HEAD,      [H2D_data_header_fields()]],
    ["RSVD",        [[("RSVD",          16)]]],
]

G5_slot_format = [
    [M2S_RWD_HEAD,  [M2S_RwD_header_fields()]],
    ["RSVD",        [[("RSVD",          1)]]],
    [H2D_RESP,      [H2D_response_fields()]],
    ["RSVD",        [[("RSVD",          8)]]],
]
