# Async API Gateway with Rate Limiting & Caching

# Description
Build a reverse-proxy API gateway that routes requests to
downstream microservices. Implement token-bucket rate limiting, response
caching with TTL, and circuit-breaker patterns.
# Prerequisites:
- asyncioevent loop and coroutines
- aiohttpor FastAPI framework
- Token-bucket rate limiting algorithm
- Redis for caching ( aioredis )
- Circuit breaker design pattern
- HTTP reverse proxy concepts
- Middleware pattern

# Use-Case:
- Single entry point routing /api/users/** , /api/orders/** , etc. to separate
- services
- Enforce per-API-key rate limits (e.g., 50 req/min)
- Cache GET responses with configurable TTL
- Open circuit breaker after 5 consecutive failures on a downstream service
- Return fallback 503 responses when circuit is open
- Expose a health dashboard showing service status and cache hit rates#