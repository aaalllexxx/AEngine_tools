from rich import print
from Debug import Program


class AEngineError:
    __description__ = "Default AEngine Error"
    exit_code = -1
    message = "Default AEngine Error"
    data = []

    def __init__(self, *data):
        self.data = data
        Program.errors += 1

    def __str__(self):
        classname = str(str(type(self)).split(self.__module__)[1][1:].split("\'")[0])
        return f"{classname}: {self.message}{', error data is `' if self.data else ''}{', '.join(self.data)}`"

    def send(self):
        print(f"[red]{self}[/red]")
        raise SystemError(self.exit_code)

    def catch(self):
        print(f"[red]{self}[/red]")


class FileExtensionError(AEngineError):
    __description__ = "Ошибка возникает в том случае, когда передан файл с неподходящим расширением"
    exit_code = 12_001
    message = "Invalid file extension"
