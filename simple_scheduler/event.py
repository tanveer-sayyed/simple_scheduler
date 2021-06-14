from pytz import timezone
from datetime import datetime
from multiprocess import Process

from simple_scheduler.base import Schedule

class Event(Schedule):
    """ Event occurs at an exact time.
        e.g. scirpt_1 is called at 14:00 and 20:00
        Each event is tried 3-times (but executed only once)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _schedule(self, function, tz, when, number_of_reattempts,
                  reattempt_duration):
        """

        Parameters
        ----------
        function : callable function
            name of the function which needs to be scheduled
        tz : str
            timezone
        hour : int
            hour of the time to be scheduled
        minute : int
            minute of the time to be scheduled
        number_of_reattempts : int, optional
            each event is tried these many number of times, but executed once
        reattempt_duration : int, optional
            duration to wait (in seconds) after un-successful attempt

        Returns
        -------
        None.
        """
        while True:
            HH, MM = str(datetime.now(timezone(tz)).time()).\
                        rsplit(":",1)[0].\
                            split(":")
            day = self._days[datetime.today().weekday()]
            condition_1 =     (f"{day}|{HH}:{MM}" in when) |\
                                  (f"*|{HH}:{MM}" in when)
            condition_2 = (f"{day}|*{HH[1]}:{MM}" in when) |\
                              (f"*|*{HH[1]}:{MM}" in when)
            condition_3 = (f"{day}|{HH[0]}*:{MM}" in when) |\
                              (f"*|{HH[0]}*:{MM}" in when)
            condition_4 = (f"{day}|{HH}:*{MM[1]}" in when) |\
                              (f"*|{HH}:*{MM[1]}" in when)
            condition_5 = (f"{day}|{HH}:{MM[0]}*" in when) |\
                              (f"*|{HH}:{MM[0]}*" in when)
            condition_6 =       (f"{day}|**:{MM}" in when) |\
                                    (f"*|**:{MM}" in when)
            condition_7 =   (f"{day}|**:{MM[0]}*" in when) |\
                                (f"*|**:{MM[0]}*" in when)
            condition_8 =   (f"{day}|**:*{MM[1]}" in when) |\
                                (f"*|**:*{MM[1]}" in when)
            condition_9 =       (f"{day}|{HH}:**" in when) |\
                                    (f"*|{HH}:**" in when)
            if True in [condition_1, condition_2, condition_3, condition_4,
                        condition_5, condition_6, condition_7, condition_8,
                        condition_9]:
                for tries in range(number_of_reattempts):
                    try:
                        p = Process(target = function)
                        p.start()
                        self._workers.append(p)
                        self._sleep(period_in_seconds=59.9)
                        break
                    except Exception as e:
                        self._print(str(e))
                        self._sleep(period_in_seconds=reattempt_duration)
                        p.ternimate()
                        continue
            else:
                self._sleep(period_in_seconds=55)
                
    def __assert_int(self, i):
        try:
            if i is not "0":
                assert(int(i))
        except ValueError:
            assert(i == "*")

    def add_job(self, target, tz, when,
                job_name=None,
                number_of_reattempts=3,
                reattempt_duration=10,
                args=(),
                kwargs={}):
        """
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
        reattempt_duration : int, optional
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

        """
        when = [w.lower() for w in when]
        try:
            desired_day_list = list(self._days.values()) + ["*"]
            for element in when:
                if element.split("|")[0] not in desired_day_list:
                    raise Exception("Incorrect day; should be one of "+\
                                    "{list(self._days.values()) + ["*"]}")
                HH, MM = element.split("|")[1].split(":")
                try:
                    assert(len(HH) == 2)
                except:
                    raise
                try:
                    assert(len(MM) == 2)
                except:
                    raise
                self.__assert_int(HH[0])
                self.__assert_int(HH[1])
                self.__assert_int(MM[0])
                self.__assert_int(MM[1])
        except:
            raise Exception('Elements of "when"(list(str)) must be a ' +\
                            'collection of:\n*|HH:MM,\n*|HH:MM,\n*|H*:MM,\n'+\
                            '*|*H:MM,\n*|**:MM,\n*|**:M*,\n*|**:*M,\n*|HH:**')
        try:
            assert(type(reattempt_duration) == int)
        except ValueError:
            try:
                assert(type(reattempt_duration) == float)
            except ValueError:
                raise Exception("reattempt_duration(seconds) should be"+\
                                " either int or float")
            
        function, job_name = self._manifest_function(target,
                                                     job_name,
                                                     args,
                                                     kwargs)
        self._jobs[job_name] = [f"{job_name} event | {when} | {tz}]"]
        self._processes.append(Process(target=self._schedule,
                                       name = job_name,
                                       args=(function,
                                             tz,
                                             when,
                                             number_of_reattempts,
                                             reattempt_duration)))

event_scheduler = Event(verbose=True)
