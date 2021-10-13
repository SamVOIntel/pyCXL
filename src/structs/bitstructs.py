# Python imports
import operator

# Package imports
from src.structs.biterator import Biterator
from src.structs.bitfields import BitField


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

    def from_bin(self, binstring: str = ""):
        """
        This class is meant to represent a struct of bit fields. It requires bits to populate.
        """
        if binstring.startswith("0b"):
            binstring = binstring[2:]

        if len(binstring) < self.size:
            raise ValueError("Not enough bins to fill the BitStruct")

        for field in self.fields:
            int_val = int(binstring[:field.size], 2)
            field.value = int_val
            binstring = binstring[field.size:]

    def from_bytes(self, bytestring: bytes):
        """
        Populates the bit struct from a bytearray
        """
        if len(bytestring) < self.size // 8:
            raise ValueError("Not enough bytes to fill the BitStruct")

        data = Biterator(bytestring)
        available_bins = next(data)

        for field in self.fields:
            while len(available_bins) < field.size:
                available_bins += next(data)
            int_val = int(available_bins[:field.size], 2)
            field.value = int_val
            available_bins = available_bins[field.size:]
