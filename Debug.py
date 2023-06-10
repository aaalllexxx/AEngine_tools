import json


class Time:
    average_delta = 0
    delta = 0
    program_time = 0
    longest_delta = 0


class Program:
    loops = 0
    errors = 0


class Info:
    cpu = 0
    memory = 0


def export_all(path, encoding="utf-8"):
    json_data = {
        "time_metrics": {
            "program_time": Time.program_time,
            "average_delta": Time.average_delta,
            "longest_delta": Time.longest_delta
        },
        "system_metrics": {
            "cpu": Info.cpu,
            "memory": Info.memory
        },
        "program_metrics": {
            "loops_count": Program.loops,
            "errors_count": Program.errors
        }
    }

    with open(path, "w", encoding=encoding) as file:
        file.write(json.dumps(json_data, indent=4))
