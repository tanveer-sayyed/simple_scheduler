from time import sleep, ctime, time
from simple_scheduler.event import event_scheduler

event_scheduler.timezones()
TZ = "Asia/Kolkata"
WHEN = ["tue|14:**", "*|10:45"] #[mon/tue/wed/thu/fri/sat/sun] or "*" for all days

# correct argument precedence in a function
def print_args(a, b=1, *args, **kwargs):
    print(ctime(time()), a, b, args, kwargs)
# the above print_args function would be called twice,
# so to differentiate between then use "job_name"

event_scheduler.add_job(target = print_args,
                        args = (0,), # don't forget "," for single arguments
                        kwargs = {"b":2},
                        when = WHEN,
                        tz = TZ,
                        job_name = "print-args-1")
event_scheduler.add_job(target= print_args,
                        args = (0, 2, "arg1", "arg2"),
                        kwargs = {"key1":"value1",
                                  "key2":"value2"},
                        when = WHEN,
                        tz = TZ,
                        job_name = "print-args-2")

event_scheduler.verbose = True # (default)
event_scheduler.job_summary()
event_scheduler.run()
event_scheduler.job_summary()

sleep(200)
event_scheduler.remove_job("print-args-2")

sleep(5)
event_scheduler.clear()
