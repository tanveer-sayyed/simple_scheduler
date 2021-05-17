from simple_scheduler.event import event_scheduler

event_scheduler.timezones()
TZ = "Asia/Kolkata"
# day -> [mon/tue/wed/thu/fri/sat/sun]
WHEN = ["mon|10:29", "*|10:30"] #"*" for all days, 1-min difference

# correct argument precedence in a function
def target(a, b=1, *args, **kwargs):
    print(a, b, args, kwargs)

event_scheduler.add_job(target = target,
                        args = (0,), # don't forget "," for single arguments
                        kwargs = {"b":2},
                        when = WHEN,
                        tz = TZ)
event_scheduler.add_job(target= target,
                        args = (0, 2, "arg1", "arg2"),
                        kwargs = {"key1":"value1",
                                  "key2":"value2"},
                        when = WHEN,
                        tz = TZ)
event_scheduler.run()
