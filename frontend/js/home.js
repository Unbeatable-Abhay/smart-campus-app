const resourceList = document.getElementById("resource-list");
const errorBox = document.getElementById("error-box");
const searchInput = document.getElementById("search-input");

if (!getToken()) {
    window.location.href = "login.html";
}

let allResources = [];

async function loadResources() {
    resourceList.innerHTML = "";
    errorBox.style.display = "none";

    const result = await apiGetResources();

    if (result.status !== 200) {
        errorBox.textContent = result.data.error || "Could not load resources";
        errorBox.style.display = "block";
        return;
    }

    allResources = result.data;
    renderResources(allResources);
}

function renderResources(resourceArray) {
    resourceList.innerHTML = "";

    if (resourceArray.length === 0) {
        resourceList.innerHTML = "<p style='color: #8a8272; font-size: 13px;'>No resources found.</p>";
        return;
    }

    for (let i = 0; i < resourceArray.length; i++) {
        renderResourceCard(resourceArray[i]);
    }
}

function renderResourceCard(resource) {
    const card = document.createElement("div");
    card.className = "card";

    const title = document.createElement("div");
    title.className = "card-title";
    title.textContent = resource.name;

    const subtitle = document.createElement("div");
    subtitle.className = "card-subtitle";
    subtitle.textContent = resource.type + " / " + (resource.department || "N/A") + " / " + (resource.location || "N/A");

    const bookBtn = document.createElement("button");
    bookBtn.textContent = "Book";
    bookBtn.style.marginTop = "10px";

    const bookingForm = document.createElement("div");
    bookingForm.className = "booking-form";

    const startLabel = document.createElement("label");
    startLabel.textContent = "Start time";
    const startInput = document.createElement("input");
    startInput.type = "datetime-local";

    const endLabel = document.createElement("label");
    endLabel.textContent = "End time";
    const endInput = document.createElement("input");
    endInput.type = "datetime-local";

    const confirmBtn = document.createElement("button");
    confirmBtn.textContent = "Confirm booking";

    bookingForm.appendChild(startLabel);
    bookingForm.appendChild(startInput);
    bookingForm.appendChild(endLabel);
    bookingForm.appendChild(endInput);
    bookingForm.appendChild(confirmBtn);

    bookBtn.addEventListener("click", function () {
        bookingForm.classList.toggle("open");
    });

    confirmBtn.addEventListener("click", async function () {
        if (!startInput.value || !endInput.value) {
            alert("Please select both a start and end time.");
            return;
        }

        const result = await apiCreateBooking(resource.id, startInput.value, endInput.value);

        if (result.status === 201) {
            alert("Booking submitted successfully.");
            bookingForm.classList.remove("open");
        } else {
            alert(result.data.error);
        }
    });

    card.appendChild(title);
    card.appendChild(subtitle);
    card.appendChild(bookBtn);
    card.appendChild(bookingForm);

    resourceList.appendChild(card);
}

searchInput.addEventListener("input", function () {
    const query = searchInput.value.toLowerCase();

    const filtered = allResources.filter(function (resource) {
        const name = (resource.name || "").toLowerCase();
        const type = (resource.type || "").toLowerCase();
        const department = (resource.department || "").toLowerCase();

        return name.includes(query) || type.includes(query) || department.includes(query);
    });

    renderResources(filtered);
});

loadResources();