from typing import Literal
from datetime import datetime
import rich
import modules.utils.logger.config as cfg

class LoggerFmt:

    def __init__(self):
        self.__app_name = f'[bold white on {cfg.APP_NAME_BG_COLOR}]  Domobile  [/]'
        self.__info     = f'[bold {cfg.INFO_COLOR}][ INFO  ][/]'
        self.__warn     = f'[bold {cfg.WARN_COLOR}][ WARN  ][/]'
        self.__error    = f'[bold {cfg.ERROR_COLOR}][ ERROR ][/]'
        self.__fatal    = f'[bold {cfg.FATAL_COLOR}][ FATAL ][/]'
        self.__debug    = f'[bold {cfg.DEBUG_COLOR}][ DEBUG ][/]'

        self.__info_msg     = lambda msg: f'[{cfg.INFO_MSG_COLOR}]{msg}[/]'
        self.__warn_msg     = lambda msg: f'[{cfg.WARN_MSG_COLOR}]{msg}[/]'
        self.__error_msg    = lambda msg: f'[{cfg.ERROR_MSG_COLOR}]{msg}[/]'
        self.__fatal_msg    = lambda msg: f'[{cfg.FATAL_MSG_COLOR}]{msg}[/]'
        self.__debug_msg    = lambda msg: f'[italic {cfg.DEBUG_MSG_COLOR}]{msg}[/]'

    def fmtTime(self, timestamp: int) -> str:
        return f'[grey30]{datetime.fromtimestamp(timestamp).strftime("%d/%m/%y %H:%M:%S")}[/]'
    
    def fmtContext(self, context: str, subcontext: str, bg: str, fg: str) -> str:
        return f'[bold {fg} on {bg}]( {context}/{subcontext} )[/]'

    async def logInfo(self, timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
        rich.print(
            self.__app_name, 
            self.fmtTime(timestamp), 
            self.__info, 
            self.fmtContext(context, subcontext, bg, fg),
            self.__info_msg(message)
        )

    async def logWarn(self, timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
        rich.print(
            self.__app_name, 
            self.fmtTime(timestamp), 
            self.__warn, 
            self.fmtContext(context, subcontext, bg, fg),
            self.__warn_msg(message)
        )

    async def logError(self, timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
        rich.print(
            self.__app_name, 
            self.fmtTime(timestamp), 
            self.__error, 
            self.fmtContext(context, subcontext, bg, fg),
            self.__error_msg(message)
        )

    async def logFatal(self, timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
        rich.print(
            self.__app_name, 
            self.fmtTime(timestamp), 
            self.__fatal, 
            self.fmtContext(context, subcontext, bg, fg),
            self.__fatal_msg(message)
        )

    async def logDebug(self, timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
        rich.print(
            self.__app_name, 
            self.fmtTime(timestamp), 
            self.__debug, 
            self.fmtContext(context, subcontext, bg, fg),
            self.__debug_msg(message)
        )