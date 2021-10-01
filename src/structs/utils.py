# Python imports
import operator
from types import SimpleNamespace


# todo potential good use cases for dataclasses
class Biterator:

    def __init__(self, data):
        """
        Brief:
            An iterator which returns the bits associated with each byte in a bytearray

        Params:
            data: an array of bytes
        """
        self.data = data
        self.size = len(data)
        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        idx = self.index
        if idx >= self.size:
            raise StopIteration
        self.index += 1
        bin_val = bin(self.data[idx])[2:]
        return "0" * (8 - len(bin_val)) + bin_val

    @classmethod
    def generator(cls, byte_string):
        """
        Brief:
            A generator yielding the binary data associated with a bytearray
        """
        for byte_val in byte_string:
            bin_val = bin(byte_val)[2:]
            yield "0" * (8 - len(bin_val)) + bin_val


class BitField:

    def __init__(self, size: int, name: str = "", value: int = 0):
        self.__size = size
        self.__name = name
        self._value = value

    def __int__(self):
        return self.value

    def __index__(self):
        """
        Brief:
            Enables type conversions such as __hex__
        """
        return operator.index(int(self))

    def __str__(self):
        return f"{self.name}:    {self.value}"

    def to_bin(self):
        """
        __bin__ cannot be overloaded in the same way as other methods. Treat this function as if you could.
        """
        binStr = bin(self.value)[2:]
        while len(binStr) < self.size:
            binStr = '0' + binStr
        return binStr

    def to_bytes(self):
        """
        Creates a bytearray of the appropriate size. Unclear what this might be used for.
        """
        bins = self.to_bin()
        num_bytes, rem = divmod(len(bins), 8)
        if rem:
            num_bytes += 1
        return int(bins, 2).to_bytes(num_bytes, 'big')

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if len(bin(new_value)[2:]) > self.size:
            raise ValueError(f"{new_value} is too large for the field size: {self.size} bits")
        self._value = new_value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        raise AttributeError("name field cannot be modified")

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, new_size):
        raise AttributeError("size field cannot be modified")


class BitStruct:

    def __init__(self, bitfields: list[BitField], name: str = ""):
        self.__fields = bitfields
        self.__name = name
        self.__size = sum([field.size for field in bitfields])

    def __str__(self):
        print_width = max([len(field.name) for field in self.fields])
        retStr = f"\t{self.name}:\n"
        for field in self.fields:
            padding = " " * (print_width - len(field.name))
            retStr += f"\t\t{field.name}:{padding}{field.value}\n"
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

    @property
    def fields(self):
        return self.__fields

    @fields.setter
    def fields(self, new_val):
        raise AttributeError("Cannot modify the organization of this BitFieldStruct's BitFields.")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_val):
        raise AttributeError("This BitFieldStruct cannot be re-named.")

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, new_val):
        raise AttributeError("This BitFieldStruct cannot be re-sized.")

    def to_bin(self):
        retStr = ""
        for field in self.fields:
            binStr = bin(field.value)[2:]
            while len(binStr) < field.size:
                binStr = '0' + binStr
            retStr += binStr
        return retStr

    def to_bytes(self):
        """
        Creates a bytearray of the appropriate size. Unclear what this might be used for.
        """
        bins = self.to_bin()
        num_bytes, rem = divmod(len(bins), 8)
        if rem:
            num_bytes += 1
        return int(bins, 2).to_bytes(num_bytes, 'big')

    def from_binary(self, binstring: str = ""):
        """
        This class is meant to represent a struct of bit fields. It requires bits to populate.
        """
        if binstring.startswith("0b"):
            binstring = binstring[2:]

        for field in self.fields:
            int_val = int(binstring[:field.size], 2)
            field.value = int_val
            binstring = binstring[field.size:]

    def from_bytes(self, bytestring: bytes):
        """
        Populates the bit struct from a bytearray
        """
        data = Biterator(bytestring)
        available_bins = next(data)

        for field in self.fields:
            while len(available_bins) < field.size:
                available_bins += next(data)
            int_val = int(available_bins[:field.size], 2)
            field.value = int_val
            available_bins = available_bins[field.size:]


class FlitStruct:
    """
    A FlitStruct is defined as a 16 byte ordered collection of BitStructs
    """

    def __init__(self, bitstructs: list[BitStruct], name: str = ""):
        self.__structs = bitstructs
        self.__name = name
        # A FlitStruct is specifically 128 bits
        self.__size = 128

        total_size = sum([struct.size for struct in self.structs])
        if total_size != self.size:
            raise ValueError(f"Expected 128 bits, was {total_size}")

    def __str__(self):
        retStr = f"{self.name}:\n"
        for struct in self.structs:
            retStr += str(struct)
        return retStr

    def __int__(self):
        binstr = self.to_bin()
        return int(binstr, 2)

    def __bytes__(self):
        binStr = self.to_bin()
        byteStr = b""
        for i in range(0, len(binStr), 8):
            intVal = int(binStr[i:i + 8], 2)
            # int.to_bytes requires a byteorder param
            byteStr += intVal.to_bytes(1, byteorder='big')
        while len(byteStr) < 16:
            byteStr = b"\x00" + byteStr
        return byteStr

    def __index__(self):
        """
        Brief:
            Enables type conversions such as __hex__
        """
        return operator.index(int(self))

    @property
    def structs(self):
        return self.__structs

    @structs.setter
    def structs(self, new_value):
        raise AttributeError("Cannot modify FlitStruct substructs")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_value):
        raise AttributeError("Cannot modify FlitStruct's name")

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, new_value):
        raise AttributeError("Cannot modify FlitStruct's size")

    def to_bin(self):
        binstr = ""
        for struct in self.structs:
            binstr += struct.to_bin()
        return binstr

    def from_bytes(self, bytestring: bytes):
        data = Biterator(bytestring)
        available_bins = next(data)

        for struct in self.structs:
            while len(available_bins) < struct.size:
                available_bins += next(data)
            struct.from_binary(available_bins[:struct.size])
            available_bins = available_bins[struct.size:]



