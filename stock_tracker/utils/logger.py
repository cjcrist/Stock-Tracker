# logger.py

import logging


class Logger:
    def __init__(self, logger):
        self._LOGGER = logging.getLogger(logger)
        self._loggers = []

    def set_loggers(self, loggers) -> None:
        """
        Sets sub logger handlers
        :param loggers: list of loggers to use
        """
        self._loggers = [log_name for log_name in loggers]

    def debug(self, message):
        return self._LOGGER.debug(message)

    def info(self, message):
        return self._LOGGER.info(message)

    def error(self, message):
        return self._LOGGER.error(message)

    def setup_logging(self, debug=False, verbose=False) -> None:
        """
        Setup logging
        :param debug: Toggle debug logging output (default: False)
        :param verbose: Toggle request library logging output (default: False)
        """
        level = logging.DEBUG if debug else logging.INFO
        log_handler = logging.StreamHandler()
        logfmt = '%(levelname)s %(name)s: %(message)s' if not debug else \
                 '%(levelname)s %(asctime)s %(name)s: %(message)s'
        formatter = logging.Formatter(fmt=logfmt, datefmt='%Y-%m-%dT%H:%M:%S')
        log_handler.setFormatter(formatter)
        self._LOGGER.addHandler(log_handler)
        self._LOGGER.setLevel(level)
        self._LOGGER.propagate = False

        # Determine other loggers to use
        if verbose:
            for k, v in logging.Logger.manager.loggerDict.items():
                if k not in self._loggers:
                    self._loggers.append(k)

        # Add in logging from libraries
        for log_name in self._loggers:
            logger = logging.getLogger(log_name)
            logger.addHandler(log_handler)
            logger.setLevel(level)
            logger.propagate = False
