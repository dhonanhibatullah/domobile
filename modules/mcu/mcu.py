import threading
from typing import Optional
import serial
from modules.mcu.frame import MCUFrame
from modules.logger.logger import Logger

class MCUHandler:

    def __init__(self, port: str, baudrate: int, logger: Logger):
        self.__ser: Optional[serial.Serial]
        self.__port     = port
        self.__baudrate = baudrate
        self.__logger   = logger
        self.__ok       = True
        self.__ok_lock  = threading.Lock()
        self.__thread   = threading.Thread(target=self.__routine, name='MCUHandler Thread')

    def start(self) -> None:
        self.__thread.start()

    def stop(self) -> None:
        with self.__ok_lock:
            self.__ok = False
        self.__thread.join()

    def __isOk(self) -> bool:
        with self.__ok_lock:
            return self.__ok

    def __routine(self) -> None:
        self.__ser = serial.Serial(self.__port, self.__baudrate)
        self.__logger.info('init', 'serial initiating...')

        while True:
            b = self.__ser.read()
            if b[0] == 0xDD:
                b += self.__ser.read_until(bytes([0xEE]))
                try:
                    f = MCUFrame()
                    f.parse(b)
                    self.__ser.write(f.dump())
                    self.__logger.info('init', 'serial initiated successfully')
                    break
                except:
                    self.__logger.error('init', 'serial initiation failed, retrying...')
                    continue

        while self.__isOk():
            pass