from flask import Flask, jsonify, request, render_template, json
import gspread
from google.oauth2 import service_account
import sys
import os

from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = './credentials.json'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = gspread.authorize(credentials)
gsheet = client.open("SNU Volleyball").sheet1
sh = client.open("SNU Volleyball")
livesheet = client.open("SNU Volleyball").worksheet("Display")

app = Flask(__name__, static_folder='client/build', static_url_path='')
CORS(app)

# API Route~
@app.route('/api', methods=['GET'])
@cross_origin()
def index():
    return {
        "tutorial": "Flask React Heroku"
    }

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/test", methods=['POST'])
def update_sheet():
    return {"201": "Success"}

@app.route("/standings", methods=['GET'])
def standings():
    return jsonify(get_games())

@app.route("/get-teams", methods=['GET'])
def teams():
    return jsonify(get_teams())


def get_teams():
    teams = gsheet.get_all_values()
    if teams:
        teams.pop(0)
    for ii in range(len(teams)):
        teams[ii][0]=str(ii)
        teams[ii] = list(filter(('').__ne__,teams[ii]))

    return teams

def get_games():
    matchups = livesheet.get_all_values()
    matchups.pop(0)
    return matchups


if __name__ == "__main__":
    app.run()
