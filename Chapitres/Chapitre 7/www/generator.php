<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Générateur de Profil</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/preline/dist/preline.css">
    <script defer src="https://cdn.jsdelivr.net/npm/preline/dist/preline.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background-color: #f4f4f4;
        }
        .card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
            width: 500px;
            text-align: center;
        }
        .stepper {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .step {
            padding: 10px;
            border-radius: 5px;
            margin: 5px;
            background: #ddd;
            cursor: pointer;
        }
        .step.active {
            background: #007bff;
            color: white;
        }
        .step-content {
            display: none;
        }
        .step-content.active {
            display: block;
        }
        button {
            padding: 10px;
            margin: 5px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .btn-primary {
            background: #007bff;
            color: white;
        }
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        input, textarea, select {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>Générateur de Profil</h2>
        <div class="stepper" id="stepper">
            <div class="step active" data-step="1" onclick="goToStep(1)">Informations Personnelles</div>
            <div class="step" data-step="2" onclick="goToStep(2)">Détails de Contact</div>
            <div class="step" data-step="3" onclick="goToStep(3)">Présentation</div>
            <div class="step" data-step="4" onclick="goToStep(4)">Autres Informations</div>
        </div>
        <form action="profil.php" method="POST" id="profilForm">
            <div class="step-content active" data-step="1">
                <label for="nom">Nom :</label>
                <input type="text" id="nom" name="nom" required>
                <label for="prenom">Prénom :</label>
                <input type="text" id="prenom" name="prenom" required>
                <label for="sexe">Sexe :</label>
                <select id="sexe" name="sexe" required>
                    <option value="femme">Femme</option>
                    <option value="homme">Homme</option>
                </select>
                <button type="button" class="btn-primary" onclick="nextStep(1)">Suivant</button>
            </div>
            <div class="step-content" data-step="2">
                <label for="date_naissance">Date de Naissance :</label>
                <input type="date" id="date_naissance" name="date_naissance" required>
                <label for="email">Email :</label>
                <input type="email" id="email" name="email" required>
                <button type="button" class="btn-secondary" onclick="prevStep()">Précédent</button>
                <button type="button" class="btn-primary" onclick="nextStep(2)">Suivant</button>
            </div>
            <div class="step-content" data-step="3">
                <label for="bio">Biographie :</label>
                <textarea id="bio" name="bio" rows="4"></textarea>
                <label for="photo">Photo de Profil (URL) :</label>
                <input type="url" id="photo" name="photo">
                <button type="button" class="btn-secondary" onclick="prevStep()">Précédent</button>
                <button type="button" class="btn-primary" onclick="nextStep(3)">Suivant</button>
            </div>
            <div class="step-content" data-step="4">
                <label for="couleur_preferee">Couleur préférée :</label>
                <input type="color" id="couleur_preferee" name="couleur_preferee">
                <label for="couleur_secondaire">Couleur secondaire :</label>
                <input type="color" id="couleur_secondaire" name="couleur_secondaire">
                <label for="interets">Centres d'intérêt :</label>
                <input type="text" id="interets" name="interets" placeholder="Séparés par des virgules">
                <label for="discord">Discord :</label>
                <input type="text" id="discord" name="discord" placeholder="Ex: utilisateur#1234">
                <label for="facebook">Facebook :</label>
                <input type="url" id="facebook" name="facebook" placeholder="Lien vers votre profil">
                <label for="sport">Sport préféré :</label>
                <select id="sport" name="sport">
                    <option value="football">Football</option>
                    <option value="basketball">Basketball</option>
                    <option value="tennis">Tennis</option>
                    <option value="natation">Natation</option>
                    <option value="rugby">Rugby</option>
                    <option value="cyclisme">Cyclisme</option>
                    <option value="athletisme">Athlétisme</option>
                    <option value="autre">Autre</option>
                </select>
                <button type="button" class="btn-secondary" onclick="prevStep()">Précédent</button>
                <input type="submit" class="btn-primary" value="Générer le Profil">
            </div>
        </form>
    </div>

    <script>
        let currentStep = 1;

        function showStep(step) {
            document.querySelectorAll('.step-content').forEach(el => el.classList.remove('active'));
            document.querySelector(`.step-content[data-step="${step}"]`).classList.add('active');
            document.querySelectorAll('.step').forEach(el => el.classList.remove('active'));
            document.querySelector(`.step[data-step="${step}"]`).classList.add('active');
        }

        function validateStep(step) {
            let inputs = document.querySelectorAll(`.step-content[data-step="${step}"] input[required]`);
            for (let input of inputs) {
                if (!input.value) {
                    alert("Veuillez remplir tous les champs requis avant de continuer.");
                    return false;
                }
            }
            return true;
        }

        function nextStep(step) {
            if (validateStep(step)) {
                if (currentStep < 4) {
                    currentStep++;
                    showStep(currentStep);
                }
            }
        }

        function prevStep() {
            if (currentStep > 1) {
                currentStep--;
                showStep(currentStep);
            }
        }

        function goToStep(step) {
            if (step <= currentStep) {
                showStep(step);
                currentStep = step;
            }
        }

        document.addEventListener("DOMContentLoaded", () => showStep(currentStep));
    </script>
</body>
</html>
