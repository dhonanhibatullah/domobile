import time
from typing import Optional, Literal
from modules.logger.db import LoggerDB
from modules.logger.fmt import LoggerFmt

class Logger:
    __db: Optional[LoggerDB]    = None
    __fmt: Optional[LoggerFmt]  = None

    def __init__(self, context: str, bg: str = '#000000', fg: str = '#FFFFFF', path: str = ''):
        self.__context  = context
        self.__bg       = bg
        self.__fg       = fg

        if not Logger.__db:
            Logger.__db = LoggerDB(path)
        if not Logger.__fmt:
            Logger.__fmt = LoggerFmt()

    async def logInfo(self, subcontext: str, message: str) -> None:
        ts = int(time.time())
        Logger.__fmt.logInfo(
            ts, 
            self.__context, 
            subcontext,
            self.__bg,
            self.__fg,
            message
        )
        await Logger.__db.logInfo(
            ts,
            self.__context,
            subcontext,
            message
        )

    async def logWarn(self, subcontext: str, message: str) -> None:
        ts = int(time.time())
        Logger.__fmt.logWarn(
            ts, 
            self.__context, 
            subcontext,
            self.__bg,
            self.__fg,
            message
        )
        await Logger.__db.logWarn(
            ts,
            self.__context,
            subcontext,
            message
        )

    async def logError(self, subcontext: str, message: str) -> None:
        ts = int(time.time())
        Logger.__fmt.logError(
            ts, 
            self.__context, 
            subcontext,
            self.__bg,
            self.__fg,
            message
        )
        await Logger.__db.logError(
            ts,
            self.__context,
            subcontext,
            message
        )

    async def logFatal(self, subcontext: str, message: str) -> None:
        ts = int(time.time())
        Logger.__fmt.logFatal(
            ts, 
            self.__context, 
            subcontext,
            self.__bg,
            self.__fg,
            message
        )
        await Logger.__db.logFatal(
            ts,
            self.__context,
            subcontext,
            message
        )

    async def logDebug(self, subcontext: str, message: str) -> None:
        ts = int(time.time())
        Logger.__fmt.logDebug(
            ts, 
            self.__context, 
            subcontext,
            self.__bg,
            self.__fg,
            message
        )
        await Logger.__db.logDebug(
            ts,
            self.__context,
            subcontext,
            message
        )