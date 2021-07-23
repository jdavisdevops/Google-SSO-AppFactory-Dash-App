# import os
# from oauthlib.oauth2 import WebApplicationClient
# from flask import Flask, redirect, request, url_for
# import requests
# from flask_login import LoginManager, login_required, login_user, logout_user
# from flaskapp.googleroutes import google_api
# # from flask_sqlalchemy import SQLAlchemy
# # from flask_migrate import Migrate
# from flaskapp.models import Users
# # from flaskapp.creds.get_google_auth import get_credentials
# # from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin

# app = Flask(__name__)
# app.config.update(
#     DEBUG=True,
#     DEVELOPMENT=True,
#     TESTING=False,
#     CSRF_ENABLED=True,
#     SECRET_KEY=os.urandom(24),
#     SQLALCHEMY_DATABASE_URI="postgresql://postgres:Superman17!@localhost:5432/users",
# )
# app.register_blueprint(google_api)

# Login Manager
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "/login"


# @login_manager.user_loader
# def load_user(user_id):
#     return Users.query.get(int(user_id))


# @app.route('/data', methods=['GET'])
# def show_data():
#     if request.method == 'GET':
#         data = Users.query.all()
#         results = [
#             {
#                 "id": user.id,
#                 "email": user.email,
#                 "profile_pic": user.profile_pic,
#             } for user in data]
        


# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0")
