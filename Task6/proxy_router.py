import httpx
from fastapi import Request, HTTPException
from fastapi.responses import Response

from config import SERVICE_ROUTES
from cache import get_cache, set_cache


async def proxy_request(service_name, path, request, breaker):
    base_url = SERVICE_ROUTES[service_name]
    if not breaker.allow_request():
        raise HTTPException(503, "Service unavailable")
    cache_key = f"{service_name}:{path}"

    if request.method == "GET":
       cached = await get_cache(cache_key)
       if cached:
        return Response(content=cached)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                request.method,
                f"{base_url}/{path}",
                content=await request.body()
            )
        breaker.record_success()

        if request.method == "GET":
            await set_cache(cache_key, response.content)
        return Response(
            content=response.content,
            status_code=response.status_code
        )

    except Exception:
        breaker.record_failure()
        raise HTTPException(503, "Downstream error")