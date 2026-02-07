import redis
import time

r = redis.Redis(host="redis", port=6379)

print("Worker started...")

while True:
    task = r.blpop("tasks", timeout=5)
    if task:
        print("Processing task:", task)
        time.sleep(3)
        print("Task done")
