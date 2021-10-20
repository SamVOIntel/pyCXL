# External Dependencies
import pytest

# Package imports
from tests.test_utils import (
    EIGHT_BIT_STRUCT,
    TEN_BIT_STRUCT,
    FIFTEEN_BIT_STRUCT,
    TWENTY_BIT_STRUCT,
    THIRTY_BIT_STRUCT,
    FORTY_BIT_STRUCT
)
from pyCXL.structs.bitcollections import FlitStruct
# ============================= FlitStruct Tests =============================
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
            ], True
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
            ], True
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
            ], True
        ),
        (
            [
                EIGHT_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ], True
        ),
        (
            # too small
            [
                FIFTEEN_BIT_STRUCT(),
                FORTY_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT()
            ], False
        ),
        (
            # too big
            [
                EIGHT_BIT_STRUCT(),
                TEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                FIFTEEN_BIT_STRUCT(),
                TWENTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                THIRTY_BIT_STRUCT(),
                EIGHT_BIT_STRUCT(),
            ], False
        )
    ]
)
def test_FlitStruct_must_be_128_bits(bitstructs, expected):
    try:
        FlitStruct(bitstructs=bitstructs, name="TEST FLITSTRUCT")
        assert expected
    except ValueError as err:
        assert f"FlitStructs MUST be 128 bits, was" in str(err)
        assert expected is False
