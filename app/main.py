from fastapi import FastAPI
from routes import router as api_router


def get_application() -> FastAPI:
    """
    Controller to setup the application and return an Application
    instance to Uvicorn.
    """
    application = FastAPI()
    application.include_router(api_router)

    return application


app = get_application()