class FlitParser:
    """
    Brief:
        A generic "flit" parser. A "flit" being a 128 bit struct containing a collection of arbitrarily sized substructs
    """

    def __init__(self, structs):
        """
        Brief:
            Constructor

        Params:
            structs:
                structs refers to a specifically formatted list of lists. Below is a schematic representation of one.

                # list of substructures
                [
                    # substructure
                    [                       # list of field lists
                        "substruct_name",   [   # list of fields
                                                [
                                                ("field_name",      int(size_of_field_in_bits)),
                                                . . .
                                                ]
                                            ]
                    ],
                    . . .
                ]

            It is list of tuples which represent the name of a field and the size in bits of that field. Each list of
            field tuples is associated with the name of a substructure. Each substructure is contained in a list of
            substructures.
        """
        self.__structs = structs
        # create the shape of the struct
        for struct in structs:
            if hasattr(self, struct[0]):
                self._add_struct(struct)
            else:
                setattr(self, struct[0], [])
                self._add_struct(struct)

    def _add_struct(self, struct):
        if len(struct[1]) > 1:
            for repeated_struct in struct[1]:
                getattr(self, struct[0]).append(SimpleNamespace())
                for field in repeated_struct:
                    setattr(getattr(self, struct[0])[-1], field[0], 0)
        else:
            getattr(self, struct[0]).append(SimpleNamespace())
            for field in struct[1][0]:
                setattr(getattr(self, struct[0])[-1], field[0], 0)

    def __str__(self):
        """
        Brief:
            Creates a str representation of the class such as the example below:
                struct[index]:
                    field:    value
                    . . .

                struct[index + 1]:
                    field:    value

        """
        retStr = ""
        printable_attrs = [
            __struct[0] for __struct in self.__structs if "RSVD" not in __struct[0]
        ]
        for attr in printable_attrs:
            struct_array = getattr(self, attr)
            for idx, struct in enumerate(struct_array):
                retStr += f"{attr}[{idx}]:\n"
                printable_fields = [
                    field for field in dir(struct)
                    if not field.startswith("_") and "RSVD" not in field
                ]
                print_width = max([len(field) for field in printable_fields])
                for field in printable_fields:
                    padding = " " * (print_width - len(field) + 4)
                    retStr += f"\t{field}:{padding}{getattr(struct, field)}\n"
                retStr += "\n"
        return retStr

    def __bin__(self):
        """
        Brief:
            Creates a binary representation of the struct of size 128 bits. this method does not actually override
            bin(self) in the same way that __int__ does. It is named as a dunder method though because that's how it
            is used.
        """
        binStr = ""

        attrs = set([__struct[0] for __struct in self.__structs])
        sub_array_indexes = {attr: 0 for attr in attrs}

        for __struct in self.__structs:
            for struct_array in __struct[1]:
                for field in struct_array:
                    val = getattr(
                        getattr(
                            self, __struct[0]
                        )[sub_array_indexes[__struct[0]]],
                        field[0]
                    )
                    binVal = bin(val)[2:]
                    while len(binVal) < field[1]:
                        binVal = "0" + binVal
                    binStr += binVal
                sub_array_indexes[__struct[0]] += 1
        if len(binStr) != 128:
            raise ValueError(f"The binary representation of this struct was {len(binStr)} bits, expected 128!")
        return binStr

    def __int__(self):
        """
        Brief:
            Returns an int representation of the Flit
        """
        binStr = self.__bin__()
        return int(binStr, 2)

    def __index__(self):
        """
        Brief:
            Enables type conversions such as __hex__
        """
        return operator.index(int(self))

    def __bytes__(self):
        """
        Brief:
            Ensures that the byte representation of the Flit is the correct size
        """
        binStr = self.__bin__()
        byteStr = b""
        for i in range(0, len(binStr), 8):
            intVal = int(binStr[i:i+8], 2)
            # int.to_bytes requires a byteorder param even though it doesnt matter as I am looking at 1 byte
            byteStr += intVal.to_bytes(1, byteorder='big')
        while len(byteStr) < 16:
            byteStr += b"\x00"
        return byteStr

    def from_buffer(self, data):
        """
        Brief:
            Modelled after the Ctypes Structure.from_buffer() class method, this takes in a bytearray and populates the
            substructure. If the FlitParser has not already been initialized then nothing will happen. No endian-ness
            is specified because it is assumed that the order of fields to be filled and the order of bytes in the
            array are already in alignment.
        """
        data_iter = Biterator(data)
        available_bins = next(data_iter)

        attrs = set([__struct[0] for __struct in self.__structs])
        sub_array_indexes = {attr: 0 for attr in attrs}

        # iterate over each field in each struct
        for __struct in self.__structs:
            for array_element in __struct[1]:
                for field_tuple in array_element:

                    # make sure I have enough bits to set the field value
                    while len(available_bins) < field_tuple[1]:
                        available_bins += next(data_iter)

                    # calculate the field value
                    value = int(available_bins[:field_tuple[1]], 2)

                    # consume the bins used to calculate the value
                    available_bins = available_bins[field_tuple[1]:]

                    # set the value
                    setattr(getattr(self, __struct[0])[sub_array_indexes[__struct[0]]], field_tuple[0], value)

                # increment the array index when finished with all fields in the array element
                sub_array_indexes[__struct[0]] += 1


