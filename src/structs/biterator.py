class Biterator:

    def __init__(self, data: bytes):
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