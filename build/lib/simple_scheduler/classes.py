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
            if (hour_ == hour) & (minute_ == minute):
                self._print(f"{ctime(time())} :: {function.__qualname__}" +\
                            f" [event @{hour}:{minute} | {tz} time]")
                print()
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

    def add_event(self, target, tz, when, args=(), kwargs={}):
        """
        Assigns an event to a process.

        Parameters
        ----------
        target : a callable function
        tz : str
            time zone (call the method .timezones() for more info)
        when : list(str)
            at what precise time(s) should the function be called
            eg. ["12:34","23:45", ...] --> please "only" use 24-hour clock
        args : tuple(object,), optional
            un-named argumets for the "target" function
            the default is ()
        kwargs : dict{key:object}, optional
            named argumets for the "target" function
            the default is {}

        Raises
        ------
        Exception
            - If time (in "when"-list) is not a collection of "int:int"
            eg. ["12:30am","2:30 pm", ...] --> please "only" use 24-hour clock

        Returns
        -------
        None.

        """
        function = self._manifest_function(target, args, kwargs)
        for hour_minute in when:
            try:
                hour = int(hour_minute.split(":")[0])
                minute = int(hour_minute.split(":")[1])
            except ValueError:
                self._processes = []
                raise Exception('Elements of "when" (list) must be ' +\
                                '["int:int", "int:int", ...]')
            self._processes.append(Process(target=self._schedule,
                                           name = function.__qualname__,
                                           args=(function, tz, hour, minute)))

class Recurring(Schedule):
    """ Recurring tasks are those that occur after every "x"-seconds.
        (e.g. script_1 is called every 600 seconds)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _schedule(self, function, period_in_seconds):
        """
        Parameters
        ----------
        function : callable function{ctime(time())}
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

    def add_recurring(self, target, period_in_seconds, args=(), kwargs={}):
        """
        Assigns an periodic task to a process.

        Parameters
        ----------
        target : a callable function
        period_in_seconds : int
            the time period in seconds to execute this function
        args : tuple(object,), optional
            un-named argumets for the "target" function
            the default is ()
        kwargs : dict{key:object}, optional
            named argumets for the "target" function
            the default is {}

        Returns
        -------
        None.

        """
        function = self._manifest_function(target, args, kwargs)
        self._processes.append(Process(target=self._schedule,
                                       name = function.__qualname__,
                                       args=(function, period_in_seconds)))

# def call_me(f, z="ZZZZZZZZ", *args, **kwargs):
#     print(f ,z, args, kwargs)
    
# def f():
#     print("....")
    
# # correct function definition
# def my_function(a, b, *args, **kwargs):
#     pass

# event_scheduler = Event(verbose=True)


# # event_scheduler.add_event(function_with_parameters=(call_me, 5, 6),
# #                             tz="Asia/Kolkata",
# #                             when=["12:49","aa:48"])
# # print(event_scheduler.add_event.__doc__)
# # event_scheduler.run()

# recurring_scheduler = Recurring(True)
# recurring_scheduler.verbose = False
# recurring_scheduler.add_recurring(target = call_me,
#                                   kwargs={"f":"FFFF", "b":"BBBB"},
#                                   period_in_seconds=1)
# recurring_scheduler.add_recurring(target = call_me,
#                                   args=("FFFF",),
#                                   period_in_seconds=1)
# recurring_scheduler.add_recurring(target = call_me,
#                                   args=("FFFF","ZZZZ"),
#                                   kwargs={"b":"BBBB"},
#                                   period_in_seconds=1)
# recurring_scheduler.add_recurring(target = call_me,
#                                   args=("FFFF","ZZZZ","NNNNNN"),
#                                   kwargs={"b":"BBBB"},
#                                   period_in_seconds=1)
# recurring_scheduler.add_recurring(target = f,
#                                   period_in_seconds=1,
#                                   )
# recurring_scheduler.add_recurring(target = call_me,
#                                   period_in_seconds=3,
#                                   kwargs={"b":3, "z":"AAAA"},
#                                   args=(1,2,3,4,5))

# recurring_scheduler.run()


# # TypeError: call_me() got multiple values for argument 'b'
# # Wed Mar 17 11:57:39 2021 :: call_me[recurring]
# # Process Process-1:46:
# # Traceback (most recent call last):
# #   File "/usr/lib/python3.6/multiprocessing/process.py", line 258, in _bootstrap
# #     self.run()
# #   File "/usr/lib/python3.6/multiprocessing/process.py", line 93, in run
# #     self._target(*self._args, **self._kwargs)
# # TypeError: call_me() got multiple values for argument 'b'
# # Wed Mar 17 11:57:40 2021 :: call_me[recurring]
# # Process Process-1:47:
# # Traceback (most recent call last):
# #   File "/usr/lib/python3.6/multiprocessing/process.py", line 258, in _bootstrap
# #     self.run()
# #   File "/usr/lib/python3.6/multiprocessing/process.py", line 93, in run
# #     self._target(*self._args, **self._kwargs)
# # TypeError: call_me() got multiple values for argument 'b'