"""Starting point and sub-paths are defined here"""
from fastapi import FastAPI, Response, Request
from app.routers import (
    users, login, tweets, likes, comments, follows,
    timeline
)
import socket
import time
import structlog
from uvicorn.protocols.utils import get_path_with_query_string
from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.context import correlation_id
import os
from starlette.concurrency import iterate_in_threadpool
from pydantic import parse_obj_as
from app.custom_logging import setup_logging


LOG_JSON_FORMAT = parse_obj_as(bool, os.getenv("LOG_JSON_FORMAT", False))
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
setup_logging(json_logs=LOG_JSON_FORMAT, log_level=LOG_LEVEL)


app = FastAPI()
app.include_router(users.router)
app.include_router(login.router)
app.include_router(follows.router)
app.include_router(tweets.router)
app.include_router(likes.router)
app.include_router(comments.router)
app.include_router(timeline.router)


access_logger = structlog.stdlib.get_logger("api.access")


# region Get Request Body workaround
# https://stackoverflow.com/questions/69669808/fastapi-custom-middleware-getting-body-of-request-inside
async def set_body(request: Request, body: bytes):
    async def receive():
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    set_body(request, body)
    return body
# endregion


@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    structlog.contextvars.clear_contextvars()
    # These context vars will be added to all log entries emitted
    # during the request
    request_id = correlation_id.get()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start_time = time.perf_counter_ns()
    # If the call_next raises an error, we still want to return
    # our own 500 response, so we can add headers to it
    # (process time, request ID...)
    response = Response(status_code=500)
    try:
        await set_body(request, await request.body())
        request_body = await get_body(request)
        response = await call_next(request)
    except Exception:
        # TODO: Validate that we don't swallow exceptions (unit test?)
        structlog.stdlib.get_logger("api.error")\
            .exception("Uncaught exception")
        raise
    finally:
        response_body = [section async for section in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        for res in response_body:
            response_body = res.decode('utf8').replace("'", '"')

        process_time = time.perf_counter_ns() - start_time
        status_code = response.status_code
        url = get_path_with_query_string(request.scope)
        client_host = request.client.host
        client_port = request.client.port
        http_method = request.method
        http_version = request.scope["http_version"]
        # Recreate the Uvicorn access log format, but add all
        # parameters as structured information
        access_logger.debug(
            f"""{client_host}:{client_port} - "{http_method} {url} HTTP/{
                http_version}" {status_code}""",
            http={
                "url": str(request.url),
                "status_code": status_code,
                "method": http_method,
                "request_id": request_id,
                "version": http_version,
            },
            network={"client": {"ip": client_host, "port": client_port}},
            duration=process_time,
            request={
                "body": request_body,
                "path_params": dict(request.path_params),
                "query_params": dict(request.query_params),
                },
            response=response_body
        )
        response.headers["X-Process-Time"] = str(process_time / 10 ** 9)
        return response


# This middleware must be placed after the logging,
# to populate the context with the request ID
# NOTE: Why last??
# Answer: middlewares are applied in the reverse order
# of when they are added.
app.add_middleware(CorrelationIdMiddleware)


@app.get('/')
def root() -> dict:
    """Root path"""
    return {"message": "Welcome to our Twitter Clone! "
            "Go to '/docs' for the API documentation.",
            "Container Id": f'{socket.gethostname()}'}
