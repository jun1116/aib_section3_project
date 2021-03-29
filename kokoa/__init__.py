from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    app = Flask(__name__)
    
    if app.config["ENV"] == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    if config is not None:
        app.config.from_pyfile(config)

    db.init_app(app)
    migrate.init_app(app, db)
    from .models import user_model
    # from .models import tweet_model

    from kokoa.routes import main_route
    from kokoa.routes import chat_route
    from kokoa.routes import find_route

    app.register_blueprint(main_route.bp)
    app.register_blueprint(chat_route.bp)
    app.register_blueprint(find_route.bp)
    # app.register_blueprint(user_route.bp, url_prefix='/user')

    app.secret_key = 'super'

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
