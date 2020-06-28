#!/usr/bin/python3

from time import time as _time


class LogAll:
    """
    'LogConsole' and 'LogFile' classes in one class

    :since: 0.1.0
    """

    def __init__(self, log_fname: str, critical_fname: str = None, debug_fname: str = None, error_fname: str = None, info_fname: str = None, warning_fname: str = None,
                 console_log_format: str = "[{runtime}] - {filename}(line: {lineno}) - {levelname}: {message}",
                 file_log_format: str = "[{year}-{month}-{day} {hour}:{minute}:{second}] - {filename}(line: {lineno}) - {levelname}: {message}") -> None:
        """
        :param log_fname: str
            filename of the file to which all logging messages should be saved
            syntax: <filename>
            example: "/home/pi/test.log"
        :param critical_fname: str, optional
            filename of the file to which critical logging messages should be saved
            syntax: <filename>
            example: "/home/pi/test_critical.log"
        :param debug_fname: str, optional
            filename of the file to which debug logging messages should be saved
            syntax: <filename>
            example: "/home/pi/test_debug.log"
        :param error_fname: str, optional
            filename of the file to which error logging messages should be saved
            syntax: <filename>
            example: "/home/pi/test_error.log"
        :param info_fname: str, optional
            filename of the file to which info logging messages should be saved
            syntax: <filename>
            example: "/home/pi/test_info.log"
        :param warning_fname: str, optional
            filename of the file to which warning logging messages should be saved
            syntax: <fname>
            example: "/home/pi/test_warning.log"
        :param console_log_format: str, optional
            format of the console output
            syntax: <format>
            example: [{runtime}] - {filename}(line: {lineno}) - {levelname}: {message}
            NOTE: in 'format' you can use the following curly bracktes:
                year            gives the year back
                month           gives the month back
                day             gives the day back
                hour            gives the hour back
                minute          gives the minute back
                second          gives the second back
                microsecond     gives the microsecond back
                runtime         gives the back since the logger has started
                levelname       gives the levelname back
                filename        gives the name of the file from which the logger is called back
                lineno          gives the line number back from which the levelname function was called
                function        gives the function back from which the levelname function was called
                message         gives the in levelname function given message back
        :param file_log_format: str, optional
            format of the output that should be write to file
            syntax: <format>
            example: [{runtime}] - {filename}(line: {lineno}) - {levelname}: {message}
            NOTE: in 'format' you can use the following curly bracktes:
                year            gives the year back
                month           gives the month back
                day             gives the day back
                hour            gives the hour back
                minute          gives the minute back
                second          gives the second back
                microsecond     gives the microsecond back
                runtime         gives the back since the logger has started
                levelname       gives the levelname back
                filename        gives the name of the file from which the logger is called back
                lineno          gives the line number back from which the levelname function was called
                function        gives the function back from which the levelname function was called
                message         gives the in levelname function given message back
        :return: None

        :since: 0.1.0
        """
        from datetime import datetime
        from inspect import getframeinfo, stack

        caller_infos = getframeinfo(stack()[1][0])
        self.log_fname = log_fname

        self.critical_fname = critical_fname
        self.debug_fname = debug_fname
        self.error_fname = error_fname
        self.info_fname = info_fname
        self.warning_fname = warning_fname

        self._date = datetime.now()
        self._filename = caller_infos.filename
        self._console_log_format = console_log_format
        self._file_log_format = file_log_format
        self._function = caller_infos.function
        self._lineno = caller_infos.lineno
        self._start_time = _time()

    def _format(self, levelname: str, message: str, lineno: int = None) -> dict:
        """
        returns a dict with custom entries

        :param levelname: str
            name of the level
            syntax: <levelname>
            example: "INFO"
        :param message: str
            message in the dict
            syntax: <message>
            example: "Test message"
        :param lineno: int
            line number in the dict
            syntax: <line number>
            example: 34
        :return: dict
            syntax: {"year": <year>,
                     "month": <month>,
                     "day": <day>,
                     "hour": <hour>,
                     "minute": <minute>,
                     "second": <second>,
                     "microsecond": <microsecond>,
                     "runtime": <runtime>,
                     "levelname": <level name>,
                     "filename": <filename>,
                     "lineno": <line number>,
                     "function": <function>,
                     "message": <message>}
            example: {"year": 2000,
                      "month": 1,
                      "day": 1,
                      "hour": 00,
                      "minute": 00,
                      "second": 00,
                      "microsecond": 00000,
                      "runtime": "01:23:45",
                      "levelname": "INFO",
                      "filename": "abc.py",
                      "lineno": 123,
                      "function": "test_function",
                      "message": "This is a test message"}

        :since: 0.1.0
        """
        if lineno:
            return {"year": self._date.year, "month": self._date.month, "day": self._date.day, "hour": self._date.hour, "minute": self._date.minute, "second": self._date.second, "microsecond": self._date.microsecond,
                    "runtime": self._runtime(), "levelname": levelname, "filename": self._filename, "lineno": lineno, "function": self._function, "message": message}
        else:
            return {"year": self._date.year, "month": self._date.month, "day": self._date.day, "hour": self._date.hour, "minute": self._date.minute, "second": self._date.second, "microsecond": self._date.microsecond,
                    "runtime": self._runtime(), "levelname": levelname, "filename": self._filename, "lineno": self._lineno, "function": self._function, "message": message}

    def _runtime(self) -> str:
        """
        returns the runtime

        :return: str
            returns the runtime
            syntax: <hour>:<minute>:<day>
            example: "01:23:45"

        :since: 0.1.0
        """
        second = int(_time() - self._start_time)
        minute = 0
        hour = 0
        while (second / 60) >= 1:
            minute += 1
            second -= 60

        while (minute / 60) >= 1:
            hour += 1
            minute -= 60

        if len(str(second)) == 1:
            second = "0" + str(second)

        if len(str(minute)) == 1:
            minute = "0" + str(minute)

        if len(str(hour)) == 1:
            hour = "0" + str(hour)

        return str(str(hour) + ":" + str(minute) + ":" + str(second))

    def critical(self, msg: str, lineno: int = None) -> None:
        """
        prints and write given format with 'critical' levelname and in 'msg' given message

        :param msg: str
            message you want to print and write
            syntax: <message>
            example: "critical message"
        :param lineno: int, optional
            custom 'lineno' (line number) entry
            syntax: <lineno>
            example: 5
        :return: None

        :since: 0.1.0
        """
        LogFile(self.log_fname, format=self._file_log_format).critical(msg, self._format("CRITICAL", msg, lineno=lineno))
        if self.critical_fname is not None:
            LogFile(self.critical_fname, format=self._file_log_format).critical(msg, self._format("CRITICAL", msg, lineno=lineno))
        LogConsole(self._console_log_format).critical(msg, self._format("CRITICAL", msg, lineno=lineno))

    def debug(self, msg: str, lineno: int = None) -> None:
        """
        prints and write given format with 'debug' levelname and in 'msg' given message

        :param msg: str
            message you want to print and write
            syntax: <message>
            example: "debug message"
        :param lineno: int, optional
            custom 'lineno' (line number) entry
            syntax: <lineno>
            example: 5
        :return: None

        :since: 0.1.0
        """
        LogFile(self.log_fname, format=self._file_log_format).debug(msg, self._format("DEBUG", msg, lineno=lineno))
        if self.debug_fname is not None:
            LogFile(self.debug_fname, format=self._file_log_format).debug(msg, self._format("DEBUG", msg, lineno=lineno))
        LogConsole(self._console_log_format).debug(msg, self._format("DEBUG", msg, lineno=lineno))

    def error(self, msg: str, lineno=None) -> None:
        """
        prints and write given format with 'error' levelname and in 'msg' given message

        :param msg: str
            message you want to print and write
            syntax: <message>
            example: "error message"
        :param lineno: int, optional
            custom 'lineno' (line number) entry
            syntax: <lineno>
            example: 5
        :return: None

        :since: 0.1.0
        """
        LogFile(self.log_fname, format=self._file_log_format).error(msg, self._format("ERROR", msg, lineno=lineno))
        if self.error_fname is not None:
            LogFile(self.error_fname, format=self._file_log_format).error(msg, self._format("ERROR", msg, lineno=lineno))
        LogConsole(self._console_log_format).error(msg, self._format("ERROR", msg, lineno=lineno))

    def info(self, msg: str, lineno=None) -> None:
        """
        prints and write given format with 'info' levelname and in 'msg' given message

        :param msg: str
            message you want to print and write
            syntax: <message>
            example: "info message"
        :param lineno: int, optional
            custom 'lineno' (line number) entry
            syntax: <lineno>
            example: 5
        :return: None

        :since: 0.1.0
        """
        LogFile(self.log_fname, format=self._file_log_format).info(msg, self._format("INFO", msg, lineno=lineno))
        if self.info_fname is not None:
            LogFile(self.log_fname, format=self._file_log_format).info(msg, self._format("INFO", msg, lineno=lineno))
        LogConsole(self._console_log_format).info(msg, self._format("INFO", msg, lineno=lineno))

    def warning(self, msg: str, lineno=None) -> None:
        """
        prints and write given format with 'warning' levelname and in 'msg' given message

        :param msg: str
            message you want to print and write
            syntax: <message>
            example: "warning message"
        :param lineno: int, optional
            custom 'lineno' (line number) entry
            syntax: <lineno>
            example: 5
        :return: None

        :since: 0.1.0
        """
        LogFile(self.log_fname, format=self._file_log_format).warning(msg, self._format("WARNING", msg, lineno=lineno))
        if self.warning_fname is not None:
            LogFile(self.warning_fname, format=self._file_log_format).warning(msg, self._format("WARNING", msg, lineno=lineno))
        LogConsole(self._console_log_format).warning(msg, self._format("WARNING", msg, lineno=lineno))


