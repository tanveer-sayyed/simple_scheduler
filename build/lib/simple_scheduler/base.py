from time import time, sleep
from functools import partial
from pytz import all_timezones

class Schedule():
    """ The parent of "event" and "recurring" classes."""

    def __init__(self, verbose=False):
        self._processes = []
        self._workers = []
        self.verbose = verbose
        self._days = {0:"mon",
               1:"tue",
               2:"wed",
               3:"thu",
               4:"fri",
               5:"sat",
               6:"sun"}

    def timezones(self):
        """
        A quick look-up of different time-zones.

        Returns
        -------
        all_timezones : list
            pytz.all_timezones

        """
        return all_timezones

    def _print(self, message):
        """
        To silence, this class, if need be.

        Parameters
        ----------
        message : str
            description

        Returns
        -------
        None.

        """
        if self.verbose:
            print(); print(message)

    def _sleep(self, period_in_seconds):
        """
        Resourceful sleep

        Parameters
        ----------
        period_in_seconds : int

        Returns
        -------
        None.

        """
        s = time() + period_in_seconds
        for x in self._workers:
            if not x.is_alive():
                x.join()
                self._workers.remove(x)
        sleep(s - time())

    def run(self):
        """
        Spawns tasks simultaneously.

        Returns
        -------
        None.

        """
        try:
            if self._processes:
                [process.start() for process in self._processes]
        except:
            self.stop()
            pass

    def _manifest_function(self, target, args, kwargs):
        """
        Wraps the function in its own
        parameters for future execution.

        Parameters
        ----------
        target : callable function
            name of the function which needs to be scheduled
        args : tuple
            args for the above target function
        kwargs : dict
            kwargs for the above target function

        Returns
        -------
        function : callable function
            target function loaded with its own parameters

        """
        try:
            function = partial(target, *args, **kwargs)
            # function.__qualname__ = target.__qualname__
            # function.__doc__ = target.__doc__
            return function
        except:
            self._processes = []
            raise
            
    def clear(self):
        """
        Stops all jobs as well as clears them from the schedule.

        Returns
        -------
        None.

        """
        while self._processes != []:
            try:
                for x in self._processes:
                    if x.is_alive():
                        x.terminate()
                        self._processes.remove(x)
            except:
                pass
