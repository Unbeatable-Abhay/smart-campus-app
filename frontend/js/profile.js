const logoutBtn = document.getElementById("logout-btn");
const nameEl = document.getElementById("profile-name");
const emailEl = document.getElementById("profile-email");
const departmentEl = document.getElementById("profile-department");
const roleEl = document.getElementById("profile-role");

if (!getToken()) {
    window.location.href = "login.html";
}

const user = getUser();

if (user) {
    nameEl.textContent = user.name;
    emailEl.textContent = user.email;
    departmentEl.textContent = "Department: " + (user.department || "N/A");
    roleEl.textContent = "Role: " + user.role;
} else {
    nameEl.textContent = "Unable to load profile";
}

logoutBtn.addEventListener("click", function () {
    clearToken();
    clearUser();
    window.location.href = "login.html";
});