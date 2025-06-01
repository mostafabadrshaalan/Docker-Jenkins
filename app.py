import os
from dotenv import load_dotenv
from flask import Flask
import logging
from mongodb_odm import connect


# I can put the db name like in docker-compose file (image : mongo) instead of host name
# connect("mongodb://localhost:27017/testdb")
connect("mongodb://mongo:27017/testdb")

app = Flask(__name__)

logger = logging.getLogger(__name__)
load_dotenv()
@app.route('/')
def hello():
    return "Hello, World! Mostafaaaaaaaaa"

if __name__ == '__main__':
    PORT = os.getenv('PORT')
    app.run(debug=True, host='0.0.0.0', port=PORT)
