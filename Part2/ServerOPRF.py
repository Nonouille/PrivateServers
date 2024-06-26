
from flask import Flask, request, jsonify
from flask_cors import CORS
from OPRF_var import q
import os, csv
app = Flask(__name__)

CORS(app)

def generate_random_salt():
    salt = int.from_bytes(os.urandom(16), byteorder='big')
    return salt 

@app.route('/oprf', methods=['POST'])
def serverOPRF():
    try:
        s = generate_random_salt()
        U = request.json.get('U')
        C = request.json.get('C')
        print("s : ", s)
        with open('server.csv', mode='a') as file:
                writer = csv.writer(file)
                writer.writerow([U, s])
        print("C : ", C)
        R = pow(C, s,2*q + 1)
        return jsonify({'R': R}), 200
    except Exception as e:
        return jsonify({'Message' : 'Error in Server OPRF', 'Error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5002, debug=True)

