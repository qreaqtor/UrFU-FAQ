from app.api.endpoints import app

from uvicorn import Server, Config


server = Server(Config(app, host="127.0.0.1", port=8000))
server.run()