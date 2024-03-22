from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend
from gmpy2 import mpz, c_div

app = Flask(__name__)


parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
numbers = parameters.parameter_numbers()


# Server's secret key (salt s)
private_key = parameters.generate_private_key()
salt = private_key.private_numbers().x

print("number p ", numbers.p)
print("numbers q", numbers.q)


p = mpz(numbers.p)
q = c_div(p - 1, 2)

print("p" , p) 
print("q", q)

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