class LogConsole:
    """
    a simple logger for consoles

    :since: 0.1.0
    """

    def __init__(self, format: str = "[{runtime}] - {filename}(line: {lineno}) - {levelname}: {message}") -> None:
        """
        :param format: str, optional
            format of the console output
            syntax: <format>
            example: [{runtime}] - {filename}(line: {lineno}) - {levelname}: {message}
            NOTE: in 'format' you can use the following curly bracktes:
                year            gives the year back
                month           gives the month back
                day             gives the day back
                hour            gives the hour back
                minute          gives the minute back
                second          gives the second back
                microsecond     gives the microsecond back
                runtime         gives the back since the logger has started
                levelname       gives the levelname back
                filename        gives the name of the file from which the logger is called back
                lineno          gives the line number back from which the levelname function was called
                function        gives the function back from which the levelname function was called
                message         gives the in levelname function given message back
        :return: None

        :since: 0.1.0
        """
        from datetime import datetime
        from inspect import getframeinfo, stack

        self.format = format

        self._caller_infos = getframeinfo(stack()[1][0])
        self._date = datetime.now()
        self._start_time = _time()

    def _format(self, levelname: str, message: str) -> dict:
        """
        returns a dict with custom entries

        :param levelname: str
            name of the level
            syntax: <levelname>
            example: "INFO"
        :param message: str
            message in the dict
            syntax: <message>
            example: "Test message"
        :return: dict
            syntax: {"year": <year>,
                     "month": <month>,
                     "day": <day>,
                     "hour": <hour>,
                     "minute": <minute>,
                     "second": <second>,
                     "microsecond": <microsecond>,
                     "runtime": <runtime>,
                     "levelname": <level name>,
                     "filename": <filename>,
                     "lineno": <line number>,
                     "function": <function>,
                     "message": <message>}
            example: {"year": 2000,
                      "month": 1,
                      "day": 1,
                      "hour": 00,
                      "minute": 00,
                      "second": 00,
                      "microsecond": 00000,
                      "runtime": "01:23:45",
                      "levelname": "INFO",
                      "filename": "abc.py",
                      "lineno": 123,
                      "function": "test_function",
                      "message": "This is a test message"}

        :since: 0.1.0
        """
        return {"year": self._date.year, "month": self._date.month, "day": self._date.day, "hour": self._date.hour, "minute": self._date.minute, "second": self._date.second, "microsecond": self._date.microsecond,
                "runtime": self._runtime(), "levelname": levelname, "filename": self._caller_infos.filename, "lineno": self._caller_infos.lineno, "function": self._caller_infos.function, "message": message}

    def _runtime(self) -> str:
        """
        returns the runtime

        :return: str
            returns the runtime
            syntax: <hour>:<minute>:<day>
            example: "01:23:45"

        :since: 0.1.0
        """
        second = int(_time() - self._start_time)
        minute = 0
        hour = 0
        while (second / 60) >= 1:
            minute += 1
            second -= 60

        while (minute / 60) >= 1:
            hour += 1
            minute -= 60

        if len(str(second)) == 1:
            second = "0" + str(second)

        if len(str(minute)) == 1:
            minute = "0" + str(minute)

        if len(str(hour)) == 1:
            hour = "0" + str(hour)

        return str(str(hour) + ":" + str(minute) + ":" + str(second))

    def critical(self, msg: str, _format_values: dict = None) -> None:
        """
        prints given format with 'critical' levelname and in 'msg' given message

        :param msg: str
            message you want to print out
            syntax: <message>
            example: "critical message"
        :param _format_values: dict, optional
            dictionary with own format values
            syntax: {<key>: <value>}
            example: {"mytext": "This is my text"}
            NOTE: if you use '_format_values' the in function '_format' given format values won't used
        :return: None

        :since: 0.1.0
        """
        if _format_values is None:
            print(self.format.format(**self._format(levelname="CRITICAL", message=msg)))
        else:
            print(self.format.format(**_format_values))

    def debug(self, msg: str, _format_values: dict = None) -> None:
        """
        prints given format with 'debug' levelname and in 'msg' given message

        :param msg: str
            message you want to print out
            syntax: <message>
            example: "debug message"
        :param _format_values: dict, optional
            dictionary with own format values
            syntax: {<key>: <value>}
            example: {"mytext": "This is my text"}
            NOTE: if you use '_format_values' the in function '_format' given format values won't used
        :return: None

        :since: 0.1.0
        """
        if _format_values is None:
            print(self.format.format(**self._format(levelname="DEBUG", message=msg)))
        else:
            print(self.format.format(**_format_values))

    def error(self, msg: str, _format_values: dict = None) -> None:
        """
        prints given format with 'error' levelname and in 'msg' given message

        :param msg: str
            message you want to print out
            syntax: <message>
            example: "error message"
        :param _format_values: dict, optional
            dictionary with own format values
            syntax: {<key>: <value>}
            example: {"mytext": "This is my text"}
            NOTE: if you use '_format_values' the in function '_format' given format values won't used
        :return: None

        :since: 0.1.0
        """
        if _format_values is None:
            print(self.format.format(**self._format(levelname="ERROR", message=msg)))
        else:
            print(self.format.format(**_format_values))

    def info(self, msg: str, _format_values: dict = None) -> None:
        """
        prints given format with 'info' levelname and in 'msg' given message

        :param msg: str
            message you want to print out
            syntax: <message>
            example: "info message"
        :param _format_values: dict, optional
            dictionary with own format values
            syntax: {<key>: <value>}
            example: {"mytext": "This is my text"}
            NOTE: if you use '_format_values' the in function '_format' given format values won't used
        :return: None

        :since: 0.1.0
        """
        if _format_values is None:
            print(self.format.format(**self._format(levelname="INFO", message=msg)))
        else:
            print(self.format.format(**_format_values))

    def warning(self, msg: str, _format_values: dict = None) -> None:
        """
        prints given format with 'warning' levelname and in 'msg' given message

        :param msg: str
            message you want to print out
            syntax: <message>
            example: "warning message"
        :param _format_values: dict, optional
            dictionary with own format values
            syntax: {<key>: <value>}
            example: {"mytext": "This is my text"}
            NOTE: if you use '_format_values' the in function '_format' given format values won't used
        :return: None

        :since: 0.1.0
        """
        if _format_values is None:
            print(self.format.format(**self._format(levelname="WARNING", message=msg)))
        else:
            print(self.format.format(**_format_values))


