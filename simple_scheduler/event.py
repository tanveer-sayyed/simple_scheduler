from pytz import timezone
from time import time, ctime
from datetime import datetime
from multiprocess import Process

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
            HH_MM = str(datetime.now(timezone(tz)).time()).rsplit(":",1)[0]
            day = self._days[datetime.today().weekday()]
            if (f"{day}|{HH_MM}" in when) | (f"*|{HH_MM}" in when):
                self._print(f"{ctime(time())} :: {function.func.__qualname__}" +\
                            f" [event @{day}|{HH_MM}|{tz}]")
                for tries in range(3): # number of attempts for any job
                    try:
                        function()
                        self._sleep(period_in_seconds=60)
                        break
                    except Exception as e:
                        self._print(str(e))
                        self._sleep(period_in_seconds=10)
                        continue
            else:
                self._sleep(period_in_seconds=55)

    def add_job(self, target, tz, when, args=(), kwargs={}):
        """
        Assigns an event to a process.

        Parameters
        ----------
        target : a callable function
        tz : str
            time zone (call the method .timezones() for more info)
        when : list, a collection of "day|HH:MM"
            at what precise time(s) should the function be called
            eg. ["mon|22:04","sat|03:45", ...] please "only" use 24-hour
                                               clock with "|" as day separator
                                               and ":" as time separator
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
            eg. ["tue|12:30am","thu|2:30 pm", ...] please "only" use 24-hour
                                                   clock, with "|" as day
                                                   separator and ":" as time
                                                   separator

        Returns
        -------
        None.

        """
        function = self._manifest_function(target, args, kwargs)
        when = [w.lower() for w in when]
        try:
            [int(x.split(":")[0].split("|")[1]) for x in when]
            [int(x.split(":")[1]) for x in when]
        except:
            raise Exception('Elements of "when" (list) must be a collection' +\
                            'of ["day|HH:MM", "day|HH:MM", ...]')
        self._processes.append(Process(target=self._schedule,
                                       name = function.func.__qualname__,
                                       args=(function, tz, when)))

event_scheduler = Event(verbose=True)