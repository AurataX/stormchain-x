from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints import (
    assets,
    graph,
    health,
    observations,
    recovery,
    scenarios,
    simulation,
)
from app.core.config import Settings
from app.core.database import connect
from app.core.errors import register_error_handlers


def create_app(settings: Settings | None = None):
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(application):
        engine, sessions = connect(settings.database_url)
        application.state.engine = engine
        application.state.sessions = sessions
        application.state.settings = settings
        try:
            yield
        finally:
            await engine.dispose()

    application = FastAPI(title="STORMCHAIN-X", version="0.2.0", lifespan=lifespan)

    register_error_handlers(application)
    for router in (
        health.router,
        assets.router,
        observations.router,
        scenarios.router,
        graph.router,
        simulation.router,
        recovery.router,
    ):
        application.include_router(router)
    return application


app = create_app()
