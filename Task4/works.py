import redis, json, time, sys, uuid
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

QUEUE = "task_queue"
DLQ = "dead_letter_queue"
RESULTS = "task_results"
MAX_RETRIES = 3

def add(a, b):
    time.sleep(2)
    return a + b

def multiply(a, b):
    time.sleep(3)
    return a * b

def fail_task(x):
    time.sleep(1)
    raise Exception("Intentional failure")

TASKS = {
    "add": add,
    "multiply": multiply,
    "fail_task": fail_task
}

def save(task_id, data):
    r.hset(RESULTS, task_id, json.dumps(data))

def load(task_id):
    data = r.hget(RESULTS, task_id)
    return json.loads(data) if data else None

def send(task_name, *args):
    task_id = str(uuid.uuid4())
    task = {
        "task_id": task_id,
        "task": task_name,
        "args": args,
        "retry": 0,
        "status": "PENDING",
        "created_at": time.time()
    }
    save(task_id, task)
    r.lpush(QUEUE, json.dumps(task))
    print("Submitted:", task_id)
    return task_id

def producer():
    print("Producer started")
    send("add", 10, 20)
    send("multiply", 5, 8)
    send("fail_task", 99)

def backoff(n):
    return 2 ** n

def worker():
    print("Worker waiting for tasks...")
    while True:
        _, raw = r.brpop(QUEUE)
        task = json.loads(raw)
        tid = task["task_id"]
        task["status"] = "RUNNING"
        task["start_time"] = time.time()
        save(tid, task)
        try:
            result = TASKS[task["task"]](*task["args"])
            task.update({
                "status": "SUCCESS",
                "result": result
            })
            print("Success:", result)
        except Exception as e:
            task["retry"] += 1
            if task["retry"] <= MAX_RETRIES:
                delay = backoff(task["retry"])
                print("Retrying in", delay)
                time.sleep(delay)
                task["status"] = "RETRYING"
                r.lpush(QUEUE, json.dumps(task))
            else:
                task.update({
                    "status": "FAILED",
                    "error": str(e)
                })
                r.lpush(DLQ, json.dumps(task))

        task["end_time"] = time.time()
        task["duration"] = task["end_time"] - task["start_time"]
        save(tid, task)

def dashboard():
    print("\nDashboard\n")
    for tid, data in r.hgetall(RESULTS).items():
        task = json.loads(data)
        print(  tid,"|",task["task"], "|", task["status"],  "| retry:", task["retry"]  )

def status(task_id):
    task = load(task_id)
    if not task:
        print("Task not found")
        return
    print("\nTask Details\n")
    for k, v in task.items():
        print(k, ":", v)

def show_dlq():
    print("\nDead Letter Queue\n")
    for t in r.lrange(DLQ, 0, -1):
        print(json.loads(t))

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "producer":
        producer()
    elif cmd == "worker":
        worker()
    elif cmd == "dashboard":
        dashboard()
    elif cmd == "status":
        status(sys.argv[2])
    elif cmd == "dlq":
        show_dlq()
    else:
        print("Invalid command")