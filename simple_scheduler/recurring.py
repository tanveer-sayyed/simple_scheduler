from multiprocess import Process

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
                self._sleep(period_in_seconds=period_in_seconds)
                p = Process(target = function)
                p.start()
                self._workers.append(p)
            except Exception as e:
                self._print(str(e))
                [p.terminate for p in self._workers]
                self._workers = []
                pass

    def add_job(self, target, period_in_seconds, job_name=None, args=(),
                kwargs={}):
        """
        Assigns an periodic task to a process.

        Parameters
        ----------
        target : a callable function
        period_in_seconds : int
            the time period in seconds to execute this function
        job_name : str, optional
            used to identify a job, defaults to name of the function
            to remove jobs use this name
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
        function, job_name = self._manifest_function(target,
                                                     job_name,
                                                     args,
                                                     kwargs)
        self._jobs[job_name] = [f"{job_name} "+\
                               f"[recurring | {period_in_seconds}-second(s)]"]
        p = Process(target=self._schedule,
                    name = job_name,
                    args=(function, period_in_seconds))
        self._processes.append(p)

recurring_scheduler = Recurring(verbose=True)
