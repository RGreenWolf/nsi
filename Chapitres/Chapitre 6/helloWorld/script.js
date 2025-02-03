const button = document.getElementById("btn");
const input = document.getElementById("annee");
const card = document.getElementById("card");
const resultat = document.getElementById("resultat");

var show = (message) => {
    card.style.display = "block";
    resultat.innerText = message;
}

button.addEventListener("click", () => {
    const anneeActuelle = new Date().getFullYear();
    const annee = input.value;
    if (annee === null || annee === "") {
        show("Veuillez saisir une année");
    } else if (isNaN(annee)) {
        show("Année non valide");
    } else {
        let age = anneeActuelle - annee;
        let message = "Vous avez " + age + " ans. ";
        if (age > 150) {
            message = "Sacré menteur, tu ne t'enrogistre pas sur instagram tu sais !";
        } else if (age < 18) {
            message += "Vous êtes mineur.";
        } else if (age >= 18 && age < 60) {
            message += "Vous êtes adulte.";
        } else if (age >= 60 && age < 80) {
            message += "Vous êtes membre du 3e âge.";
        } else {
            message += "Vous êtes membre du 4e âge.";
        }
        show(message);
    }
})

const print = (message) => {
    console.log(message);
}