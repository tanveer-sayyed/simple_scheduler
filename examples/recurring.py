from time import sleep, ctime, time
from simple_scheduler.recurring import recurring_scheduler

def wait_10_secs(t):
    wait_t_secs(10)

def wait_t_secs(t):
    began_at = ctime(time())
    sleep(t)
    print(f"I waited {t} seconds. [From: {began_at} to {ctime(time())}]")
# the above wait_t_secs function would be called twice,
# so to differentiate between then use "job_name"

recurring_scheduler.add_job(target=wait_10_secs,
                            period_in_seconds=5, # period < execution time
                            start="Jul 23 12:18:00 2021",
                            stop="Jul 23 12:19:00 2021",
                            job_name="ten",
                            number_of_reattempts=0,
                            reattempt_duration_in_seconds=0,
                            kwargs={"t":10},
                            tz="Asia/Kolkata")
recurring_scheduler.add_job(target=wait_t_secs,
                            kwargs={"t":7}, # period < execution time
                            period_in_seconds=5,
                            job_name="seven")
recurring_scheduler.add_job(target=wait_t_secs,
                            kwargs={"t":3}, # period > execution time
                            period_in_seconds=5,
                            job_name="three")

recurring_scheduler.verbose = True # (default)

recurring_scheduler.job_summary()
recurring_scheduler.run()
sleep(1)
recurring_scheduler.job_summary()

sleep(100)
print("Removing job with name 'three'...")
recurring_scheduler.remove_job("three")

sleep(50)
print("Removing job with name 'seven'...")
recurring_scheduler.remove_job("seven")

sleep(10)
print("Stopping and clearing the scheduler.\n")
recurring_scheduler.clear()
