from fastapi import FastAPI

from src.config import routes, exceptions

from src.config.env import env

def create_app() -> FastAPI:
    docs_url = "/docs" if env.get_item("DEBUG", None) == "True" else None

    app = FastAPI(
        docs_url=docs_url,
        redoc_url='/',
        title=env.get_item("APP_NAME", "Quiz"),
        version="1.0",
        contact={
            'name': 'Diqxy1',
            'url': 'https://github.com/Diqxy1',
            'email': 'diqxy1@gmail.com'
        }
    )

    routes.init_app(app)
    exceptions.init_app(app)

    return app

app = create_app()