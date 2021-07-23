# Google-SSO-AppFactory-Dash-App
A Google SSO enabled Flask-App Factory multiple Dash Apps with Flask-Login and User.Data retrieval inside of Dash Components

Using Flask-Login, we can utilize the Flask App factory methodologies to create all routing and User Login handling with a Postgres DB updated with SQL Alchemy. Once authenticated, users are taken to a home page created as a stand alone Dash instance and access User data inside of callbacks to update the Dash HTML components with the User's data. 

The Data Dashboard rendered inside is a standalone fully self updating Data dashboard built in Plotly's Dash for analytics and ease of access to grade, incident, and attendance data.

Google SSO implemented using flask to implement URL routing protection to require authentication for all users.

Extended PostGres Database with JSON documents for a hybrid DB and a custom data warehouse installation.

Complex Oracle SQL hits internal student information system nightly for data updates.

Gunicorn wsgi with nginx web server developed in Ubuntu 20.1 server hosted on a Nutanix Cluster.

Lots of Pandas data manipulation is specific to our student information system's database, and the data is legally protected so I am unable to upload and share that.

Data warehouse code, data, and Google Credentials not included in repo for security purposes. 
