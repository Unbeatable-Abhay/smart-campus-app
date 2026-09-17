function createPetals(count) {
    for (let i = 0; i < count; i++) {
        const petal = document.createElement("div");
        petal.className = "petal";

        const startLeft = Math.random() * 100;
        petal.style.left = startLeft + "vw";

        const duration = 6 + Math.random() * 6;
        petal.style.animationDuration = duration + "s";

        const delay = Math.random() * 10;
        petal.style.animationDelay = delay + "s";

        const size = 8 + Math.random() * 8;
        petal.style.width = size + "px";
        petal.style.height = size + "px";

        document.body.appendChild(petal);
    }
}

createPetals(15);