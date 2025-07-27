import logging
import json


def debug(obj):
    """
    Print a JSON representation of the given object to the console, at debug level.
    """
    if logging.getLogger().level == logging.DEBUG:
        print(json.dumps(obj, indent=2, default=str))


def info(obj):
    """
    Print a JSON representation of the given object to the console, at info level.
    """
    if logging.getLogger().level <= logging.INFO:
        print(json.dumps(obj, indent=2, default=str))


def warn(obj):
    """
    Print a JSON representation of the given object to the console, at warn level.
    """
    if logging.getLogger().level <= logging.WARNING:
        print(json.dumps(obj, indent=2, default=str))


def error(obj):
    """
    Print a JSON representation of the given object to the console, at error level.
    """
    print(json.dumps(obj, indent=2, default=str))
