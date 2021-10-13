# Package Imports
from src.structs.flitsubstructures import (
    flit_header_fields,
    D2H_request_fields,
    D2H_response_fields,
    D2H_data_header_fields,
    S2M_NDR_fields,
    S2M_DRS_fields,
    S2M_NDR_fields_minus_devload,
    S2M_NDR_devload_array_fields,

    # Constants
    FLIT_HEAD,
    D2H_REQ,
    D2H_RESP,
    D2H_HEAD,
    S2M_NDR,
    S2M_DRS,
    DEVLOAD
)

H0_slot_format = [
    [FLIT_HEAD,     [flit_header_fields()]],
    [D2H_HEAD,      [D2H_data_header_fields()]],
    [D2H_RESP,      [D2H_response_fields()] * 2],
    [S2M_NDR,       [S2M_NDR_fields()]],
    ["RSVD",        [[("RSVD",      9)]]]
]


H1_slot_format = [
    [FLIT_HEAD,     [flit_header_fields()]],
    [D2H_REQ,       [D2H_request_fields()]],
    [D2H_HEAD,      [D2H_data_header_fields()]],
]

H2_slot_format = [
    [FLIT_HEAD,     [flit_header_fields()]],
    [D2H_HEAD,      [D2H_data_header_fields()] * 4],
    [D2H_RESP,      [D2H_response_fields()]],
    ["RSVD",        [[("RSVD",         8)]]]
]

H3_slot_format = [
    [FLIT_HEAD,     [flit_header_fields()]],
    [S2M_DRS,       [S2M_DRS_fields()]],
    [S2M_NDR,       [S2M_NDR_fields()]],
    ["RSVD",        [[("RSVD",      26)]]]
]

H4_slot_format = [
    [FLIT_HEAD,     [flit_header_fields()]],
    [S2M_NDR,       [S2M_NDR_fields_minus_devload()] * 2],
    [DEVLOAD,       [S2M_NDR_devload_array_fields()] * 2],
    ["RSVD",        [[("RSVD",          36)]]]
]

H5_slot_format = [
    [FLIT_HEAD,     [flit_header_fields()]],
    [S2M_DRS,       [S2M_DRS_fields()] * 2],
    ["RSVD",        [[("RSVD",        16)]]]
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
    [D2H_REQ,       [D2H_request_fields()]],
    [D2H_RESP,      [D2H_response_fields()] * 2],
    ["RSVD",        [[("RSVD",          9)]]],
]

G2_slot_format = [
    [D2H_REQ,       [D2H_request_fields()]],
    [D2H_HEAD,      [D2H_data_header_fields()]],
    [D2H_RESP,      [D2H_response_fields()]],
    ["RSVD",        [[("RSVD",          12)]]],
]

G3_slot_format = [
    [D2H_HEAD,      [D2H_data_header_fields()] * 4],
    ["RSVD",        [[("RSVD",          60)]]],
]

G4_slot_format = [
    [S2M_DRS,       [S2M_DRS_fields()]],
    [S2M_NDR,       [S2M_NDR_fields_minus_devload()] * 2],
    [DEVLOAD,       [S2M_NDR_devload_array_fields()] * 2],
    ["RSVD",        [[("RSVD",          28)]]],
]

G5_slot_format = [
    [S2M_NDR,       [S2M_NDR_fields_minus_devload()] * 2],
    [DEVLOAD,       [S2M_NDR_devload_array_fields()] * 2],
    ["RSVD",        [[("RSVD",          68)]]],
]

G6_slot_format = [
    [S2M_DRS,       [S2M_DRS_fields()] * 3],
    ["RSVD",        [[("RSVD",          8)]]],
]
