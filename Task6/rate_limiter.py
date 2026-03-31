import time

class TokenBucket:
    def __init__(self, rate, window):
        self.rate = rate
        self.window = window
        self.tokens = rate
        self.last_time = time.time()

    def allow_request(self):
        now = time.time()
        elapsed = now - self.last_time
        refill = (elapsed / self.window) * self.rate
        self.tokens = min(self.rate, self.tokens + refill)
        if self.tokens >= 1:
            self.tokens -= 1
            self.last_time = now
            return True
        return False