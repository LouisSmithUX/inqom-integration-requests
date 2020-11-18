# app.py
from flask import Flask,request
import json
from notion.client import NotionClient
import os
app = Flask(__name__)


@app.route('/addRow', methods=['POST'])
def post():
    json_data = request.json

    print(json_data)

    # Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
    client = NotionClient(token_v2= os.environ.get('NOTION', None))
    cv = client.get_collection_view("https://www.notion.so/inqom/6e6f8425d65641a59c8757d6c45dfd3f?v=64a21046becb448195a529b7c2da2447")

    row = cv.collection.add_row()
    row.name = json_data['name']
    row.profil = json_data['profil']
    row.integration_demandee = json_data['integration_demandee']
    row.explications = json_data['explications']

    # Return the response in json format
    return json.dumps({'success':True}), 204, {'ContentType':'application/json'} 


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome!!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)