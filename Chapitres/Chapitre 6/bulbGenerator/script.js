const button = document.getElementById("btn");
const img = document.getElementById("img");

var statusLampe = false

button.addEventListener("click", () => {
    if (statusLampe) {
        button.innerText = "éteindre"
        img.src = "./ampoule_off.png"
        statusLampe = false
    } else {
        button.innerText = "allumer"
        img.src = "./ampoule_on.png"
        statusLampe = true
    }
})