import threading
import time
import queue
from modules.logger.db import LoggerDB
import modules.logger.fmt as fmt

INFO_TYPE     = 0
WARN_TYPE     = 1
ERROR_TYPE    = 2
FATAL_TYPE    = 3
DEBUG_TYPE    = 4

class Logger:

    def __init__(self, context: str, bg: str, fg: str, queue: queue.Queue):
        self.__context  = context
        self.__bg       = bg
        self.__fg       = fg
        self.__queue    = queue

    def info(self, subcontext: str, message: str) -> None:
        self.__queue.put((
            INFO_TYPE,
            int(time.time()),
            self.__context,
            subcontext,
            self.__bg,
            self.__fg,
            message
        ))

    def warn(self, subcontext: str, message: str) -> None:
        self.__queue.put((
            WARN_TYPE,
            int(time.time()),
            self.__context,
            subcontext,
            self.__bg,
            self.__fg,
            message
        ))

    def error(self, subcontext: str, message: str) -> None:
        self.__queue.put((
            ERROR_TYPE,
            int(time.time()),
            self.__context,
            subcontext,
            self.__bg,
            self.__fg,
            message
        ))

    def fatal(self, subcontext: str, message: str) -> None:
        self.__queue.put((
            FATAL_TYPE,
            int(time.time()),
            self.__context,
            subcontext,
            self.__bg,
            self.__fg,
            message
        ))

    def debug(self, subcontext: str, message: str) -> None:
        self.__queue.put((
            DEBUG_TYPE,
            int(time.time()),
            self.__context,
            subcontext,
            self.__bg,
            self.__fg,
            message
        ))

class LoggerHandler:

    def __init__(self, path: str, debug: bool):
        self.__db       = LoggerDB(path)
        self.__debug    = debug
        self.__ok       = True
        self.__ok_lock  = threading.Lock()
        self.__msg_q    = queue.Queue()
        self.__thread   = threading.Thread(target=self.__routine, name='LoggerHandler Thread')

    def createLogger(self, context: str, bg: str='#000000', fg: str='#FFFFFF') -> Logger:
        return Logger(context, bg, fg, self.__msg_q)
        
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
        while self.__isOk():
            try:
                log = self.__msg_q.get(timeout=1)
                if log[0] == INFO_TYPE:       
                    self.__logInfo(log[1], log[2], log[3], log[4], log[5], log[6])
                elif log[0] == WARN_TYPE:     
                    self.__logWarn(log[1], log[2], log[3], log[4], log[5], log[6])
                elif log[0] == ERROR_TYPE:    
                    self.__logError(log[1], log[2], log[3], log[4], log[5], log[6])
                elif log[0] == FATAL_TYPE:    
                    self.__logFatal(log[1], log[2], log[3], log[4], log[5], log[6])
                elif log[0] == DEBUG_TYPE:    
                    self.__logDebug(log[1], log[2], log[3], log[4], log[5], log[6])
            except:
                pass

    def __logInfo(self, timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
        fmt.logInfo(
            timestamp, 
            context, 
            subcontext,
            bg,
            fg,
            message
        )
        self.__db.logInfo(
            timestamp,
            context,
            subcontext,
            message
        )

    def __logWarn(self, timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
        fmt.logWarn(
            timestamp, 
            context, 
            subcontext,
            bg,
            fg,
            message
        )
        self.__db.logWarn(
            timestamp,
            context,
            subcontext,
            message
        )

    def __logError(self, timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
        fmt.logError(
            timestamp, 
            context, 
            subcontext,
            bg,
            fg,
            message
        )
        self.__db.logError(
            timestamp,
            context,
            subcontext,
            message
        )

    def __logFatal(self, timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
        fmt.logFatal(
            timestamp, 
            context, 
            subcontext,
            bg,
            fg,
            message
        )
        self.__db.logFatal(
            timestamp,
            context,
            subcontext,
            message
        )

    def __logDebug(self, timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
        if self.__debug:
            fmt.logDebug(
                timestamp, 
                context, 
                subcontext,
                bg,
                fg,
                message
            )
            self.__db.logDebug(
                timestamp,
                context,
                subcontext,
                message
            )