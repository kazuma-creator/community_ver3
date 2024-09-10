from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config

# 一旦インスタンスを作成
db = SQLAlchemy()
migrate = Migrate()

def create_app():
  app = Flask(__name__)
  CORS(app,resources={r"/*": {"origins": "*"}})
  app.config.from_object(Config)
  
  db.init_app(app)
  migrate.init_app(app,db)
  
  # ブループリントを登録
  from app.routes import main
  app.register_blueprint(main)
  
  from app.models import User,Community,Membership
  
  return app
