# Python imports
import operator
from math import ceil

# Package imports
from pyCXL.structs.biterator import Biterator
from pyCXL.structs.bitfields import BitField

BITS_IN_A_BYTE = 8


class BitStruct:

    def __init__(self, bitfields: list[BitField], name: str):
        self.__fields = bitfields
        self.__name = name
        self.__size = sum([field.size for field in bitfields])
        self.__idx = 0

    def __str__(self):
        print_width = max([len(field.name) for field in self.fields])
        retStr = f"\t{self.name}:\n"
        for field in self.fields:
            if field.rsvd:
                continue
            padding = " " * (print_width - len(field.name) + 4)
            retStr += f"\t\t{field.name}:{padding}{field.value}"
            if field.enums:
                additional_value = field.enums.get(field.value, False)
                if additional_value:
                    retStr += f"\t{additional_value}"
            retStr += "\n"
        return retStr

    def __int__(self):
        binstr = self.to_bin()
        return int(binstr, 2)

    def __index__(self):
        """
        Brief:
            Enables type conversions such as __hex__
        """
        return operator.index(int(self))

    def __bytes__(self):
        """
        Creates a bytearray of the appropriate size. Unclear what this might be used for.
        """
        intVal = int(self)
        bytes_needed, rem = divmod(self.size, 8)
        if rem:
            bytes_needed += 1
        return intVal.to_bytes(bytes_needed, 'big')

    def __iter__(self):
        self.__idx = 0
        return self

    def __next__(self):
        idx = self.idx
        if idx >= len(self.fields):
            raise StopIteration
        self.__idx += 1
        return self.fields[idx]

    def __getitem__(self, item):
        return self.fields[item]

    @property
    def fields(self):
        return self.__fields

    @fields.setter
    def fields(self, new_val):
        raise AttributeError("Cannot modify BitStruct's fields")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_val):
        raise AttributeError("Cannot modify BitStruct's name")

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, new_val):
        raise AttributeError("Cannot modify BitStruct's size")

    @property
    def idx(self):
        return self.__idx

    @idx.setter
    def idx(self, new_value):
        raise AttributeError("Cannot modify BitStruct's index")

    def to_bin(self):
        retStr = ""
        for field in self.fields:
            binStr = bin(field.value)[2:]
            while len(binStr) < field.size:
                binStr = '0' + binStr
            retStr += binStr
        return retStr

    def to_dict(self):
        return {self.name: {field.name: field.value for field in self}}

    def from_bin(self, bitstring: str = ""):
        """
        This class is meant to represent a struct of bit fields. It requires bits to populate.
        """
        if self.size > BITS_IN_A_BYTE:
            raise NotImplementedError(
                "You must specify an Endianness by using eiter LittleEndianBitStruct or BigEndianBitStruct"
            )

        if bitstring.startswith("0b"):
            bitstring = bitstring[2:]

        for field in self.fields:
            int_val = int(bitstring[:field.size], 2)
            field.value = int_val
            bitstring = bitstring[field.size:]

    def from_bytes(self, bytestring: bytes):
        """
        Populates the bit struct from a bytearray
        """
        if self.size > BITS_IN_A_BYTE:
            raise NotImplementedError(
                "You must specify an Endianness by using eiter LittleEndianBitStruct or BigEndianBitStruct"
            )

        # there should only be 1 byte worth of data
        data = Biterator(bytestring)
        available_bins = next(data)

        for field in self.fields:
            field.value = int(available_bins[:field.size], 2)
            available_bins = available_bins[field.size:]


class LittleEndianBitStruct(BitStruct):

    def to_bin(self):
        retStr = ""
        for field in self.fields:
            binStr = bin(field.value)[2:]
            while len(binStr) < field.size:
                binStr = '0' + binStr
            retStr += binStr
        return retStr

    def from_bin(self, bitstring: str = ""):
        """
        This class is meant to represent a struct of bit fields. It requires bits to populate.
        """
        if bitstring.startswith("0b"):
            bitstring = bitstring[2:]

        if len(bitstring) < self.size:
            raise ValueError("Not enough bins to fill the BitStruct")

        for field in self.fields:
            field.value = int(bitstring[:field.size], 2)
            bitstring = bitstring[field.size:]

    def from_bytes(self, bytestring: bytes):
        """
        Populates the bit struct from a bytearray
        """
        if len(bytestring) < ceil(self.size / BITS_IN_A_BYTE):
            raise ValueError("Not enough bytes to fill the BitStruct")

        data = Biterator(bytestring)
        available_bins = next(data)

        for field in self.fields:
            while len(available_bins) < field.size:
                available_bins += next(data)
            field.value = int(available_bins[:field.size], 2)
            available_bins = available_bins[field.size:]


class BigEndianBitStruct(BitStruct):

    def to_bin(self):
        """
        This is where I learned to hate big endian. Here's a puzzle for you:
            Given 3 random integers and three random number of bits *at least* large enough to represent those numbers,
            produce a stream of bits which equals those values in big endian.

        For example:
            integer:  20  number of bits: 7
            integer:  85  number of bits: 13
            integer:  255 number of bits: 9

        See if you can do that more efficiently than what I have below, then see if you can do it more efficiently than
        little endian above.
        """
        bitvals = []
        for field in self.fields:
            bitstr = bin(field.value)[2:]
            while len(bitstr) < field.size:
                bitstr = '0' + bitstr
            bitvals.append(bitstr)
        retstr = ""
        line = ""
        for val in bitvals:
            for eachbit in val[::-1]:
                line = eachbit + line
                if len(line) == 8:
                    retstr += line
                    line = ""
        retstr += line
        return retstr

    def from_bin(self, bitstring: str = ""):
        """
        This class is meant to represent a struct of bit fields. It requires bits to populate.
        """
        if bitstring.startswith("0b"):
            bitstring = bitstring[2:]

        if len(bitstring) < self.size:
            raise ValueError("Not enough bins to fill the BitStruct")

        bitstring = bitstring[:self.size]

        # reverse the order of the binary in byte sized chucks
        be_order = "".join(
                reversed([bitstring[i:i + BITS_IN_A_BYTE] for i in range(0, len(bitstring), BITS_IN_A_BYTE)])
        )

        bit_idx = 0
        available_bins = be_order[bit_idx:bit_idx + BITS_IN_A_BYTE]

        for field in reversed(self.fields):
            while len(available_bins) < field.size:
                bit_idx += BITS_IN_A_BYTE
                available_bins += be_order[bit_idx:bit_idx + BITS_IN_A_BYTE]
            field.value = int(available_bins[:field.size], 2)
            available_bins = available_bins[field.size:]

    def from_bytes(self, bytestring: bytes):
        """
        Populates the bit struct from a bytearray
        """
        if len(bytestring) < ceil(self.size / BITS_IN_A_BYTE):
            raise ValueError("Not enough bytes to fill the BitStruct")

        bytestring = bytestring[:ceil(self.size / BITS_IN_A_BYTE)]
        bytestring = bytestring[::-1]

        trim = (len(bytestring) * 8) % self.size

        data = Biterator(bytestring)
        available_bins = next(data)

        if trim:
            available_bins = available_bins[:len(available_bins) - trim]

        for field in reversed(self.fields):
            while len(available_bins) < field.size:
                available_bins += next(data)
            field.value = int(available_bins[:field.size], 2)
            available_bins = available_bins[field.size:]
