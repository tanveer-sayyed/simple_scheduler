# simple_scheduler
- Does not miss future events.
- Uses light weight multiprocessing to schedule jobs.
- This package uses a 24-hour clock, only.
- Simultaneously schedule any number of jobs.
- Recurring jobs to be precisely scheduled.
- Event jobs to be executed within the minute.
- Works even when period < execution time
- Schedule the same function, again, with a different job_name
- On execution failure, set the number of reattempts.
- Control the duration between each re-attempt.
- Works only in background, hence easy to intergrate across platforms(eg. django, flask)

## Install
From [PyPi](https://pypi.org/project/simple_scheduler/) :

    pip install simple-scheduler

## How to use?

### Quick-start
See [examples](https://github.com/Vernal-Inertia/simple_scheduler/tree/main/examples/)

### Long
There are two different schedulers:

    >>> from simple_scheduler.event import event_scheduler    
    >>> from simple_scheduler.recurring import recurring_scheduler

Purpose of each scheduler:

    >>> print(event_scheduler.__doc__)
     Event occurs at an exact time.
        e.g. scirpt_1 is called at 14:00 and 20:00
        Each event is tried 3-times (but executed only once).

    >>> print(recurring_scheduler.__doc__)
     Recurring tasks are those that occur after every "x"-seconds.
        (e.g. script_1 is called every 600 seconds)

#### Using only recurrent_scheduler

    >>> print(recurring_scheduler.add_job.__doc__)

        Assigns an periodic task to a process.

        Parameters
        ----------
        target : a callable function
        period_in_seconds : int
            the time period in seconds to execute this function
        args : tuple(object,), optional
            un-named argumets for the "target" callable
            the default is ()
        job_name : str, optional
            used to identify a job, defaults to name of the function
            to remove jobs use this name            
        kwargs : dict{key:object}, optional
            named argumets for the "target" callable
            the default is {}
        number_of_reattempts : int, optional
            default is 0
            each recurring is tried these many number of times, but executed once
        reattempt_duration_in_seconds : int, optional
            default is 10 secs
            duration to wait (in seconds) after un-successful attempt

        Returns
        -------
        None.

See [examples/recurring.py](https://github.com/Vernal-Inertia/simple_scheduler/blob/main/examples/recurring.py)

#### Using only event_scheduler

    >>> print(event_scheduler.add_job.__doc__)

        Assigns an event to a process.

        Parameters
        ----------
        target : a callable function
        tz : str
            time zone (call the method .timezones() for more info)
        when : list, a collection of "day|HH:MM"
            at what precise time(s) should the function be called
            eg. ["mon|22:04","*|03:45", ...] please "only" use 24-hour
                                             clock with "|" as day separator
                                             and ":" as time separator
        job_name : str, optional
            used to identify a job, defaults to name of the function
            to remove jobs use this name
        number_of_reattempts : int, optional
            defailt is 3
            each event is tried these many number of times, but executed once
        reattempt_duration_in_seconds : int, optional
            default is 10 secs
            duration to wait (in seconds) after un-successful attempt
        args : tuple(object,), optional
            un-named argumets for the "target" callable
            the default is ()
        kwargs : dict{key:object}, optional
            named argumets for the "target" callable
            the default is {}

        Raises
        ------
        Exception
            - If time (in "when"-list) is not a collection of "day|HH:MM"
              i.e. *|HH:MM, *|HH:MM, *|*H:MM,, *|*H:MM, *|**:MM, *|**:*M, *|**:M*'
            eg. ["tue|12:30am","thu|2:30 pm", ...] please "only" use 24-hour
                                                   clock, with "|" as day
                                                   separator and ":" as time
                                                   separator

        Returns
        -------
        None.

See [examples/event.py](https://github.com/Vernal-Inertia/simple_scheduler/blob/main/examples/event.py)

### Toggle verbose (for debugging set to True)
    >>> event_scheduler.verbose = False
    >>> recurring_scheduler.verbose = True

### Job summary (before and after jobs are run)
    >>> event_scheduler.job_summary()
    >>> recurring_scheduler.job_summary()
    
### Number of reattempts in case event fails [fallback]
    >>> event_scheduler.add_job(number_of_reattempts = 3)
    >>> recurring_scheduler.add_job(number_of_reattempts = 0)

### Reattempt duration(in seconds) between each reattempt [fallback]
    >>> event_scheduler.add_job(reattempt_duration_in_seconds = 10)
    >>> recurring_scheduler.add_job(reattempt_duration_in_seconds = 10)

### Start time (keep the scheduler running but postpone execution at this time)
    >>> event_scheduler.add_job(start="Dec 31 23:59:59 2021")
    >>> recurring_scheduler.add_job(start="Dec 31 23:59:59 2021")
    
### Stop time (time when scheduler expires)
    >>> event_scheduler.add_job(stop="Dec 31 23:59:59 2021")
    >>> recurring_scheduler.add_job(stop="Dec 31 23:59:59 2021")
    
### Remove a single job
    >>> event_scheduler.remove_job(job_name)
    >>> recurring_scheduler.remove_job(job_name)
    
### Clear schedule (remove all jobs)
    >>> event_scheduler.clear()
    >>> recurring_scheduler.clear()
    
### Docker with gunicorn
    In app.py ensure that scheduler is started globally and not within main()
    >>> event_scheduler.run()
    >>> if __name__ == "__main__":
    >>>    app.run(host="0.0.0.0", port="5000")

    In gunicorn config or args, add: --preload
    (this will ensure that only one instance of scheduler is running)    