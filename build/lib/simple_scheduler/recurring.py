from multiprocessing import Process
from time import sleep, time, ctime

from simple_scheduler.base import Schedule

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
recurring_scheduler = Recurring(verbose=True)

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