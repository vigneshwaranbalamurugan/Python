import time
from config import FAILURE_THRESHOLD, RESET_TIMEOUT

class CircuitBreaker:
    def __init__(self):
        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_time = None

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= FAILURE_THRESHOLD:
            self.state = "OPEN"

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def allow_request(self):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > RESET_TIMEOUT:
                self.state = "HALF_OPEN"
                return True

            return False

        return True
