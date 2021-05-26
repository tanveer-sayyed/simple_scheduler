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
                            job_name="ten",
                            kwargs={"t":10})
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
recurring_scheduler.job_summary()

sleep(10)
print("Removing job with name 'ten'...")
recurring_scheduler.remove_job("ten")

sleep(10)
print("Removing job with name 'ten'...")
recurring_scheduler.remove_job("ten")

sleep(10)
print("Stopping and clearing the scheduler.\n")
recurring_scheduler.clear()