class LogFile:
    """
    a simple logger for files

    :since: 0.1.0
    """

    def __init__(self, log_fname: str, mode: str = "a", format: str = "[{year}-{month}-{day} {hour}:{minute}:{second}] - {filename}(line: {lineno}) - {levelname}: {message}") -> None:
        """
        :param log_fname: str
            filename of the file to which the logging messages should be saved
            syntax: <fname>
            example: "/home/pi/test.log"
        :param mode: str, optional
            mode to write on file
            syntax: <mode>
            example: "a"
        :param format: str, optional
            format of the output that should be write to file
            syntax: <format>
            example: [{runtime}] - {filename}(line: {lineno}) - {levelname}: {message}
            NOTE: in 'format' you can use the following curly bracktes:
                year            gives the year back
                month           gives the month back
                day             gives the day back
                hour            gives the hour back
                minute          gives the minute back
                second          gives the second back
                microsecond     gives the microsecond back
                runtime         gives the back since the logger has started
                levelname       gives the levelname back
                filename        gives the name of the file from which the logger is called back
                lineno          gives the line number back from which the levelname function was called
                function        gives the function back from which the levelname function was called
                message         gives the in levelname function given message back
        :return: None

        :since: 0.1.0
        """
        from datetime import datetime
        from inspect import getframeinfo, stack

        self.format = format
        self.log_fname = log_fname
        self.mode = mode

        self._caller_infos = getframeinfo(stack()[1][0])
        self._date = datetime.now()
        self._start_time = _time()

    def _format(self, levelname: str, message: str) -> dict:
        """
        returns a dict with custom entries

        :param levelname: str
            name of the level
            syntax: <levelname>
            example: "INFO"
        :param message: str
            message in the dict
            syntax: <message>
            example: "Test message"

        :return: dict
            syntax: {"year": <year>,
                     "month": <month>,
                     "day": <day>,
                     "hour": <hour>,
                     "minute": <minute>,
                     "second": <second>,
                     "microsecond": <microsecond>,
                     "runtime": <runtime>,
                     "levelname": <level name>,
                     "filename": <filename>,
                     "lineno": <line number>,
                     "function": <function>,
                     "message": <message>}
            example: {"year": 2000,
                      "month": 1,
                      "day": 1,
                      "hour": 00,
                      "minute": 00,
                      "second": 00,
                      "microsecond": 00000,
                      "runtime": "01:23:45",
                      "levelname": "INFO",
                      "filename": "abc.py",
                      "lineno": 123,
                      "function": "test_function",
                      "message": "This is a test message"}

        :since: 0.1.0
        """
        return {"year": self._date.year, "month": self._date.month, "day": self._date.day, "hour": self._date.hour, "minute": self._date.minute, "second": self._date.second, "microsecond": self._date.microsecond,
                "runtime": self._runtime(), "levelname": levelname, "filename": self._caller_infos.filename, "lineno": self._caller_infos.lineno, "function": self._caller_infos.function, "message": message}

    def _runtime(self) -> str:
        """
        returns the runtime

        :return: str
            returns the runtime
            syntax: <hour>:<minute>:<day>
            example: "01:23:45"

        :since: 0.1.0
        """
        second = int(_time() - self._start_time)
        minute = 0
        hour = 0
        while (second / 60) >= 1:
            minute += 1
            second -= 60

        while (minute / 60) >= 1:
            hour += 1
            minute -= 60

        if len(str(second)) == 1:
            second = "0" + str(second)

        if len(str(minute)) == 1:
            minute = "0" + str(minute)

        if len(str(hour)) == 1:
            hour = "0" + str(hour)

        return str(str(hour) + ":" + str(minute) + ":" + str(second))

    def _write(self, msg: str) -> None:
        """
        writes the given message to the log file

        :param msg: str
            message that should be write to the file
            syntax: <message>
            example: "Test message"
        :return: None

        :since: 0.1.0
        """
        with open(self.log_fname, self.mode) as file:
            file.write(msg + "\n")
            file.close()

    def critical(self, msg: str, _format_values: dict = None) -> None:
        """
        writes given format with 'critical' levelname and in 'msg' given message to file

        :param msg: str
            message you want to write to file
            syntax: <message>
            example: "critical message"
        :param _format_values: dict, optional
            dictionary with own format values
            syntax: {<key>: <value>}
            example: {"mytext": "This is my text"}
            NOTE: if you use '_format_values' the in function '_format' given format values won't used
        :return: None

        :since: 0.1.0
        """
        if _format_values is None:
            self._write(self.format.format(**self._format(levelname="CRITICAL", message=msg)))
        else:
            self._write(self.format.format(**_format_values))

    def debug(self, msg: str, _format_values: dict = None) -> None:
        """
        writes given format with 'debug' levelname and in 'msg' given message to file

        :param msg: str
            message you want to write to file
            syntax: <message>
            example: "debug message"
        :param _format_values: dict, optional
            dictionary with own format values
            syntax: {<key>: <value>}
            example: {"mytext": "This is my text"}
            NOTE: if you use '_format_values' the in function '_format' given format values won't used
        :return: None

        :since: 0.1.0
        """
        if _format_values is None:
            self._write(self.format.format(**self._format(levelname="DEBUG", message=msg)))
        else:
            self._write(self.format.format(**_format_values))

    def error(self, msg: str, _format_values: dict = None) -> None:
        """
        writes given format with 'debug' levelname and in 'msg' given message to file

        :param msg: str
            message you want to write to file
            syntax: <message>
            example: "debug message"
        :param _format_values: dict, optional
            dictionary with own format values
            syntax: {<key>: <value>}
            example: {"mytext": "This is my text"}
            NOTE: if you use '_format_values' the in function '_format' given format values won't used
        :return: None

        :since: 0.1.0
        """
        if _format_values is None:
            self._write(self.format.format(**self._format(levelname="ERROR", message=msg)))
        else:
            self._write(self.format.format(**_format_values))

    def info(self, msg: str, _format_values: dict = None) -> None:
        """
        writes given format with 'info' levelname and in 'msg' given message to file

        :param msg: str
            message you want to write to file
            syntax: <message>
            example: "info message"
        :param _format_values: dict, optional
            dictionary with own format values
            syntax: {<key>: <value>}
            example: {"mytext": "This is my text"}
            NOTE: if you use '_format_values' the in function '_format' given format values won't used
        :return: None

        :since: 0.1.0
        """
        if _format_values is None:
            self._write(self.format.format(**self._format(levelname="INFO", message=msg)))
        else:
            self._write(self.format.format(**_format_values))

    def warning(self, msg: str, _format_values: dict = None) -> None:
        """
        writes given format with 'warning' levelname and in 'msg' given message to file

        :param msg: str
            message you want to write to file
            syntax: <message>
            example: "warning message"
        :param _format_values: dict, optional
            dictionary with own format values
            syntax: {<key>: <value>}
            example: {"mytext": "This is my text"}
            NOTE: if you use '_format_values' the in function '_format' given format values won't used
        :return: None

        :since: 0.1.0
        """
        if _format_values is None:
            self._write(self.format.format(**self._format(levelname="WARNING", message=msg)))
        else:
            self._write(self.format.format(**_format_values))
