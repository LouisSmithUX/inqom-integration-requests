# app.py
from flask import Flask
from notion.client import NotionClient
app = Flask(__name__)


# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
client = NotionClient(token_v2="8ccf0781da8e353a657cc539ae2dfeda1d770925789def42cb7fc13701a592819c15dd26a67102c4fe7513c0551eddbce1c1abe0752aa70d4af5f4f7279314ec51f267262c777860756cf9dd80ea")

# Replace this URL with the URL of the page you want to edit
page = client.get_block("https://www.notion.so/inqom/6e6f8425d65641a59c8757d6c45dfd3f?v=64a21046becb448195a529b7c2da2447")


@app.route('/addRow', methods=['POST'])
def post():
    json_data = request.json

    # Return the response in json format
    return jsonify(response)


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome!!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)