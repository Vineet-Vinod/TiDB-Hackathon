from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# declare database
db = SQLAlchemy()
DB_NAME = "database.db"

def createApp():
        app = Flask(__name__)
        app.config["SECRET_KEY"] = "testKey"
        
        # configure database
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
        db.init_app(app)
        migrate = Migrate(app, db)

        from .views import views
        from .auth import auth
        
        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

        # register database models
        from .models import User
        with app.app_context():
                #'''
                # deletes all contents of the database
                with db.engine.connect() as con:
                        trans = con.begin()
                        for table in db.metadata.sorted_tables: 
                                con.execute(table.delete())
                        trans.commit()
                #'''
                db.create_all()

        login_manager = LoginManager()
        login_manager.login_view = "views.home"
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
                return User.query.get(int(id))

        return app