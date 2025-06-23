from datetime import datetime
import rich
import modules.utils.logger.config as cfg

__APP_NAME      = f'[bold white on {cfg.APP_NAME_BG_COLOR}]  Domobile  [/]'
__INFO          = f'[bold {cfg.INFO_COLOR}][ INFO  ][/]'
__WARN          = f'[bold {cfg.WARN_COLOR}][ WARN  ][/]'
__ERROR         = f'[bold {cfg.ERROR_COLOR}][ ERROR ][/]'
__FATAL         = f'[bold {cfg.FATAL_COLOR}][ FATAL ][/]'
__DEBUG         = f'[bold {cfg.DEBUG_COLOR}][ DEBUG ][/]'
__INFO_MSG      = lambda msg: f'[{cfg.INFO_MSG_COLOR}]{msg}[/]'
__WARN_MSG      = lambda msg: f'[{cfg.WARN_MSG_COLOR}]{msg}[/]'
__ERROR_MSG     = lambda msg: f'[{cfg.ERROR_MSG_COLOR}]{msg}[/]'
__FATAL_MSG     = lambda msg: f'[{cfg.FATAL_MSG_COLOR}]{msg}[/]'
__DEBUG_MSG     = lambda msg: f'[italic {cfg.DEBUG_MSG_COLOR}]{msg}[/]'
__FMT_TIME      = lambda timestamp: f'[grey30]{datetime.fromtimestamp(timestamp).strftime("%d/%m/%y %H:%M:%S")}[/]'
__FMT_CONTEXT   = lambda context, subcontext, bg, fg: f'[bold {fg} on {bg}]( {context}/{subcontext} )[/]'

def logInfo(timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
    rich.print(
        __APP_NAME, 
        __FMT_TIME(timestamp), 
        __INFO, 
        __FMT_CONTEXT(context, subcontext, bg, fg),
        __INFO_MSG(message)
    )

def logWarn(timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
    rich.print(
        __APP_NAME, 
        __FMT_TIME(timestamp), 
        __WARN, 
        __FMT_CONTEXT(context, subcontext, bg, fg),
        __WARN_MSG(message)
    )

def logError(timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
    rich.print(
        __APP_NAME, 
        __FMT_TIME(timestamp), 
        __ERROR, 
        __FMT_CONTEXT(context, subcontext, bg, fg),
        __ERROR_MSG(message)
    )

def logFatal(timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
    rich.print(
        __APP_NAME, 
        __FMT_TIME(timestamp), 
        __FATAL, 
        __FMT_CONTEXT(context, subcontext, bg, fg),
        __FATAL_MSG(message)
    )

def logDebug(timestamp: int, context: str, subcontext: str, bg: str, fg: str, message: str) -> None:
    rich.print(
        __APP_NAME, 
        __FMT_TIME(timestamp), 
        __DEBUG, 
        __FMT_CONTEXT(context, subcontext, bg, fg),
        __DEBUG_MSG(message)
    )