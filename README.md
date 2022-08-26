# simple_scheduler
- Does not miss future events.
- Works even when period < execution time
- Works on any platform (Linux, Windows, Mac)
- Uses light weight multiprocessing to schedule jobs.
- This package uses a 24-hour clock, only.
- Simultaneously schedule any number of jobs.
- Recurring jobs to be precisely scheduled.
- Event jobs to be executed within the minute.
- Schedule the same function, again, with a different job_name
- On execution failure, set the number of reattempts.
- Control the duration between each re-attempt.
- Works only in background, hence easy to intergrate across platforms(eg. django, flask)
- Set start and stop timestamps if you want to ensure that your function executes only within this window

## Install
From [PyPi](https://pypi.org/project/simple_scheduler/) :

    pip install simple-scheduler

## Quick-start
There are 2 different schedulers:

1. Event scheduler (event occurs at an exact time)
```python
from simple_scheduler.event import event_scheduler
from time import sleep, ctime, time

def print_args(a, b=1, *args, **kwargs):
    print(ctime(time()), a, b, args, kwargs)

event_scheduler.add_job(
    target=print_args,
    args=(0,),
    kwargs={"b":2},
    tz="Asia/Kolkata",
    job_name="print-args-1",
    number_of_reattempts=2,
    when=["fri|14:28", "*|14:**"],
    reattempt_duration_in_seconds=5
    )
event_scheduler.add_job(
    target= print_args,
    args=(0, 2, "arg1", "arg2"),
    kwargs={
        "key1":"value1",
        "key2":"value2"
        },
    when=["fri|14:28", "*|14:**"],
    tz="Asia/Kolkata",
    start="Jul 23 13:00:00 2021",
    stop="Jul 23 15:00:00 2021",
    job_name="print-args-2",
    number_of_reattempts=2,
    reattempt_duration_in_seconds=5
    )
event_scheduler.run()
```

2. Recurring Scheduler (tasks occur after every "x"-seconds)
```python
from simple_scheduler.recurring import recurring_scheduler
from time import sleep, ctime, time

def wait_10_secs(t): wait_X_secs(10)

def wait_X_secs(t):
    began_at = ctime(time()); sleep(t)
    print(f"I waited {t} seconds. [From: {began_at} to {ctime(time())}]")
    
recurring_scheduler.add_job(
    target=wait_10_secs,
    period_in_seconds=5,                              # period < execution time
    start="Jul 23 12:18:00 2021",
    stop="Jul 23 12:19:00 2021",
    job_name="ten",
    number_of_reattempts=0,
    reattempt_duration_in_seconds=0,
    kwargs={"t":10},
    tz="Asia/Kolkata"
    )
recurring_scheduler.add_job(
    target=wait_X_secs,
    kwargs={"t":3},                                   # period > execution time
    period_in_seconds=5,
    job_name="three"
    )
recurring_scheduler.run()

```
## APIs
### Toggle verbose
```python
event_scheduler.verbose = False
recurring_scheduler.verbose = True
```

### Job summary
```python
event_scheduler.job_summary()
recurring_scheduler.job_summary()
```
    
### Number of reattempts in case event fails [fallback]
```python
event_scheduler.add_job(number_of_reattempts = 3)
recurring_scheduler.add_job(number_of_reattempts = 0)
```

### Reattempt duration(in seconds) between each reattempt [fallback]
```python
event_scheduler.add_job(reattempt_duration_in_seconds = 10)
recurring_scheduler.add_job(reattempt_duration_in_seconds = 10)
```

### Start time (keep the scheduler running but postpone execution until this time)
```python
event_scheduler.add_job(start="Dec 31 23:59:59 2021")
recurring_scheduler.add_job(start="Dec 31 23:59:59 2021")
```
    
### Stop time (time when scheduler expires)
```python
event_scheduler.add_job(stop="Dec 31 23:59:59 2021")
recurring_scheduler.add_job(stop="Dec 31 23:59:59 2021")
```
    
### Remove a single job
```python
event_scheduler.remove_job(job_name)
recurring_scheduler.remove_job(job_name)
```
    
### Clear schedule (remove all jobs)
```python
event_scheduler.clear()
recurring_scheduler.clear()
```
    
### Docker with gunicorn
    In app.py ensure that scheduler is started globally and not within main()
```python
event_scheduler.run()

if __name__ == "__main__":
   app.run(host="0.0.0.0", port="5000")
```
    Also, in gunicorn config use the --preload argument. This will ensure that
    only 1 instance of scheduler is running.
