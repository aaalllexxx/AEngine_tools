import os
from ast import literal_eval

from exceptions import FileExtensionError


class Config:
    def __init__(self, path, encoding="utf-8"):
        extension = path.split(".")[-1].lower()
        if extension != "aecf":
            FileExtensionError(f"'.aecf' extension required, got '.{extension}'").send()
        self.load(path, encoding)

    def load(self, path, encoding):
        with open(path, "r", encoding=encoding) as file:
            data = file.read()
        self.from_string(data)

    def from_string(self, string):
        rules = {
            "int": int,
            "str": str,
            "auto": literal_eval
        }

        data = string.split("\n")
        for row in data:
            row_data = [i.strip() for i in row.split("=")]
            if len(row_data) > 2:
                second_data = row_data[1:]
                row_data = row_data[0]
                row_data.append("=".join(second_data))
            if ":" in row_data[1]:
                data_type = row_data[1].split(":")[1].strip()
                if data_type in list(rules):
                    try:
                        self.__dict__[row_data[0]] = rules[data_type](row_data[1].split(":")[0].strip())
                    except ValueError:
                        self.__dict__[row_data[0]] = row_data[1].split(":")[0].strip()
                else:
                    try:
                        self.__dict__[row_data[0]] = literal_eval(row_data[1].split(":")[0].strip())
                    except ValueError:
                        self.__dict__[row_data[0]] = row_data[1].split(":")[0].strip()
            else:
                try:
                    self.__dict__[row_data[0]] = literal_eval(row_data[1])
                except ValueError:
                    self.__dict__[row_data[0]] = row_data[1]

    def items(self):
        return self.__dict__.items()
