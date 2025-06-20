import binascii

class MCUFrame:

    def __init__(self, id: int, address: int, data: bytes | bytearray):
        self.__data_len = len(data)
        self.__frame    = bytearray([id, address & 0xFF, (address >> 8) & 0xFF, self.__data_len & 0xFF, (self.__data_len >> 8) & 0xFF]) + bytearray(data)
        self.__crc      = binascii.crc_hqx(self.__frame, 0xFFFF)
        self.__frame    = bytearray([0xDD]) + self.__frame + bytearray([self.__crc & 0xFF, (self.__crc >> 8) & 0xFF]) + bytearray([0xDD])
        
    def getBytes(self) -> bytes:
        return bytes(self.__frame)