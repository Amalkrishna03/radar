import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from api.main import api_router
from utils.source import config

app = FastAPI(
    title="RADAR",
    openapi_url="/api/openapi.json",
    docs_url="/api/swagger",
    redoc_url="/api/redoc",
)

print(config["ENV"])

app.include_router(api_router, prefix="/api")

if config["ENV"] == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def main():
    if config["ENV"] == "production":
        app.mount("/", StaticFiles(directory="web/dist/", html=True), name="static")

    if config["ENV"] == "development":
        @app.get("/")
        @app.get("/{index}")
        async def index(request: Request):
            url = f"{config['FRONTEND']}{request.url.path}"
            response = RedirectResponse(url=url)
            return response


if __name__ == "__main__":
    main()
    uvicorn.run(app, host="0.0.0.0", port=4000)

# uv run --env-file .env fastapi dev server.py
