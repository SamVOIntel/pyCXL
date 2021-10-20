# Python imports
import operator

# Package imports
from pyCXL.structs.biterator import Biterator
from pyCXL.structs.bitstructs import BitStruct


class BitCollection:
    """
    A BitCollection is defined as an ordered collection of BitStructs
    """

    def __init__(self, bitstructs: list[BitStruct], name: str):
        self.__structs = bitstructs
        self.__name = name
        self.__size = sum([struct.size for struct in self.structs])
        self.__idx = 0

    def __iter__(self):
        self.__idx = 0
        return self

    def __next__(self):
        idx = self.idx
        if idx >= len(self.structs):
            raise StopIteration
        self.__idx += 1
        return self.structs[idx]

    def __str__(self):
        retStr = f"{self.name}:\n"
        for struct in self.structs:
            retStr += str(struct)
        return retStr

    def __int__(self):
        binstr = self.to_bin()
        return int(binstr, 2)

    def __bytes__(self):
        intVal = int(self)
        bytes_needed, rem = divmod(self.size, 8)
        if rem:
            bytes_needed += 1
        # int.to_bytes requires a byteorder param
        return intVal.to_bytes(bytes_needed, byteorder='big')

    def __index__(self):
        """
        Brief:
            Enables type conversions such as __hex__
        """
        return operator.index(int(self))

    def __len__(self):
        return len(self.structs)

    def __getitem__(self, item):
        return self.structs[item]

    @property
    def structs(self):
        return self.__structs

    @structs.setter
    def structs(self, new_value):
        raise AttributeError(f"Cannot modify BitCollection's substructs")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_value):
        raise AttributeError("Cannot modify BitCollection's name")

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, new_value):
        raise AttributeError("Cannot modify BitCollection's size")

    @property
    def idx(self):
        return self.__idx

    @idx.setter
    def idx(self, new_value):
        raise AttributeError("Cannot modify BitCollection's index")

    def to_bin(self):
        binstr = ""
        for struct in self.structs:
            binstr += struct.to_bin()
        return binstr

    def to_dict(self):
        """
        Creates a dictionary representation of the struct.

        It's possible that a BitCollection might contain multiple structs
        of the same name.
        """
        return {
            self.name: [
                struct.to_dict() for struct in self
            ]
        }

    def from_bin(self, binstring: str):
        """
        Because this is a collection of bit structs it does make sense that someone
        might want to populate it with bits rather than bytes.
        """
        if binstring.startswith("0b"):
            binstring = binstring[2:]

        if len(binstring) < self.size:
            raise ValueError("Not enough bins to fill the BitCollection")

        for struct in self.structs:
            struct.from_bin(binstring[:struct.size])
            binstring = binstring[struct.size:]

    def from_bytes(self, bytestring: bytes):
        if len(bytestring) < self.size // 8:
            raise ValueError("Not enough bytes to fill the BitCollection")

        data = Biterator(bytestring)
        available_bins = next(data)

        for struct in self.structs:
            while len(available_bins) < struct.size:
                available_bins += next(data)
            struct.from_bin(available_bins[:struct.size])
            available_bins = available_bins[struct.size:]


class FlitStruct(BitCollection):

    def __init__(self, bitstructs: list[BitStruct], name: str):
        super().__init__(bitstructs=bitstructs, name=name)
        if self.size != 128:
            raise ValueError(f"FlitStructs MUST be 128 bits, was {self.size}")