const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");
const toggleLink = document.getElementById("toggle-link");
const formTitle = document.getElementById("form-title");
const errorBox = document.getElementById("error-box");

let showingLogin = true;

toggleLink.addEventListener("click", function (event) {
    event.preventDefault();

    showingLogin = !showingLogin;

    if (showingLogin) {
        loginForm.style.display = "block";
        registerForm.style.display = "none";
        formTitle.textContent = "Login";
        toggleLink.textContent = "Need an account? Register";
    } else {
        loginForm.style.display = "none";
        registerForm.style.display = "block";
        formTitle.textContent = "Register";
        toggleLink.textContent = "Already have an account? Login";
    }

    errorBox.style.display = "none";
});

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    const result = await apiLogin(email, password);

    if (result.status === 200) {
        setToken(result.data.token);
        setUser(result.data.user);
        window.location.href = "home.html";
    } else {
        errorBox.textContent = result.data.error;
        errorBox.style.display = "block";
    }
});

registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const name = document.getElementById("register-name").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const department = document.getElementById("register-department").value;

    const result = await apiRegister(name, email, password, "student", department);

    if (result.status === 201) {
        const loginResult = await apiLogin(email, password);
        setToken(loginResult.data.token);
        setUser(loginResult.data.user);
        window.location.href = "home.html";
    } else {
        errorBox.textContent = result.data.error;
        errorBox.style.display = "block";
    }
});