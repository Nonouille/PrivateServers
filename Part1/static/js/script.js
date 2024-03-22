function login() {
    const form = document.getElementById('login');
    const user = form['username'].value;
    const password = form['password'].value;
  
    const loginCall = async () => {
      const response = await fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user: user,
          password: password
        })
      });
      const data = await response.json();
      console.log(data);

      if (response.ok) {
        alert(data.message);
      } else {
        alert("Error: " + data.message);
      }
    }
    loginCall();
  }
  
  function register() {
    const form = document.getElementById('signup');
    const user = form['username'].value;
    const password = form['password'].value;
  
    const registerCall = async () => {
      const response = await fetch('/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user: user,
          password: password
        })
      });
      const data = await response.json();
      console.log(data);

      if (response.ok) {
        alert(data.message);
      } else {
        alert("Error: " + data.message);
      }
    }
    registerCall();
  }
  
  function toggleForm() {
    var loginForm = document.getElementById("login-form");
    var signupForm = document.getElementById("signup-form");
  
    if (loginForm.style.display === "none") {
      loginForm.style.display = "block";
      signupForm.style.display = "none";
    } else {
      loginForm.style.display = "none";
      signupForm.style.display = "block";
    }
  }