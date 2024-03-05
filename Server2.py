from flask import Flask
import tink
from tink import aead
from tink import secret_key_access

app = Flask(__name__)
port = 3001

@app.route('/')
def hello_world():
  return 'Hello World!'

@app.route('/register')
def register():
  return '';

if __name__ == '__main__':
  app.run(port=port)
