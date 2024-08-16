import time

from fastapi import Request

from logger import logger


async def request_middleware(request: Request, call_next):
    start_time = time.time()

    # Add request logging here
    log_dict = {
        "method": request.method,
        "url": request.url.path,
        "headers": dict(request.headers),
        "body": await request.body(),
    }
    logger.info(log_dict, extra={"request": log_dict})

    response = await call_next(request)

    process_time = time.time() - start_time
    # Add response logging here
    log_dict = {"url": request.url.path, "method": request.method, "process_time": process_time}
    logger.info(log_dict, extra={"response": log_dict})
    return response
