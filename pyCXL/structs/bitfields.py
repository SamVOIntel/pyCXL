# Python imports
import operator


class BitField:

    def __init__(self, size: int, name: str, value: int = 0, enums: dict = None, rsvd: bool = False):
        self.__size     = size
        self.__name     = name
        self.__enums    = enums
        self.__rsvd     = rsvd
        self._value     = value

    def __int__(self):
        return self.value

    def __index__(self):
        """
        Brief:
            Enables type conversions such as __hex__
        """
        return operator.index(int(self))

    def __str__(self):
        if self.rsvd:
            return ""

        retStr = f"{self.name}:\t{self.value}"

        if self.enums:
            additional_info = self.enums.get(self.value, "")
            if additional_info:
                retStr += f"\t{additional_info}"

        retStr += "\n"
        return retStr

    def __bytes__(self):
        """
        Creates a bytearray of the appropriate size. Unclear what this might be used for.
        """
        intVal = int(self)
        bytes_needed, rem = divmod(self.size, 8)
        if rem:
            bytes_needed += 1
        return intVal.to_bytes(bytes_needed, 'big')

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, new_size):
        raise AttributeError("size field cannot be modified")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        raise AttributeError("name field cannot be modified")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if len(bin(new_value)[2:]) > self.size:
            raise ValueError(f"{new_value} is too large for the field size: {self.size} bits")
        self._value = new_value

    @property
    def enums(self):
        return self.__enums

    @enums.setter
    def enums(self, new_enums):
        raise AttributeError("enums field cannot be modified")

    @property
    def rsvd(self):
        return self.__rsvd

    @rsvd.setter
    def rsvd(self, new_rsvd):
        raise AttributeError("rsvd field cannot be modified")

    def to_dict(self):
        return {self.name: self.value}

    def to_bin(self):
        """
        __bin__ cannot be overloaded in the same way as other methods. Treat this function as if you could.
        """
        binStr = bin(self.value)[2:]
        while len(binStr) < self.size:
            binStr = '0' + binStr
        return binStr