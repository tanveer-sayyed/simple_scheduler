from time import sleep, ctime, time
from simple_scheduler.recurring import recurring_scheduler

def wait(t):
    sleep(t)
    print(f"I waited {t} seconds. [{ctime(time())}]")

recurring_scheduler.add_job(target=wait,
                            kwargs={"t":10},     # The function-wait() executes in 10 
                            period_in_seconds=5) # seconds but is called every 5-seconds.
recurring_scheduler.run()
