"""Logging middleware with request ID tracing and default function ID handling."""

from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import uuid
import contextvars


request_id_ctx_var = contextvars.ContextVar("request_id", default=None)


def add_request_id_to_log(record: dict) -> None:
    """Inject request ID and default function ID into log records."""
    record["extra"]["request_id"] = request_id_ctx_var.get() or "N/A"
    record["extra"].setdefault("function_id", "N/A")


logger.configure(patcher=add_request_id_to_log)

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level:<8}</level> | "
    "RequestID=<cyan>{extra[request_id]}</cyan> | "
    "FuncID=<magenta>{extra[function_id]}</magenta> | "
    "<level>{message}</level>\n"
)

logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=""),
    format=LOG_FORMAT,
    enqueue=True,
    colorize=True,
)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log incoming HTTP requests and responses."""

    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request_id_ctx_var.set(request_id)

        try:
            body_bytes = await request.body()
            body_text = body_bytes.decode("utf-8", errors="ignore").strip()
            logger.debug(
                f"Request: {request.method} {request.url.path} | Body: {body_text or 'empty'}"
            )

            response = await call_next(request)

        except Exception as e:
            logger.exception(
                f" Error while processing {request.method} {request.url.path}: {str(e)}"
            )
            raise

        response.headers["X-Request-ID"] = request_id
        return response
