from cryptography.hazmat.primitives.asymmetric import dh, ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from OPRF_var import q
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import csv

app = Flask(__name__)

CORS(app)

r = None
z = None

# Function to hash an integer to an element of the cyclic group G
def string_to_integer(P,q):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(P.encode())
    hashed_value = digest.finalize()
    
    s = int.from_bytes(hashed_value, byteorder='big')
    s %= (q-2)
    s += 2
    return s

def H(P):
    s = string_to_integer(P, q)
    H_P = pow(s, 2, 2*q + 1)
    return H_P

def generate_randome_scalar():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    return private_key.private_numbers().private_value

def initialize(P,q):
    H_P = H(P)
    r = generate_randome_scalar()
    C = pow(H_P, r)
    return C

@app.route('/oprf', methods=['POST'])
def clientOPRF():
    try:
        U = request.json.get('username')
        P = request.json.get('password')
        C = initialize(P, q)
        
        body = {
            'U' : U,
            'C': C
        }
        response = requests.post('http://localhost:5000/oprf', json=body)
        R = response.json().get('R')
        z = pow(z,-1)
        K = pow(R, z)
        with open('client.csv', mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([U, P, K])
        return jsonify({'Message' : 'OPRF worded'}), 200
    except Exception as e:
        return jsonify({'Message' : 'Error in OPRF', 'Error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)


