from app.api.endpoints import app
from uvicorn import Server, Config
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="app/static"), name="static")

server = Server(Config(app, host="127.0.0.1", port=8000))
server.run()