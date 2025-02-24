function getRandomInt(max) {
  let randomNum = Math.floor(Math.random() * max+1);
  console.log(randomNum);
  return randomNum;
}

const MAX = 100;
let tries;
let number;
let gameTable = document.querySelector("#gameTable");
let playButton = document.querySelector("#playButton");
let triesE = document.querySelector("#tries");
let winNumber = document.querySelector("#winNumber");

function generateTable() {
  let html = "";
  let cpt = 1;
  let i = 0;
  let size = Math.sqrt(MAX);
  for (i; i < size; i++) {
      html += "<tr>";
      for (let j = 0; j < size; j++) {
          html += "<td id='" + cpt + "' class='tableElement text' onclick='guess(this)'>" + cpt + "</td>";
          cpt++;
      }
      html += "</tr>";
  }
  gameTable.innerHTML = html;
}

function play() {
  tries = 0;
  triesE.innerHTML = 0;
  number = getRandomInt(MAX);
  generateTable();
  playButton.innerHTML = "RESET";
  playButton.setAttribute("onclick", "reset()");
  document.getElementById('winScreen').classList.add('hidden');
  document.getElementById('gameTable').classList.remove('hidden');
}

function reset() {
  gameTable.innerHTML = "";
  playButton.innerHTML = "START A GAME";
  playButton.setAttribute("onclick","play()");
  triesE.textContent = 0;
}

function guess(numCell) {
  tries++;
  cellID = Number(numCell.id);
  if (cellID > number) {
      for (let i = cellID; i<=MAX; i++) {
        document.getElementById(i.toString()).classList.add("wrong");
      }
  } else if (cellID < number) {
      for (let i = cellID; i >= 0; i--) {
        document.getElementById(i.toString()).classList.add("wrong");
      }
  } else {
      win();
  }
  triesE.textContent = tries;
}

function win() {
  reset();
  document.getElementById("winScreen").classList.toggle("hidden");
  winNumber.innerHTML = number;
  document.getElementById('gameTable').classList.add('hidden');
}