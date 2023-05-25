from loguru import logger


class BaseProjectExceptions(Exception):
    """Исключения относящие к проекту"""
    pass


class WrongQueryException(BaseProjectExceptions):
    """Говорит о неправильном запросе в Базу Данных"""

    message: str = 'Wrong Query To Database'

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        super().__init__(logger.error(self.message))


class NotImplementedMethod(BaseProjectExceptions):
    """
    Говорит о нереализованом методе типа который наследуется от базового
    класса
    """

    message: str = 'Not Implemented Method Of Type'

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        super().__init__(logger.error(self.message))


class WrongTypeArgument:
    """Говорит о неправильном типе аргумента"""

    message: str = 'Wrong Type Of Argument'

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        super().__init__(logger.error(self.message))
