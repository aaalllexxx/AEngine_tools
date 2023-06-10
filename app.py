import time
import Debug

from Debug import Time, Info, Program
from exceptions import FileExtensionError
import psutil


class App:
    __running = True
    __deltas = 0
    debug = True

    def __on_awake(self):
        if self.debug:
            self.__program_start = time.time()

    def __on_exit(self):
        if self.debug:
            Time.program_time = time.time() - self.__program_start

    def __pre_update(self):
        if self.debug:
            Info.cpu = {
                "percent": psutil.cpu_percent(),
                "freq": psutil.cpu_freq(),
                "times": psutil.cpu_times()
            }
            Info.memory = dict(psutil.virtual_memory()._asdict())
            self.__start_time = time.time()

    def __post_update(self):
        if self.debug:
            Time.delta = time.time() - self.__start_time
            if Time.delta > Time.longest_delta:
                Time.longest_delta = Time.delta
            self.__deltas += Time.delta
            Program.loops += 1
            Time.average_delta = self.__deltas / Program.loops
            Time.program_time = time.time() - self.__program_start

    def start(self):
        pass

    def update(self):
        pass

    def finish(self):
        pass

    def run(self):
        self.__on_awake()
        self.start()
        self.__pre_update()
        self.update()
        self.__post_update()
        self.finish()
        self.__on_exit()

    def stop(self):
        self.__running = False

    def loop(self):
        self.__on_awake()
        self.start()
        while self.__running:
            self.__pre_update()
            self.update()
            self.__post_update()
        self.finish()
        self.__on_exit()