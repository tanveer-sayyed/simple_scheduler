from pytz import timezone
from datetime import datetime
from multiprocessing import Process
from time import sleep, time, ctime

from simple_scheduler.base import Schedule

class Event(Schedule):
    """ Event occurs at an exact time.
        e.g. scirpt_1 is called at 14:00 and 20:00
        Each event is tried 3-times (but executed only once)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _schedule(self, function, tz, when):
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
            hour = int(datetime.now(timezone(tz)).time().hour)
            minute = int(datetime.now(timezone(tz)).time().minute)
            print(f"{hour}:{minute}", when)
            if f"{hour}:{minute}" in when:
            # if (hour_ == hour) & (minute_ == minute):
                self._print(f"{ctime(time())} :: {function.__qualname__}" +\
                            f" [event @{hour}:{minute} | {tz}]")
                for tries in range(3): # number of attempts for any job
                    try:
                        function()
                        sleep(60) # prevent re-execution of small jobs
                        break
                    except Exception as e:
                        self._print(str(e))
                        sleep(10)
                        continue
            else:
                sleep(55)

    def add_job(self, target, tz, when, args=(), kwargs={}):
        """
        Assigns an event to a process.

        Parameters
        ----------
        target : a callable function
        tz : str
            time zone (call the method .timezones() for more info)
        when : list(str)
            at what precise time(s) should the function be called
            eg. ["12:34","23:45", ...] --> please "only" use 24-hour clock,
                                           with ":" as separator
        args : tuple(object,), optional
            un-named argumets for the "target" callable
            the default is ()
        kwargs : dict{key:object}, optional
            named argumets for the "target" callable
            the default is {}

        Raises
        ------
        Exception
            - If time (in "when"-list) is not a collection of "int:int"
            eg. ["12:30am","2:30 pm", ...] --> please "only" use 24-hour clock,
                                               with ":" as separator

        Returns
        -------
        None.

        """
        function = self._manifest_function(target, args, kwargs)
        try:
            [int(x.split(":")[0]) for x in when]
            [int(x.split(":")[1]) for x in when]
        except ValueError:
            raise Exception('Elements of "when" (list) must be ' +\
                            '["int:int", "int:int", ...]')
        print("step 1")
        print(function, tz, when)
        self._processes.append(Process(target=self._schedule,
                                       name = function.__qualname__,
                                       args=(function, tz, when)))

event_scheduler = Event(verbose=True)