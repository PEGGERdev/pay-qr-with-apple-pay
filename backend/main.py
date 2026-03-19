import uvicorn

from models import schemas  # noqa: F401
from core.config import app_config
from core.application import Routing


def create_app():
    return Routing().get_app()


if __name__ == "__main__":
    uvicorn.run(create_app(), host=app_config.app_host, port=app_config.app_port)
