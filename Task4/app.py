import redis
import json
import time
import sys
import uuid

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

QUEUE_NAME = "task_queue"
DLQ_NAME = "dead_letter_queue"
RESULT_BACKEND = "task_results"

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

TASK_MAP = {
    "add": add,
    "multiply": multiply,
    "fail_task": fail_task
}

def store_result(task_id, data):
    redis_client.hset(
        RESULT_BACKEND,
        task_id,
        json.dumps(data)
    )

def get_result(task_id):
    result = redis_client.hget(
        RESULT_BACKEND,
        task_id
    )
    if result:
        return json.loads(result)
    return None

def send_task(task_name, *args):
    task_id = str(uuid.uuid4())
    task = {
        "task_id": task_id,
        "task": task_name,
        "args": args,
        "retry": 0,
        "status": "PENDING",
        "created_at": time.time()
    }
    store_result(task_id, task)
    redis_client.lpush(
        QUEUE_NAME,
        json.dumps(task)
    )
    print(f"Task Submitted → ID: {task_id}")
    return task_id

def producer():
    print("Producer started")
    send_task("add", 10, 20)
    send_task("multiply", 5, 6)
    send_task("fail_task", 99)

def exponential_backoff(retry):
    return 2 ** retry

def worker():
    print("Worker started  Waiting for tasks...")
    while True:
        task_data = redis_client.brpop(QUEUE_NAME)
        _, task_json = task_data
        task = json.loads(task_json)
        task_id = task["task_id"]
        task["status"] = "RUNNING"
        task["start_time"] = time.time()
        store_result(task_id, task)
        task_name = task["task"]
        args = task["args"]
        print(f"\nExecuting {task_name} | TaskID={task_id}")
        try:
            result = TASK_MAP[task_name](*args)
            task["status"] = "SUCCESS"
            task["result"] = result
            print("Success  Result:", result)
        except Exception as e:
            print("Failed:", e)
            task["retry"] += 1
            if task["retry"] <= MAX_RETRIES:
                delay = exponential_backoff(task["retry"])
                print(f"Retrying in {delay} seconds")
                time.sleep(delay)

                redis_client.lpush(
                    QUEUE_NAME,
                    json.dumps(task)
                )

                task["status"] = "RETRYING"
            else:
                task["status"] = "FAILED"
                task["error"] = str(e)
                redis_client.lpush(
                    DLQ_NAME,
                    json.dumps(task)
                )
        task["end_time"] = time.time()
        if "start_time" in task:
            task["duration"] = (
                task["end_time"]
                - task["start_time"]
            )
        store_result(task_id, task)

def show_task(task_id):
    result = get_result(task_id)
    if result:
        print("\nTask Details:\n")
        for key, value in result.items():
            print(f"{key} : {value}")
    else:
        print("Task not found")

def dashboard():
    print("\nDashboard View\n")
    tasks = redis_client.hgetall(
        RESULT_BACKEND
    )
    for task_id, data in tasks.items():
        task = json.loads(data)
        print(
            f"{task_id} | "
            f"{task['task']} | "
            f"{task['status']} | "
            f"Retry={task['retry']}"
        )
        
def show_dlq():
    print("\nDead Letter Queue\n")
    tasks = redis_client.lrange(
        DLQ_NAME,
        0,
        -1
    )
    for task in tasks:
        print(json.loads(task))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "producer":
        producer()
    elif mode == "worker":
        worker()
    elif mode == "dashboard":
        dashboard()
    elif mode == "status":
        if len(sys.argv) < 3:
            print("Provide Task ID")
        else:
            show_task(sys.argv[2])
    elif mode == "dlq":
        show_dlq()
    else:
        print("Invalid command")