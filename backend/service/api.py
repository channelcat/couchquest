from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from os import environ
from .codegen import (
    custom_generate_unique_id,
    generate_openapi_code,
    generate_openapi_schema,
)
from .static import bind_static
from .exceptions import bind_exceptions


logging.basicConfig(level=logging.INFO)

# Strip development options
IS_PRODUCTION_MODE = environ.get("ENV") == "production"


def lifespan(app: FastAPI):
    logging.info("Generating OpenAPI schema...")
    generate_openapi_schema(app)
    generate_openapi_code(host="http://localhost:4000", diff_files=True)

    yield


if IS_PRODUCTION_MODE:
    kwargs = {
        "openapi_url": None,
        "docs_url": None,
        "redoc_url": None,
    }
else:
    kwargs = {
        "lifespan": lifespan,
    }

api = FastAPI(
    generate_unique_id_function=custom_generate_unique_id,
    **kwargs,
)
api.service = CORSMiddleware(
    app=api,
    allow_origins=[
        "http://localhost:3000",
        "https://drinkarr.hill.tools",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bind_static(api)
bind_exceptions(api)
