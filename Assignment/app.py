from flask import Flask, __main__, render_template, request


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()
username = quote_plus(os.getenv('MONGODB_USERNAME'))
password = quote_plus(os.getenv('MONGODB_PASSWORD'))
cluster = os.getenv('MONGODBB_CLUSTER')

url = f"mongodb+srv://{username}:{password}@{cluster}"


# Create a new client and connect to the server
client = MongoClient(url, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)
@app.route('/')
def form():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = dict(request.form)
        client['mgdb']['formdata'].insert_one(data)
        return render_template("submit.html")
    except Exception as e:
        return str(e)

@app.route('/api')
def func():
    data = list(client['mgdb']['formdata'].find_one({}, {'_id': 0}))
    data.tolist()
    return {'data': data}

if __name__ == '__main__':
    app.run(debug=True)