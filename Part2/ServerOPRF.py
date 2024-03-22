
from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)

CORS(app)

parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
# Server's secret key (salt s)
private_key = parameters.generate_private_key()
salt = private_key.private_numbers().x

@app.route('/oprf', methods=['POST'])
def serverOPRF():
    # Step 1: Receive the value C from the client 
    C = request.json.get('C')

    # Step 2: Generate a random value s
    print("randome salt s: ", salt)

    # Step 3: Compute the value C^s
    R = pow(C, salt)

    
    # Step 4: Send the value C^s to the client
    return jsonify({'R': R}), 200



if __name__ == '__main__':
    app.run(port=5000, debug=True)

