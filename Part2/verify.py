
import csv
from ClientOPRF import H
from OPRF_var import q

def calculate_oprf_key(password, salt):
    # Hash the password
    hashed_password = H(password)

    salt_int = int(salt)

    # Calculate H(password) ^ salt
    oprf_key = pow(hashed_password, salt_int, 2*q + 1)

    return oprf_key

def verify():
    with open('server.csv', mode='r') as server_file, open('client.csv', mode='r') as client_file:
        server_reader = csv.reader(server_file)
        client_reader = csv.reader(client_file)

        next(server_reader)
        next(client_reader)
        
        for server_row, client_row in zip(server_reader, client_reader):
            server_username, server_salt = server_row
            client_username, client_password, client_oprf_key = client_row
            
            if server_username != client_username:
                print(f"Username mismatch for user {server_username}")
                continue
            
            print(f"Server username: {server_username}, Server salt: {server_salt}")
            print(f"Client username: {client_username}, Client password: {client_password}, Client OPRF key: {client_oprf_key}")
            
            calculated_oprf_key = calculate_oprf_key(client_password, int(server_salt))
            print(f"Calculated OPRF key: {calculated_oprf_key}")
            
            if calculated_oprf_key == client_oprf_key:
                print(f"Verification successful for user {server_username}")
            else:
                print(f"Verification failed for user {server_username}")

if __name__ == "__main__":
    verify()


