from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from config import RATE_LIMIT, RATE_WINDOW
from rate_limiter import TokenBucket
from circuit_breaker import CircuitBreaker
from proxy_router import proxy_request
from cache import connect_redis

from contextlib import asynccontextmanager

app = FastAPI()


rate_limiters = {}


users_breaker = CircuitBreaker()
orders_breaker = CircuitBreaker()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_redis()
    yield

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    api_key = request.headers.get("x-api-key", "guest")
    if api_key not in rate_limiters:
        rate_limiters[api_key] = TokenBucket(RATE_LIMIT, RATE_WINDOW)
    if not rate_limiters[api_key].allow_request():
        return JSONResponse(
            status_code=429,
            content={"message": "Rate limit exceeded"}
        )
    return await call_next(request)

@app.api_route("/api/users/{path:path}", methods=["GET","POST","PUT","DELETE"])
async def users_route(path: str, request: Request):
    return await proxy_request("users", path, request, users_breaker)

@app.api_route("/api/orders/{path:path}", methods=["GET","POST","PUT","DELETE"])
async def orders_route(path: str, request: Request):
    return await proxy_request("orders", path, request, orders_breaker)

@app.get("/dashboard")
async def dashboard():
    return {
        "users_service": users_breaker.state,
        "orders_service": orders_breaker.state,
        "clients": len(rate_limiters)
    }
