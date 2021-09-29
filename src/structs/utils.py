# Python imports
import operator
from types import SimpleNamespace


class Biterator:

    def __init__(self, data):
        """
        Brief:
            An iterator which returns the bits associated with each byte in a bytearray

        Params:
            data: an array of bytes
        """
        self.data = data
        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        idx = self.index
        if idx >= len(self.data):
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
        if len(binStr) > 128:
            raise ValueError("The binary representation of this struct was greater than 16 bytes!")
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


