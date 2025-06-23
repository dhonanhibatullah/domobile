from typing import Optional
import binascii

class MCUFrame:

    def __init__(self):
        self.id:          Optional[int]
        self.address:     Optional[int]
        self.data:        Optional[bytes]
        self.data_len:    Optional[int]

    def create(self, id: int, address: int, data: bytes) -> None:
        self.id       = id
        self.address  = address
        self.data     = data
        self.data_len = len(data)

    def parse(self, frame: bytes) -> None:
        if frame[0] != 0xDD:
            raise ValueError('header is not 0xDD')
        elif frame[-1] != 0xDD:
            raise ValueError('tail is not 0xDD')
        
        crc_rx = (frame[-2] << 8) | frame[-3]
        crc_ex = binascii.crc_hqx(frame[1:-3], 0xFFFF)
        if crc_rx != crc_ex:
            raise ValueError('CRC does not match')
        
        len_rx = (frame[5] << 8) | frame[4]
        len_ex = len(frame) - 9
        if len_rx != len_ex:
            raise ValueError('data length does not match')
        
        self.id         = frame[1]
        self.address    = (frame[3] << 8) | frame[2] 
        self.data       = frame[6:-3]
        self.data_len   = len_rx
        
    def dump(self) -> bytes:
        if self.id == None or self.address == None or self.data == None or self.data_len == None:
            raise ValueError('incomplete data initiation') 

        frame   = bytes([self.id, self.address & 0xFF, (self.address >> 8) & 0xFF, self.data_len & 0xFF, (self.data_len >> 8) & 0xFF]) + self.data
        crc     = binascii.crc_hqx(frame, 0xFFFF)
        frame   = bytes([0xDD]) + frame + bytes([crc & 0xFF, (crc >> 8) & 0xFF]) + bytes([0xDD])
        return frame