const button = document.getElementById("btn");
const img = document.getElementById("img");
const switchB = document.getElementById("switch");
const speedSelector = document.getElementById("speed");

var statusLampe = false;
var discoInterval;

function changeStatus() {
    if (statusLampe) {
        button.innerText = "allumer";
        img.src = "./ampoule_off.png";
        statusLampe = false;
        switchB.checked = false;
        clearInterval(discoInterval);
    } else {
        button.innerText = "éteindre";
        img.src = "./ampoule_on.png";
        statusLampe = true;
        switchB.checked = true;
        startDisco();
    }
}

function startDisco() {
    const speed = parseInt(speedSelector.value);
    discoInterval = setInterval(() => {
        img.style.filter = `hue-rotate(${Math.random() * 360}deg)`;
    }, speed);
}

button.addEventListener("click", () => {
    changeStatus();
});

switchB.addEventListener("change", () => {
    changeStatus();
});

speedSelector.addEventListener("input", () => {
    if (statusLampe) {
        clearInterval(discoInterval);
        startDisco();
    }
});