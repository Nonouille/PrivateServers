from cryptography.hazmat.primitives.asymmetric import dh, ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from OPRF_var import q
from flask import Flask, request, jsonify
from flask_cors import CORS

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

def generate_randome_scalar():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    return private_key.private_numbers().private_value

def initialize(P,q):
    H_P = H(P)
    r = generate_randome_scalar()
    C = pow(H_P, r)
    return C

if __name__ == '__main__':
    app.run(port=5001, debug=True)


