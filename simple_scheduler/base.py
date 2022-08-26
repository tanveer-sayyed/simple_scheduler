from time import time, sleep
from pytz import all_timezones, timezone
from datetime import datetime
from functools import partial
from multiprocess import Process

class Schedule():
    def __init__(
            self,
            verbose:bool=False
            ) -> None:
        self._jobs = {}
        self._workers = []
        self._processes = []
        self._days = {
            0:"mon",
            1:"tue",
            2:"wed",
            3:"thu",
            4:"fri",
            5:"sat",
            6:"sun"
            }
        self.verbose = verbose

    def job_summary(self):
        """
        Provides summary of jobs that are still running

        Returns
        -------
        None.

        """
        self._print("\tScheduled jobs:")
        names = {p.name:p.is_alive() for p in self._processes}
        for _, name in enumerate(self._jobs):
            msg = f"{self._jobs[name][0]}"
            try:
                msg += f" running in {self._jobs[name][1]}"
                if not names[name]:
                    continue
            except:
                pass
            self._print(msg)

    def timezones(self):
        """
        A quick look-up of all pytz time-zones.

        Returns
        -------
        all_timezones : list
            pytz.all_timezones

        """
        return all_timezones

    def _print(
            self,
            message
            ):
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

    def _sleep(
            self,
            period_in_seconds
               ):
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

    def _execute(
            self,
            tz,
            start,
            stop,
            function,
            period_in_seconds,
            number_of_reattempts,
            reattempt_duration_in_seconds
            ):
        """
        Parameters
        ----------
        tz : str
            standard time zone (call the method .timezones() for more info)
            the default is "GMT"
        start : str, optional
            of the form "Month DD HH:MM:SS YYYY" (eg. "Dec 31 23:59:59 2021")
            the default is None
        stop : str, optional
            of the form "Month DD HH:MM:SS YYYY" (eg. "Dec 31 23:59:59 2021")
            the default is None
        function : callable function
            name of the function which needs to be scheduled
        period_in_seconds : int
        number_of_reattempts : int
            each event is tried these many number of times, but executed once
        reattempt_duration_in_seconds : int
            duration to wait (in seconds) after un-successful attempt

        Returns
        -------
        int

        """
        time_ = datetime.now(timezone(tz)).ctime()[4:]
        stop = stop if stop else time_
        start = start if start else time_
        if (time_ >= str(start)) & (time_ <= str(stop)):
            p = Process(target = function)
            p.start(); self._workers.append(p)
            timer = time() + period_in_seconds
            for tries in range(number_of_reattempts + 1):
                self._sleep(
                    period_in_seconds = timer - \
                                        time() - \
                                        reattempt_duration_in_seconds
                            )
                if (number_of_reattempts > 1) & (p.exitcode != 0):
                    p.join()
                    p = Process(target = function)
                    p.start(); self._workers.append(p)
            self._sleep(period_in_seconds= timer - time())
            return 1
        elif time_ < str(start):
            return 1
        elif time_ > str(stop):
            return 0

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

    def _manifest_function(
            self,
            target,
            job_name,
            args,
            kwargs
            ):
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

    def _validate_start_stop(
            self,
            start,
            stop
            ):
        """
        Parameters
        ----------
        start : str, optional
            of the form "Month DD HH:MM:SS YYYY" (eg. "Dec 31 23:59:59 2021")
            the default is None
        stop : str, optional
            of the form "Month DD HH:MM:SS YYYY" (eg. "Dec 31 23:59:59 2021")
            the default is None

        Raises
        ------
        Exception

        Returns
        -------
        None.

        """
        try:
            for x in [start, stop]:
                if x:
                    month, date, time, year = start.split(" ")
                    assert(month.istitle()); assert(len(month) == 3)
                    assert(date.isnumeric()); assert(len(date) == 2)
                    for t in time.split(":"):
                        assert(t.isnumeric()); assert(len(t) == 2)
                    assert(year.isnumeric()); assert(len(year) == 4)
        except:
            raise Exception('start/stop must be of the form'+\
                            ' "Month DD HH:MM:SS YYYY" (eg. "Dec 31 23:59:59 2021")')

    def remove_job(
            self,
            job_name
            ):
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

    def _remove_job(
            self,
            this_job
            ):
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
                self._jobs.pop(this_job.name)
                self._processes.remove(this_job)
                this_job.terminate()
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
