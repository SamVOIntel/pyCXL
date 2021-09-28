# Python imports
import operator
from types import SimpleNamespace


class Biterator:

    def __init__(self, data):
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
        for byte_val in byte_string:
            bin_val = bin(byte_val)[2:]
            yield "0" * (8 - len(bin_val)) + bin_val


class FlitParser:

    def __init__(self, structs):
        self.__structs = structs
        # create the shape of the struct
        for struct in structs:
            # What if the struct already exists?
            if hasattr(self, struct[0]):
                if len(struct[1]) > 1:
                    for repeated_struct in struct[1]:
                        getattr(self, struct[0]).append(SimpleNamespace())
                        for field in repeated_struct:
                            setattr(getattr(self, struct[0])[-1], field[0], 0)
                else:
                    getattr(self, struct[0]).append(SimpleNamespace())
                    for field in struct[1][0]:
                        setattr(getattr(self, struct[0])[-1], field[0], 0)
            else:
                setattr(self, struct[0], [])
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
        return binStr

    def __int__(self):
        binStr = self.__bin__()
        return int(binStr, 2)

    def __index__(self):
        return operator.index(int(self))

    def __bytes__(self):
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
        data_iter = Biterator(data)
        available_bins = next(data_iter)

        attrs = set([__struct[0] for __struct in self.__structs])
        sub_array_indexes = {attr: 0 for attr in attrs}

        for __struct in self.__structs:
            for array_element in __struct[1]:
                for field_tuple in array_element:
                    while len(available_bins) < field_tuple[1]:
                        available_bins += next(data_iter)
                    value = int(available_bins[:field_tuple[1]], 2)
                    available_bins = available_bins[field_tuple[1]:]
                    setattr(getattr(self, __struct[0])[sub_array_indexes[__struct[0]]], field_tuple[0], value)
                sub_array_indexes[__struct[0]] += 1


