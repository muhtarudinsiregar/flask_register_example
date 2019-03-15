from flask import Flask
from config import Config

app = Flask(__name__)

# tell flask to read it and apply it
app.config.from_object(Config)

from app import routes
