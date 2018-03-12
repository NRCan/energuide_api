import logging
import typing

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s: %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S%z')


def unwrap_exception_message(exc: typing.Type[Exception], join: str = ' - ') -> str:
    if exc.__context__:
        if exc.args:
            return f'{exc}{join}{unwrap_exception_message(exc.__context__)}'
        else:
            return f'{unwrap_exception_message(exc.__context__)}'
    else:
        return f'{exc}'


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
