from pytz import timezone
from datetime import datetime
from functools import partial
from time import sleep, time, ctime
from multiprocessing import Process

class schedule():
    """ The parent of "event" and "recurring" classes."""
    
    def __init__(self, verbose = False):
        self._processes = []
        self._workers = []
        self.verbose = verbose

    def _print(self, message):
        if self.verbose:
            print(message)

    def run_events(self):
        try:
            if self._processes:
                [process.start() for process in self._processes]
        except:
            [process.terminate for process in self._processes]
            pass

    def _manifest_function(self, function_with_parameters):
        try:        
            qualname = function_with_parameters[0].__qualname__
            function = partial(*function_with_parameters)
            function.__qualname__ = qualname
            return function
        except:
            raise """add_event/add_recurring attribute not properly called.
            See docs."""

class event(schedule):
    """ Event occurs at an exact time.
        (e.g. @13:57 hrs call scirpt_1)
        Each event is tried thrice, with 10 sec interval."""

    def __init__(self):
        super().__init__()

    def _schedule(self, function, tz, hour, minute):
        """
        Parameters
        ----------
        function : callable function
            name of the function which needs to be scheduled
        tz : str
            timezone
        hour : int
            hour of the time to be scheduled
        minute : int
            minute of the time to be scheduled
        Returns
        -------
        None.
        """
        while True:
            hour_ = int(datetime.now(timezone(tz)).time().hour)
            minute_ = int(datetime.now(timezone(tz)).time().minute)
            self._print(f"{ctime(time())} :: {function.__qualname__}" +\
                        f" [event @{hour}:{minute} | {tz} time]")
            if (hour_ == hour) & (minute_ == minute):
                for tries in range(3): # number of attempts for any job
                    self._print(f"Executing -- {function.__qualname__}")
                    try:
                        function()
                        sleep(60)
                        break
                    except Exception as e:
                        self._print(str(e))
                        sleep(10)
                        continue
            else:
                sleep(55)

    def add_event(self, function, tz, when):
        function = self._manifest_function(function)
        self._processes.append(Process(target=self._schedule,
                                      args=(function, tz, hour, minute)))

class recurring(schedule):
    """ Recurring tasks are those that occur after every "x"-seconds.
        (e.g. script_1 is called every 600 seconds)"""

    def __init__(self):
        super().__init__()

    def _schedule(self, function, period_in_seconds):
        """
        Parameters
        ----------
        function : callable function
            name of the function which needs to be scheduled
        period_in_seconds : int
            the time period in seconds

        Returns
        -------
        None.

        """
        while True:
            try:
                s = time() + period_in_seconds
                for x in self._workers:
                    if not x.is_alive():
                        x.join()
                        self._workers.remove(x)
                sleep(round(s - time()))
                p = Process(target = function)
                p.start()
                self._workers.append(p)
                self._print(f"{ctime(time())} :: {function.__qualname__}"+\
                            "[recurring]")
            except Exception as e:
                self._print(str(e))
                [p.terminate for p in self._workers]
                self._workers = []
                pass

    def add_recurring(self, function, period_in_seconds):
        function = self._manifest_function(function)
        self._processes.append(Process(target=self._schedule,
                                      args=(function, period_in_seconds)))

def call_me(a=1, b=2):
    print(a, b)

event_scheduler = event()
event_scheduler.verbose = True
event_scheduler.add_event((call_me, 5, 6), "Asia/Kolkata",
                          when=["11:34","11:40"])

recurring_scheduler = recurring()
