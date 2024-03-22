from cryptography.hazmat.primitives.asymmetric import dh
from gmpy2 import mpz, c_div

parameters = dh.generate_parameters(generator=2, key_size=2048)
numbers = parameters.parameter_numbers()

p = mpz(numbers.p)
q = c_div(p - 1, 2)

# print("p :", p)
# print("q :", q)

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Function to hash an integer to an element of the cyclic group G
def string_to_integer(P,q):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(P.encode())
    hashed_value = digest.finalize()
    
    s = int.from_bytes(hashed_value, byteorder='big')
    s %= (q-2)
    s += 2
    return s


print("Hashed value of 'Hello' :", string_to_integer("Hello", q))
