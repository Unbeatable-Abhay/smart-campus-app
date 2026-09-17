const bookingList = document.getElementById("booking-list");
const errorBox = document.getElementById("error-box");


if (!getToken()) {
    window.location.href = "login.html";
}


async function loadBookings() {
    bookingList.innerHTML = "";
    errorBox.style.display = "none";

    const result = await apiGetBookings();

    if (result.status !== 200) {
        errorBox.textContent = result.data.error || "Could not load bookings";
        errorBox.style.display = "block";
        return;
    }

    if (result.data.length === 0) {
        bookingList.innerHTML = "<p style='color: #8a8272; font-size: 13px;'>You have no bookings yet.</p>";
        return;
    }

    for (let i = 0; i < result.data.length; i++) {
        const booking = result.data[i];
        renderBookingCard(booking);
    }
}

function renderBookingCard(booking) {
    const card = document.createElement("div");
    card.className = "card";

    if (booking.status === "approved") {
        card.className = card.className + " status-approved";
    }

    const title = document.createElement("div");
    title.className = "card-title";
    title.textContent = "Resource #" + booking.resource_id;

    const subtitle = document.createElement("div");
    subtitle.className = "card-subtitle";
    subtitle.textContent = booking.start_time + " to " + booking.end_time;

    const statusTag = document.createElement("span");
    statusTag.className = "status-tag";
    if (booking.status === "approved") {
        statusTag.className = statusTag.className + " approved hanko";
    }
    statusTag.textContent = booking.status.toUpperCase();


    card.appendChild(title);
    card.appendChild(subtitle);
    card.appendChild(document.createElement("br"));
    card.appendChild(statusTag);

    if (booking.status === "pending") {
        const cancelBtn = document.createElement("button");
        cancelBtn.textContent = "Cancel booking";
        cancelBtn.style.marginTop = "10px";
        cancelBtn.style.backgroundColor = "#8a8272";
        cancelBtn.addEventListener("click", function () {
            cancelBooking(booking.id);
        });
        card.appendChild(cancelBtn);
    }

    bookingList.appendChild(card);
}

async function cancelBooking(bookingId) {
    const result = await apiUpdateBookingStatus(bookingId, "cancelled");

    if (result.status === 200) {
        loadBookings();
    } else {
        alert(result.data.error);
    }
}

loadBookings();