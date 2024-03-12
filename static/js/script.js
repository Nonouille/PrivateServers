function login() {
    const user = document.getElementById('user');
    const password = document.getElementById('password');

    const loginCall = async () => {
        const response = await fetch('http://localhost:3000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user: user.value,
                password: password.value
            })
        });
        const data = await response.json();
        console.log(data);
    }
    loginCall();
}