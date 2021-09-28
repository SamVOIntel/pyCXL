from ctypes import (
    BigEndianStructure,
    c_uint8,
    c_uint16
)

MESSAGE_ROUTING = {
    0: "Route to Root Complex",
    2: "Route by ID",
    3: "Broadcast from Root Complex"
}


class pcie_medium_specific_header(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        # DWord[0]
        #   Byte[0]
        ("messageRouting",              c_uint8, 3),
        ("type",                        c_uint8, 2),
        ("format",                      c_uint8, 2),
        ("rsvd7",                       c_uint8, 1),

        #   Byte[1]
        ("TH",                          c_uint8, 1),
        ("rsvd1_2",                     c_uint8, 1),
        ("attr_2",                      c_uint8, 1),
        ("rsvd11",                      c_uint8, 1),
        ("trafficClass",                c_uint8, 3),
        ("rsvd8",                       c_uint8, 1),

        #   Byte[2:3]
        ("length",                      c_uint16, 10),
        ("addrType",                    c_uint16, 2),
        ("attr",                        c_uint16, 2),
        ("errorPresent",                c_uint16, 1),
        ("tlpDigest",                   c_uint16, 1),

        # DWord[1]
        #   Byte[0:1]
        ("requestor",                   c_uint16),

        #   Byte[2]
        ("messageCode",                 c_uint8),

        #   Byte[3]
        ("mctpVDMCode",                 c_uint8, 4),
        ("pad",                         c_uint8, 2),
        ("rsvd48_49",                   c_uint8, 2),

        # DWord[2]
        #   Byte[0:1]
        ("target",                      c_uint16),

        #   Byte[2:3]
        ("vendorID",                    c_uint16)
    ]


class mctp_transport_header(BigEndian_TWIDL_Structure):
    _pack_ = 1
    _fields_ = [
        # Byte[0]
        ("headerVersion",               c_uint8, 4),
        TWIDL_Tuple("rsvd0_3",          c_uint8, 4).addAttributes(display=False),

        # For some reason not defined
        # Byte[1]
        ("destination",                 c_uint8),

        # Byte[2]
        ("sourceEndpoint",              c_uint8),

        # Byte[3]
        ("messageTag",                  c_uint8, 3),
        ("tagOwner",                    c_uint8, 1),
        ("pktseq",                      c_uint8, 2),
        ("endOfMessage",                c_uint8, 1),
        ("startOfMessage",              c_uint8, 1)
    ]


class pcie_vdm_header(BigEndian_TWIDL_Structure):
    _pack_ = 1
    _fields_ = [
        ("mediumSpecificHeader",        pcie_medium_specific_header),
        ("mctpTransportHeader",         mctp_transport_header)
    ]


class mctp_message_header(BigEndian_TWIDL_Structure):
    _pack_ = 1
    _fields_ = [
        ("messageType",                 c_uint8, 7),
        TWIDL_Tuple("integrityCheck",   c_uint8, 1).addAttributes(
            enumDict={
                0: "No MCTP message integrity check",
                1: "MCTP integrity check is present"
            }
        ),
        # break
        ("messageHeader",               c_uint8), # * M number of bytes. unclear where M comes from
        ("messageData",                 c_uint8), # * N number of bytes. Unclear where N comes from
    ]


class mctp_vdm_packet(BigEndian_TWIDL_Structure):
    _pack_ = 1
    _fields_ = [
        ("transportHeader",             pcie_vdm_header),
        ("packetPayload",               mctp_message_header)
    ]