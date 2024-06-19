from flask import Flask, current_app
from api import api
from ff import FileFolder


def create_app(testing=False):
  app = Flask(__name__)
  if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
  app.register_blueprint(api)
  with app.app_context():
    if not hasattr(current_app, "ff"):
      current_app.ff = FileFolder()
  return app


if __name__ == "__main__":
  try:
    app = create_app()
    app.run(host="127.0.0.1", port=8080)
  except Exception as error:
    print(error)
  finally:
    with app.app_context():
      if hasattr(current_app, "ff"):
        current_app.ff.close()