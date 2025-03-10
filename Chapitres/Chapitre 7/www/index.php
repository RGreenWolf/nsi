<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $password = $_POST["password"];

    $correct_password = "epid1234";

    if ($password == $correct_password) {
        header("Location: generator.php");
        exit();
    } else {
        $error_message = "Mot de passe incorrect.";
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex justify-center items-center min-h-screen">

    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-sm">
        <h2 class="text-2xl font-bold text-center mb-6">Connexion</h2>

        <?php if (isset($error_message)): ?>
            <div class="text-red-500 text-center mb-4"><?= $error_message ?></div>
        <?php endif; ?>

        <form method="POST" action="" class="space-y-4">
            <div>
                <label for="password" class="block text-sm font-semibold">Mot de passe</label>
                <input type="password" name="password" id="password" class="w-full p-2 border rounded-lg" required>
            </div>

            <button type="submit" class="w-full bg-blue-500 text-white p-2 rounded-lg">Se connecter</button>
        </form>
    </div>

</body>
</html>
