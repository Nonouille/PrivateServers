from flask import Flask,request,jsonify
import tink
from tink import aead
from tink import secret_key_access
import json

app = Flask(__name__)
port = 3001

aead.register()

with open('tink.json', 'r') as file:
  keyset = json.load(file)
serialized_keyset = json.dumps(keyset)
keyset_handle = tink.json_proto_keyset_format.parse(serialized_keyset, secret_key_access.TOKEN )
primitive = keyset_handle.primitive(aead.Aead)

@app.route('/')
def hello_world():
  return 'Hello World!'

@app.route('/encrypt',methods=['POST'])
def encrypt():
  try:
    # Retrieve hash and user from JSON request
    hash_value = request.json.get('hash')
    user_value = request.json.get('user')
    
    # Check if hash and user are not None and are strings
    if hash_value is None or user_value is None:
        return 'Hash or user is missing in the request', 400
    if not isinstance(hash_value, str) or not isinstance(user_value, str):
        return 'Hash and user must be strings', 400
    # Encode hash and user as bytes
    hash_bytes = hash_value.encode('utf-8')
    user_bytes = user_value.encode('utf-8')
        
    cypher = primitive.encrypt(hash_bytes,user_bytes).hex()
    
    response = {
      'message' : 'Cypher created successfully',
      'cypher': cypher
    }
    
    
    return jsonify(response),200
  
  except Exception as e:
    print(e)
    return 'Error encrypting', 500

@app.route('/decrypt',methods=['POST'])
def decrypt():
  try:
    # Retrieve hash and user from JSON request
    cypher_value = request.json.get('cypher')
    user_value = request.json.get('user')
    
    # Check if hash and user are not None and are strings
    if cypher_value is None or user_value is None:
        return 'Hash or user is missing in the request', 400
    if not isinstance(cypher_value, str) or not isinstance(user_value, str):
        return 'Hash and user must be strings', 400
    # Encode hash and user as bytes
    cypher_bytes = bytes.fromhex(cypher_value)
    user_bytes = user_value.encode('utf-8')
    
    hash = str(primitive.decrypt(cypher_bytes,user_bytes))
    hash = hash.split('\'')[1]
    
    response = {
      'message' : 'Cypher created successfully',
      'hash': hash
    }
    return jsonify(response),200
  
  except Exception as e:
    print(e)
    return str(e), 500

if __name__ == '__main__':
  app.run(port=port)
