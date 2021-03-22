from sqlite3 import Error


class InsufficientConfigurationError(Error):
    def __init__(self, message, err):
        self.message = message
        self.err = err


class SQLiteConnectionError(Error):
    def __init__(self, message, err):
        self.message = message
        self.err = err


class QueryExecutionError(Error):
    def __init__(self, message, err):
        self.message = message
        self.err = err
