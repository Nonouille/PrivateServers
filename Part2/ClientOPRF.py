from cryptography.hazmat.primitives.asymmetric import dh
from gmpy2 import mpz, c_div

parameters = dh.generate_parameters(generator=2, key_size=2048)
numbers = parameters.parameter_numbers()

p = mpz(numbers.p)
q = c_div(p - 1, 2)

print("p :", p)
print("q :", q)