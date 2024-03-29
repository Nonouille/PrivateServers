# Applied Cryptography - Final Project

## Part 1: Password Protection

To create the Docker containers, follow these steps:

1. Open a terminal and navigate to the `Part1` directory.
2. Make sure Docker is installed and that Docker deamon is running.
3. Run the following command to build and start the containers:
    ```
    docker-compose up --build
    ```
4. Once the containers are up and running, you can access the main page at `localhost:3000/`.
5. You can register, login and then check your username is appearing next to the encryption of your password's hash in the file of the container `/usr/src/app/data/db.txt`

## Part 2: OPRF

To start the client and server flask API, follow these steps:

1. Open a terminal and navigate to the `Part2` directory.
2. Run the following command to start the client:
    ```
    python ClientOPRF.py
    ```
3. In another terminal run the following command to start the server:
    ```
    python ServerOPRF.py
    ```

### Testing the OPRF Endpoint

To test the OPRF endpoint, you can use a tool like `Postman` or `ThunderClient`:

1. Open your preferred tool and create a new request.
2. Set the request URL to `localhost:3001/oprf`.
3. Set the request type to `POST`
4. In the request body, include the following parameters:
    - `username`: [your username]
    - `password`: [your password]
5. Send the request and observe the response.

Remember to replace `[your username]` and `[your password]` with your actual credentials.

Feel free to explore and modify the code as needed. If you have any questions, please ask us on `arnaud.py@edu.devinci.fr` and `valentin.bertogliati@edu.devinci.fr`.

Happy coding!