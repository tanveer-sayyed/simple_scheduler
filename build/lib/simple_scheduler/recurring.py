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
        function : a callable function
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
                sleep(s - time())
                p = Process(target = function)
                p.start()
                self._workers.append(p)
                self._print(f"{ctime(time())} :: {function.__qualname__}"+\
                            f" [recurring | {period_in_seconds}-second(s)]")
            except Exception as e:
                self._print(str(e))
                [p.terminate for p in self._workers]
                self._workers = []
                pass

    def add_job(self, target, period_in_seconds, args=(), kwargs={}):
        """
        Assigns an periodic task to a process.

        Parameters
        ----------
        target : a callable function
        period_in_seconds : int
            the time period in seconds to execute this function
        args : tuple(object,), optional
            un-named argumets for the "target" callable
            the default is ()
        kwargs : dict{key:object}, optional
            named argumets for the "target" callable
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
