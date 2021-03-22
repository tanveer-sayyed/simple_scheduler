# simple_scheduler
- Uses multiprocessing.
- The package uses a 24-hour clock, only.
- Simultaneously schedule any number of jobs.
- A job would be called any time within the 60-seconds[0-59] of a minute. This
  package does not begin execution of a job at the 0th-second of the minute.

## Install
From [PyPi](https://pypi.org/project/simple_scheduler/) :

    pip install simple-scheduler

## How to use?

### Quick-start
    Copy-paste the code at the bottom and run.
    
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

correct argument precedence in a function

    >>> def target(a, b=1, *args, **kwargs):
            print(a, b, args, kwargs)
      
Add above target function twice. Each function would be called on timestamps
(day|HH:MM) mentioned in list WHEN.

    >>> WHEN = ["wed|16:55", "*|16:56"] # "*" --> all days
    >>> TZ = "Asia/Kolkata"
    >>> event_scheduler.add_job(target= target,
                                args = (0,), # ... use "," for single arguments
                                kwargs = {"b":2},
                                when = WHEN,
                                tz = TZ)
    >>> event_scheduler.add_job(target= target,
                                args = (0, 2, "arg1", "arg2"),
                                kwargs = {"key1":"value1",
                                          "key2":"value2"},
                                when = WHEN,
                                tz = TZ)
    >>> event_scheduler.run()
        Wed Mar 17 16:55:32 2021 :: target [event @wed|16:55|Asia/Kolkata]
        0 2 () {}
        Wed Mar 17 16:55:32 2021 :: target [event @wed|16:55|Asia/Kolkata]
        0 2 ('arg1', 'arg2') {'key1': 'value1', 'key2': 'value2'}
        Wed Mar 17 16:56:27 2021 :: target [event @wed|16:56|Asia/Kolkata]
        0 2 () {}
        Wed Mar 17 16:56:27 2021 :: target [event @wed|16:56|Asia/Kolkata]
        0 2 ('arg1', 'arg2') {'key1': 'value1', 'key2': 'value2'}

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
        kwargs : dict{key:object}, optional
            named argumets for the "target" callable
            the default is {}

        Returns
        -------
        None.
    >>> from time import sleep
    >>> def wait(t):
            sleep(t)
            print(f"I waited {t} seconds")
    >>> recurring_scheduler.add_job(target=wait,
                                kwargs={"t":10},
                                period_in_seconds=5)
    >>> recurring_scheduler.run()
        Wed Mar 17 17:14:30 2021 :: wait [recurring | 5-second(s)]
        Wed Mar 17 17:14:35 2021 :: wait [recurring | 5-second(s)]
        I waited 10 seconds
        Wed Mar 17 17:14:40 2021 :: wait [recurring | 5-second(s)]
        I waited 10 seconds
        Wed Mar 17 17:14:45 2021 :: wait [recurring | 5-second(s)]

#### Note
The execution time of above "wait"-function is 10 seconds.
But, is being called every 5-seconds.

### Toggle verbose

    >>> event_scheduler.verbose = False
    >>> recurring_scheduler.verbose = True
    
## Complete code:
```
from time import sleep
from simple_scheduler.event import event_scheduler
from simple_scheduler.recurring import recurring_scheduler

print(event_scheduler.__doc__)
print(event_scheduler.add_job.__doc__)
print()
print(recurring_scheduler.__doc__)
print(recurring_scheduler.add_job.__doc__)
print()

# Select your timezone
event_scheduler.timezones()
TZ = "Asia/Kolkata"
WHEN = ["wed|17:26", "*|17:27"], # 1-min difference, "*" for all days

# correct argument precedence in a function
def target(a, b=1, *args, **kwargs):
    print(a, b, args, kwargs)
    
def wait(t):
    sleep(t)
    print(f"I waited {t} seconds")

event_scheduler.add_job(target = target,
                        args = (0,),   # don't forget "," for single arguments
                        kwargs = {"b":2},
                        when = WHEN,
                        tz = TZ)
event_scheduler.add_job(target= target,
                        args = (0, 2, "arg1", "arg2"),
                        kwargs = {"key1":"value1",
                                  "key2":"value2"},
                        when = WHEN,
                        tz = TZ)
recurring_scheduler.add_job(target=wait,
                            kwargs={"t":10},     # The function-wait() executes in 10 seconds
                            period_in_seconds=5) # but is called every 5-seconds.
event_scheduler.run()
recurring_scheduler.run()
```