from flask import Flask, request, render_template
from argon2 import PasswordHasher
import time
import os
import requests

port = 3000
app = Flask(__name__)
salt = b'NoSaltPleaseToday'
filePath = 'data/db.json'
database = []
hasher = PasswordHasher(time_cost=75,hash_len=128)

def load_database():
  with open(filePath, 'r+') as file:
    for line in file:
      user, cypher = line.strip().split(':')
      database.append((user, cypher))

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
    return 'User does not exist', 500
  
  # Retrieve the cypher from the database
  cypher = next((x[1] for x in database if x[0] == user), None)
  if cypher is None:
    return 'Cypher not found for user', 500
  
  #Then check if the password is correct
  hash = None
  try:
    if not password:
      return 'Password is undefined', 500
    hash = hasher.hash(password,salt=salt)
    
  except Exception as e:
    print(e)
    return 'Error logging in',e, 500
  
  finally:
    body = {
      'user': user,
      'cypher': cypher
    }
    response = requests.post('http://localhost:3001/decrypt', json=body)
    hashToVerify = response.text
  if hash != hashToVerify:
    return 'Incorrect password', 500
  else:
    return 'Logged in', 200

@app.route('/register', methods=['POST'])
def register():
  #Refresh database
  #load_database()
  #Get the user and password from the request
  user = request.json['user']
  password = request.json['password']
  hash = None
  
  #Check if the user already exists
  if user in [x[0] for x in database]:
    return 'User already exists', 500
  
  try:
    if not password:
      return 'Password is undefined', 500
    #Hash the password
    hash = hasher.hash(password,salt=salt)
    hash = hash.split('p=')[1]
    body = {
      'user': user,
      'hash': hash
    }
    #Encrypt the hash
    response = requests.post('http://localhost:3001/encrypt', json=body)
    body = response.json()
    cypher = body['cypher']
    print("user: ", user, "| hash: ",hash, "| cypher: ", cypher)
    string = user + ':' + cypher + '\n'
    with open(filePath, 'a') as file:
      file.write(string)
    return 'Account Created', 200
  except Exception as e:
    print(e)
    return 'Error creating account',str(e), 500
    

if __name__ == '__main__':
  app.run(port=port)