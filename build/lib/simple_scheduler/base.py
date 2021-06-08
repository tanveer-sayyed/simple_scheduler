from time import time, sleep
from functools import partial
from pytz import all_timezones

class Schedule():
    """ The parent of "event" and "recurring" classes."""

    def __init__(self, verbose=False):
        self._processes = []
        self._workers = []
        self.verbose = verbose
        self._days = {
            0:"mon",
            1:"tue",
            2:"wed",
            3:"thu",
            4:"fri",
            5:"sat",
            6:"sun"
            }
        self._jobs = {}

    def job_summary(self):
        self._print("\tScheduled jobs:")
        for _, name in enumerate(self._jobs):
            msg = f"{self._jobs[name][0]}"
            try:
                msg += f" running in {self._jobs[name][1]}"
            except:
                pass
            self._print(msg)

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
            print(message)

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
        if period_in_seconds > 0:
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
                [p.start() for p in self._processes]
                for p in self._processes:
                    self._jobs[p.name].append(p.pid)
        except:
            [p.terminate() for p in self._processes]
            pass

    def _manifest_function(self, target, job_name, args, kwargs):
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
            name = job_name if job_name else target.__qualname__
            function.func.__qualname__ = name
            return function, name
        except:
            self._processes = []
            raise

    def remove_job(self, job_name):
        """
        Remove job from schedule by providing job_name

        Parameters
        ----------
        job_name : str
            Name of the job assigend to argument "job_name" while adding job

        Returns
        -------
        None.

        """
        remove_jobs = [p for p in self._processes if p.name == job_name]
        if remove_jobs:
            for p in remove_jobs:
                self._remove_job(p)
            self.job_summary()
        else:
            self._print("No such job_name exists.")

    def _remove_job(self, this_job):
        """
        Helper function.

        Parameters
        ----------
        this_job : instance of multiprocess.Process

        Returns
        -------
        None.

        """
        try:
            if this_job.is_alive():
                self._print(f"Removed job: {this_job.name}")
                this_job.terminate()
                self._processes.remove(this_job)
                self._jobs.pop(this_job.name)
        except:
            raise

    def clear(self):
        """
        Stops all jobs as well as clears them from the schedule.

        Returns
        -------
        None.

        """
        for p in self._processes:
            self._remove_job(p)
        # in case a process is still alive do the following
        for p in [p for p in self._processes if p.is_alive()]:
            self._remove_job(p)
        self.job_summary()
