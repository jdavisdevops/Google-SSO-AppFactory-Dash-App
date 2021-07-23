from flask import request, render_template, Blueprint, redirect, request, url_for
from flask_login import login_required, current_user
from flaskapp.models import User

# Blueprint Config
routes_bp = Blueprint("routes_bp", __name__, template_folder="templates")

User = current_user


@routes_bp.route("/data")
@login_required
def show_data():
    user_string = repr(User)
    user_photo = User.profile_pic
    index_url = "https://dds.ausd.net"
    return f"""
        <div> User Data: {user_string} </div>
        <div> To Dash: <a href={index_url}>Return to Index</a> </div>
        """
    # return(f"<div>id={User.id}, username={User.firstlast}> User: {User} </div>")


@routes_bp.route("/")
@login_required
def index():
    return redirect("/home/")


# @routes_bp.route("/data")
# @login_required
# def show_data():
#     return app
