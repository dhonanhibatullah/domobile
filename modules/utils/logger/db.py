import asyncio
from typing import Literal
import sqlite3

class LoggerDBModel:

    def __init__(self, id: int, timestamp: int, level: str, context: str, subcontext: str, message: str):
        self.id         = id
        self.timestamp  = timestamp
        self.level      = level
        self.context    = context
        self.subcontext = subcontext
        self.message    = message

class LoggerDB:

    def __init__(self, path: str):
        self.__path     = path
        self.__conn     = sqlite3.connect(self.__path, check_same_thread=False)
        self.__cursor   = self.__conn.cursor()
        self.__lock     = asyncio.Lock()

        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER NOT NULL,
                level TEXT NOT NULL,
                context TEXT NOT NULL,
                subcontext TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        self.__conn.commit()

    async def log(self, timestamp: int, level: Literal['INFO', 'WARN', 'ERROR', 'FATAL', 'DEBUG'], context: str, subcontext: str, message: str) -> None:
        async with self.__lock:
            self.__cursor.execute('''
                INSERT INTO logs (timestamp, level, context, subcontext, message)
                VALUES (?, ?, ?, ?, ?)
            ''', (timestamp, level, context, subcontext, message))
            self.__conn.commit()

    async def logInfo(self, timestamp: int, context: str, subcontext: str, message: str) -> None:
        await self.log(timestamp, 'INFO', context, subcontext, message)

    async def logWarn(self, timestamp: int, context: str, subcontext: str, message: str) -> None:
        await self.log(timestamp, 'WARN', context, subcontext, message)

    async def logError(self, timestamp: int, context: str, subcontext: str, message: str) -> None:
        await self.log(timestamp, 'ERROR', context, subcontext, message)

    async def logFatal(self, timestamp: int, context: str, subcontext: str, message: str) -> None:
        await self.log(timestamp, 'FATAL', context, subcontext, message)

    async def logDebug(self, timestamp: int, context: str, subcontext: str, message: str) -> None:
        await self.log(timestamp, 'DEBUG', context, subcontext, message)

    async def getLogs(self, n: int) -> list[LoggerDBModel]:
        logs = []
        async with self.__lock:
            self.__cursor.execute('''
                SELECT * FROM logs
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (n,))
            logs =  self.__cursor.fetchall()
        return [LoggerDBModel(*log) for log in logs]
    
    async def getLogsByTimestamp(self, start: int, end: int) -> list[tuple]:
        logs = []
        async with self.__lock:
            self.__cursor.execute('''
                SELECT * FROM logs
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp DESC
            ''', (start, end))
            logs = self.__cursor.fetchall()
        return [LoggerDBModel(*log) for log in logs]
    
    def close(self) -> None:
        self.__conn.close()
        self.__cursor.close()