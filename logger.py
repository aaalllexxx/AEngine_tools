import datetime
from rich import print

from aecf_reader import Config
from banner_string import BannerString


def _get_key(key, options):
    keys = [key.lower() for key in list(options)]
    if key in keys:
        key = list(options)[keys.index(key)]
        return options.get(key)
    else:
        return None


class Logger:
    options = {}

    @classmethod
    def log(cls, message, *postmessages, **kwargs):
        if _get_key("show_time", cls.options) is not False:
            message = f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] " \
                      f"{message}{' | ' if postmessages else ''}" \
                      f"{' | '.join(postmessages)}"
        else:
            message = f"{message}{' | ' if postmessages else ''}" \
                      f"{' | '.join(postmessages)}"

        print(message)

    @classmethod
    def set_options(cls, options):
        cls.options = options

    @classmethod
    def append_options(cls, options):
        for k, v in options.items():
            cls.options[k] = v


class FileLogger(Logger):
    options = Logger.options

    def __init__(self, file_path=None, encoding="utf-8"):
        if _get_key("path", self.options) is None:
            self.path = file_path
        else:
            self.path = _get_key("path", self.options)
        self.encoding = encoding

    def __add(self, message, path):
        with open(path, "a", encoding=self.encoding) as file:
            file.write(message + "\n")

    def log(self, message, *postmessages, **kwargs):
        if _get_key("show_time", self.options) is not False:
            message = f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] " \
                      f"{message}{' | ' if postmessages else ''}" \
                      f"{' | '.join(postmessages)}"
        self.__add(message, self.path)


class PrettyLogger(Logger):
    @classmethod
    def log(cls, message, *postmessages, **kwargs):
        color = kwargs.get("color") or "red"
        text = f"{message}{' | ' if postmessages else ''}{' | '.join(postmessages)}"
        length = max([len(i) for i in text.split("\n")])
        text = text.replace('\n', '\n ')
        error = BannerString([
            f"[{color}]",
            "*" + "-" * length + "*",
            f" {text}",
            "*" + "-" * length + "*",
            f"[/{color}]"
        ])
        Logger.log(error)


class Debug(Logger):
    @classmethod
    def log(cls, message, *postmessages, **kwargs):
        debug = _get_key("debug", cls.options)
        if debug or debug is None:
            Logger.log(message)
