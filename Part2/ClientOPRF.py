from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from OPRF_var import q,p
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import csv, random, sys
sys.set_int_max_str_digits(99999999)

app = Flask(__name__)

CORS(app)

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

def generate_random_scalar():
    scalar = random.randint(2, 99999)
    return scalar

def initialize(P,q):
    H_P = H(P)
    r = generate_random_scalar()
    C = pow(H_P, r,p)
    return C,r

@app.route('/oprf', methods=['POST'])
def clientOPRF():
    try:
        U = request.json.get('username')
        P = request.json.get('password')
        C,r = initialize(P, q)
        print("C : ",C)
        body = {
            'U' : U,
            'C': C
        }
        response = requests.post('http://localhost:5000/oprf', json=body)
        R = response.json().get('R')
        print("R : ",R)
        print('Type of r : ',type(r))
        print("Type of p : ",type(p))
        try :
            z = pow(r,-1,p)
            print("z : ",z)
        except Exception as e:
            return jsonify({'Message' : 'Error in computing z', 'Error': str(e)}), 500
        
        try:
            K = pow(R, z,p)
            print("K : ",K)
        except Exception as e:
            return jsonify({'Message' : 'Error in computing K', 'Error': str(e)}), 500
        
        with open('client.csv', mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([U, P, K])
        return jsonify({'Message' : 'OPRF worked'}), 200
    except Exception as e:
        return jsonify({'Message' : 'Error in Client OPRF', 'Error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)


