from fastapi import FastAPI
from app.api.v1.products import router as products_router
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="Product Service", version="1.0.0")
    app.include_router(products_router, prefix="/api/v1/products", tags=["products"])
    return app


app = create_app()
