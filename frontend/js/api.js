const API_BASE_URL = "https://smart-campus-backend-zj1o.onrender.com";

function getToken() {
    return localStorage.getItem("token");
}

function setToken(token) {
    localStorage.setItem("token", token);
}

function clearToken() {
    localStorage.removeItem("token");
}

function getUser() {
    const userString = localStorage.getItem("user");
    if (!userString) {
        return null;
    }
    return JSON.parse(userString);
}

function setUser(user) {
    localStorage.setItem("user", JSON.stringify(user));
}

function clearUser() {
    localStorage.removeItem("user");
}

async function apiRegister(name, email, password, role, department) {
    const response = await fetch(API_BASE_URL + "/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, email: email, password: password, role: role, department: department })
    });
    const data = await response.json();
    return { status: response.status, data: data };
}

async function apiLogin(email, password) {
    const response = await fetch(API_BASE_URL + "/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, password: password })
    });
    const data = await response.json();
    return { status: response.status, data: data };
}

async function apiGetResources(startTime, endTime) {
    let url = API_BASE_URL + "/resources";
    if (startTime && endTime) {
        url = url + "?start_time=" + encodeURIComponent(startTime) + "&end_time=" + encodeURIComponent(endTime);
    }
    const response = await fetch(url, {
        method: "GET",
        headers: { "Authorization": "Bearer " + getToken() }
    });
    const data = await response.json();
    return { status: response.status, data: data };
}

async function apiCreateBooking(resourceId, startTime, endTime) {
    const response = await fetch(API_BASE_URL + "/bookings", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + getToken()
        },
        body: JSON.stringify({ resource_id: resourceId, start_time: startTime, end_time: endTime })
    });
    const data = await response.json();
    return { status: response.status, data: data };
}

async function apiGetBookings() {
    const response = await fetch(API_BASE_URL + "/bookings", {
        method: "GET",
        headers: { "Authorization": "Bearer " + getToken() }
    });
    const data = await response.json();
    return { status: response.status, data: data };
}

async function apiUpdateBookingStatus(bookingId, status) {
    const response = await fetch(API_BASE_URL + "/bookings/" + bookingId, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + getToken()
        },
        body: JSON.stringify({ status: status })
    });
    const data = await response.json();
    return { status: response.status, data: data };
}