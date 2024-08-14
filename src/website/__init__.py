from flask import Flask
#from flask_login import LoginManager

# declare database

def createApp():
        app = Flask(__name__)
        app.config["SECRET_KEY"] = "testKey"
        
        # configure database
        # init database

        from .views import views
        #from .auth import auth
        
        app.register_blueprint(views, url_prefix='/')
        #app.register_blueprint(auth, url_prefix='/')

        # register database models

        #login_manager = LoginManager()
        #login_manager.login_view = "views.home"
        #login_manager.init_app(app)

        # load user function

        return app