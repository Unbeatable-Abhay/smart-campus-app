const logoutBtn = document.getElementById("logout-btn");
const avatarEl = document.getElementById("profile-avatar");
const nameEl = document.getElementById("profile-name");
const emailEl = document.getElementById("profile-email");
const departmentEl = document.getElementById("profile-department");
const roleEl = document.getElementById("profile-role");

if (!getToken()) {
    window.location.href = "login.html";
}

const user = getUser();

if (user) {
    avatarEl.textContent = user.name.charAt(0).toUpperCase();
    nameEl.textContent = user.name;
    emailEl.textContent = user.email;
    departmentEl.textContent = user.department || "N/A";
    roleEl.textContent = user.role.charAt(0).toUpperCase() + user.role.slice(1);
} else {
    nameEl.textContent = "Unable to load profile";
}

logoutBtn.addEventListener("click", function () {
    clearToken();
    clearUser();
    window.location.href = "login.html";
});