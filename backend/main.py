from fastapi import FastAPI, Request
from backend.config.config import settings
from fastapi.middleware.cors import CORSMiddleware
from backend.middleware.logging import LoggingMiddleware
import time
from backend.routers import items, login, users, private, health


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["x-processing-time"] = str(process_time)
    return response


# middlewares
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.add_middleware(LoggingMiddleware)


# routers
app.include_router(items.router, prefix=settings.API_V1_STR)
app.include_router(login.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(private.router, prefix=settings.API_V1_STR)
app.include_router(health.router, prefix=settings.API_V1_STR)
