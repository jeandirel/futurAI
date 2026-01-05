from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router as api_router
from .core.logging import configure_logging
from .core.middleware import RequestIDMiddleware
from .core.settings import settings


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="OneClickQuiz Agents", version=settings.version)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)
    return app


app = create_app()
