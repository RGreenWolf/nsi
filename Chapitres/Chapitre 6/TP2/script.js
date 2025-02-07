//Retourne un nombre aléatoire dans la limite du max
function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max)) + 1;
}



const MAX = 100; //nombre max de possibilités
let essais;
let numMystere; //Nombre mystère

function play() {

  let table = document.getElementById("tableau");
  essais = 0;
  // Génére le nombre aléatoire
  numMystere = getRandomInt(MAX);

  // L'affiche en console pour tester
  console.log(numMystere);

  //Génération du tableau à compélter
  

}

//Quand le joueur clique sur une case
function tentative(numCell) {

}
