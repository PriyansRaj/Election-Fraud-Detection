import sys
import traceback
from datetime import datetime
from src.logging import logger

class CustomError(Exception):
    def __init__(self,message:str,error:Exception =None):
        super().__init__(message)
        self.timestamp = datetime.now()
        self.message= message
        self.error = error
        self.traceback = self._get_traceback_info()
        self._log_error()
    def _get_traceback_info(self):
        return "".join(traceback.format_exception(*sys.exc_info())) if sys.exc_info()[0] else None
    def _log_error(self):
        logger.error(f"CustomError: {self.message}"
                     + (f" | Root cause :{repr(self.error)}" if self.error else ""))
        if self.traceback:
            logger.debug(f"Traceback:\n{self.traceback}")
    def __str__(self):
        base_msg = f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {self.message}"
        if self.error:
            base_msg += f" | Root Cause: {repr(self.error)}"
        return base_msg




