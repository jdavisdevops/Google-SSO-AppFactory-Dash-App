# Internal Imports
from flaskapp.creds.get_google_auth import get_credentials
from flaskapp.models import User
from flaskapp import login_manager, db

# Package Imports
import requests
from flask import request, redirect, url_for, Blueprint
from flask_login import login_user
from oauthlib.oauth2 import WebApplicationClient
import json


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Google Config
GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET = get_credentials()

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

google_api = Blueprint("google_api", __name__, template_folder="templates")

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Google Login Callbacks
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@google_api.route("/login", methods=["GET", "POST"])
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@google_api.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        firstlast = userinfo_response.json()["name"]
        first_name = userinfo_response.json()["given_name"]
        last_name = userinfo_response.json()["family_name"]
        picture = userinfo_response.json()["picture"]
        users_email = userinfo_response.json()["email"]
        # Debug Print JSON Data
        # data = json.dumps(userinfo_response.json())
        # print(data)
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id=unique_id,
        firstlast=firstlast,
        first_name=first_name,
        last_name=last_name,
        email=users_email,
        profile_pic=picture,
    )
    # Doesn't exist? Add it to the database.
    if not load_user(user.id):
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)

    else:
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)

    # if not Users.get(unique_id) and Users.check_auth_users(users_email):
    #     Users.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in

    # Send user back to homepage
    return redirect(url_for("routes_bp.index"))
