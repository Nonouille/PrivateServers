from flask import Flask, request, render_template,jsonify
from flask_cors import CORS
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import requests
import json

port = 3000
app = Flask(__name__)
CORS(app)
#Not needed for random salt : salt = b'NoSaltPleaseToday'
filePath = 'data/db.json'
database = []
hasher = PasswordHasher(time_cost=30,hash_len=128)

def load_database():
  with open(filePath, 'r+') as file:
    for line in file:
      parts = line.split(':')
      database.append(parts)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
  #Refresh database
  load_database()
  #Get the user and password from the request
  user = request.json['user']
  password = request.json['password']
  
  #First check if the user exists
  if user not in [x[0] for x in database]:
    return jsonify({"message" :'User does not exist' }), 500
  
  # Retrieve the cypher from the database
  cypher = next((x[1] for x in database if x[0] == user), None)
  if cypher is None:
    return jsonify({'message' : 'Cypher not found for user' }), 500
  
  #Then check if the password is correct
  try:
    if not password:
      return jsonify({'message' : 'Password is undefined'}), 500
    
    #no need to hash the password, since .verify does it for us

    body = {
      'user': user,
      'cypher': cypher
    }
    response = requests.post('http://Server2:3001/decrypt', json=body)
    hashToVerify = response.json().get('hash')
    
    # Verify the password against the decrypted hash
    hasher.verify(hashToVerify, password)
        
    # hasher.verify throws an exception if verification fails
    return jsonify({'message': 'Logged in'}), 200
  
  except VerifyMismatchError:
    return jsonify({'message': 'Incorrect password'}), 500
    
  except Exception as e:
        return jsonify({'message': 'Error logging in', 'Error': str(e)}), 500
  
  

@app.route('/register', methods=['POST'])
def register():
  #Refresh database
  load_database()
  #Get the user and password from the request
  user = request.json['user']
  password = request.json['password']
  hash = None
  
  #Check if the user already exists
  if user in [x[0] for x in database]:
    return jsonify({'message':'User already exists'}), 500
  
  try:
    if not password:
      return jsonify({'message' : 'Password is undefined'}), 500
    #Hash the password
    hash = hasher.hash(password) #remove salt parameter to use random salt of argon2
    body = {
      'user': user,
      'hash': hash
    }
    #Encrypt the hash
    response = requests.post('http://Server2:3001/encrypt', json=body)
    body = response.json()
    cypher = body['cypher']
    string = f'{user}:{cypher}\n'
    with open(filePath, 'a') as file:
      file.write(string)
    return jsonify({'message' : 'Account Created', 'Using hash': hash}), 200
 
  except Exception as e:
    print(e)
    return jsonify({'message' :'Error creating account', 'Error' : str(e) }), 500
    

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port)
