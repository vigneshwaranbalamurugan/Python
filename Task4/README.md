# Distributed Task Queue

# Description
Implement a producer-consumer task queue that distributes work
across multiple worker processes. Include task serialization, retry logic with
exponential backoff, dead-letter queues, and result backends.

# Use-Case:
- Producer enqueues callable tasks with arguments
- Multiple worker processes poll the queue and execute tasks
- Failed tasks retry up to N times with increasing delays
- Permanently failed tasks move to a dead-letter queue
- Results stored in a backend (Redis/SQLite) for later retrieval
- Dashboard view showing task status, retries, and duration