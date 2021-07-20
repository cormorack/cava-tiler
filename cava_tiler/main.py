"""cava-tiler app."""

import logging

from brotli_asgi import BrotliMiddleware
from cava_tiler.settings import api_config
from cava_tiler.version import __version__ as tiler_version
from cava_tiler.middleware import (
    CacheControlMiddleware,
    LoggerMiddleware,
    LowerCaseQueryStringMiddleware,
    TotalTimeMiddleware,
)
from cava_tiler.routers import cog

from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers

from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

# turn off or quiet logs
logging.getLogger("botocore.credentials").disabled = True
logging.getLogger("botocore.utils").disabled = True
logging.getLogger("rio-tiler").setLevel(logging.ERROR)

app = FastAPI(
    title=api_config.name,
    version=tiler_version,
    openapi_url="/api/openapi.json",
    description="Interactive Oceans Tiling Service",
)

app.include_router(cog.router, prefix="/cog", tags=["Cloud Optimized GeoTIFF"])

add_exception_handlers(app, DEFAULT_STATUS_CODES)
if api_config.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_config.cors_origins,
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

app.add_middleware(BrotliMiddleware, minimum_size=0, gzip_fallback=True)
app.add_middleware(
    CacheControlMiddleware,
    cachecontrol=api_config.cachecontrol,
    exclude_path={r"/healthz"},
)

if api_config.debug:
    app.add_middleware(LoggerMiddleware, headers=True, querystrings=True)
    app.add_middleware(TotalTimeMiddleware)

if api_config.lower_case_query_parameters:
    app.add_middleware(LowerCaseQueryStringMiddleware)


@app.get("/healthz", description="Health Check", tags=["Health Check"])
def ping():
    """Health check."""
    return {"ping": "pong!"}


@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse(url="/docs")
