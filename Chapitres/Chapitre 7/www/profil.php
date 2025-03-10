<?php
if (isset($_GET['profil'])) {
    $profil_data = base64_decode($_GET['profil']);
    $profil = json_decode($profil_data, true);

    $nom = htmlspecialchars($profil['nom']);
    $prenom = htmlspecialchars($profil['prenom']);
    $date_naissance = htmlspecialchars($profil['date_naissance']);
    $email = htmlspecialchars($profil['email']);
    $bio = htmlspecialchars($profil['bio']);
    $photo = htmlspecialchars($profil['photo']);
    $couleur_preferee = htmlspecialchars($profil['couleur_preferee']);
    $couleur_secondaire = htmlspecialchars($profil['couleur_secondaire']);
    $interets = htmlspecialchars($profil['interets']);
    $discord = htmlspecialchars($profil['discord']);
    $facebook = htmlspecialchars($profil['facebook']);
    $sport = htmlspecialchars($profil['sport']);
    $sexe = htmlspecialchars($profil['sexe']);
} else {
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $nom = htmlspecialchars($_POST["nom"]);
        $prenom = htmlspecialchars($_POST["prenom"]);
        $date_naissance = htmlspecialchars($_POST["date_naissance"]);
        $email = htmlspecialchars($_POST["email"]);
        $bio = htmlspecialchars($_POST["bio"]);
        $photo = htmlspecialchars($_POST["photo"]);
        $couleur_preferee = htmlspecialchars($_POST["couleur_preferee"]);
        $couleur_secondaire = htmlspecialchars($_POST["couleur_secondaire"]);
        $interets = htmlspecialchars($_POST["interets"]);
        $discord = htmlspecialchars($_POST["discord"]);
        $facebook = htmlspecialchars($_POST["facebook"]);
        $sport = htmlspecialchars($_POST["sport"]);
        $sexe = htmlspecialchars($_POST["sexe"]);

        $profil = json_encode([
            'nom' => $nom,
            'prenom' => $prenom,
            'date_naissance' => $date_naissance,
            'email' => $email,
            'bio' => $bio,
            'photo' => $photo,
            'couleur_preferee' => $couleur_preferee,
            'couleur_secondaire' => $couleur_secondaire,
            'interets' => $interets,
            'discord' => $discord,
            'facebook' => $facebook,
            'sport' => $sport,
            'sexe' => $sexe
        ]);
        $profil_base64 = base64_encode($profil);
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profil Généré</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            font-family: 'Arial', sans-serif;
        }

        .card {
            background: linear-gradient(to right, <?php echo isset($couleur_preferee) ? $couleur_preferee : '#ff7e5f'; ?>, <?php echo isset($couleur_secondaire) ? $couleur_secondaire : '#feb47b'; ?>);
        }

        .loader {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 2s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body class="bg-gray-100 flex justify-center items-center min-h-screen">

    <div id="loading" class="loader"></div>

    <div id="content" style="display: none;" class="card rounded-lg shadow-lg w-full max-w-4xl p-8">
        <div class="bg-white p-6 rounded-lg shadow-lg">
            <h2 class="text-2xl font-bold text-center mb-6"><?= isset($prenom) ? $prenom : ''; ?> <?= isset($nom) ? $nom : ''; ?> - Profil</h2>

            <?php if ($photo): ?>
                <div class="flex justify-center mb-6">
                    <img class="rounded-full w-32 h-32 object-cover" src="<?= $photo ?>" alt="Photo de Profil">
                </div>
            <?php else: ?>
                <div class="flex justify-center mb-6">
                    <img class="rounded-full w-32 h-32 object-cover" src="https://via.placeholder.com/150" alt="Photo de Profil">
                </div>
            <?php endif; ?>

            <div class="mb-6">
                <h3 class="text-xl font-semibold mb-2">Informations Personnelles</h3>
                <p><strong>Date de Naissance :</strong> <?= isset($date_naissance) ? $date_naissance : ''; ?></p>
                <p><strong>Email :</strong> <?= isset($email) ? $email : ''; ?></p>
                <p><strong>Sexe : </strong> <?= $sexe ?></p>
            </div>

            <div class="mb-6">
                <h3 class="text-xl font-semibold mb-2">Biographie</h3>
                <p><?= isset($bio) ? $bio : ''; ?></p>
            </div>

            <div class="mb-6">
                <h3 class="text-xl font-semibold mb-2">Centres d'Intérêt</h3>
                <?php
                    $interets_array = isset($interets) ? explode(",", $interets) : [];
                ?>
                <ul class="list-disc pl-5">
                    <?php foreach ($interets_array as $interet): ?>
                        <li><?= trim($interet) ?></li>
                    <?php endforeach; ?>
                </ul>
            </div>

            <div class="mb-6">
                <h3 class="text-xl font-semibold mb-2">Réseaux Sociaux</h3>
                <p><strong>Discord :</strong> <?= isset($discord) ? $discord : ''; ?></p>
                <p><strong>Facebook :</strong> <a href="<?= isset($facebook) ? $facebook : ''; ?>" target="_blank" class="text-blue-500"><?= isset($facebook) ? $facebook : ''; ?></a></p>
            </div>

            <div class="mb-6">
                <h3 class="text-xl font-semibold mb-2">Sport Préféré</h3>
                <p><?= isset($sport) ? ucfirst($sport) : ''; ?></p>
            </div>

            <?php if (isset($profil_base64)): ?>
                <p class="text-center mt-4">
                    <a href="?profil=<?= $profil_base64 ?>" class="text-blue-500">Avoir le lien du profil</a>
                </p>
            <?php endif; ?>
        </div>
    </div>

    <script>
        window.onload = function() {
            document.getElementById("loading").style.display = "none";
            document.getElementById("content").style.display = "block";
        };
    </script>

</body>
</html>
