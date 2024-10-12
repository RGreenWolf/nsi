# Documentation de l'API

## Table des matières

- [Authentification](#authentification)
  - [Inscription](#inscription)
  - [Connexion](#connexion)
  - [Vérification du Token](#vérification-du-token)
- [Gestion des Parties](#gestion-des-parties)
  - [Créer une Partie](#créer-une-partie)
  - [Rejoindre une Partie](#rejoindre-une-partie)
  - [Statut d'une Partie](#statut-dune-partie)
  - [Tester un Nombre](#tester-un-nombre)
  - [Parties Publiques](#parties-publiques)
  - [Partie Aléatoire](#partie-aléatoire)
- [Classement](#classement)
- [Commandes Serveur](#commandes-serveur)

---

## Authentification

### Inscription

- **URL** : `/auth/register`
- **Méthode** : `POST`
- **Description** : Permet d'enregistrer un nouvel utilisateur.
- **Paramètres** :
  - `username` : Nom d'utilisateur (3-20 caractères).
  - `password` : Mot de passe (6-30 caractères).
- **Réponse** :
  - `200 OK` : Utilisateur enregistré avec succès.
  - `400 Bad Request` : Données invalides ou utilisateur déjà existant.

### Connexion

- **URL** : `/auth/login`
- **Méthode** : `POST`
- **Description** : Permet de connecter un utilisateur.
- **Paramètres** :
  - `username` : Nom d'utilisateur.
  - `password` : Mot de passe.
- **Réponse** :
  - `200 OK` : Connexion réussie, retourne un token.
  - `403 Forbidden` : Identifiant ou mot de passe incorrect.

### Vérification du Token

- **URL** : `/auth/check_token`
- **Méthode** : `GET`
- **Description** : Vérifie si un token est valide.
- **Paramètres** :
  - `token` : Token de l'utilisateur.
- **Réponse** :
  - `200 OK` : Token valide.
  - `403 Forbidden` : Token invalide.

---

## Gestion des Parties

### Créer une Partie

- **URL** : `/party/create`
- **Méthode** : `POST`
- **Description** : Crée une nouvelle partie avec un joueur.
- **Paramètres** :
  - `token` : Token de l'utilisateur.
  - `difficulty` : Niveau de difficulté.
  - `public` : Booléen pour une partie publique ou privée.
- **Réponse** :
  - `200 OK` : Partie créée avec succès, retourne l'ID de la partie.
  - `400 Bad Request` : Données invalides.

### Rejoindre une Partie

- **URL** : `/party/join`
- **Méthode** : `POST`
- **Description** : Rejoint une partie existante.
- **Paramètres** :
  - `id` : ID de la partie.
  - `token` : Token de l'utilisateur.
- **Réponse** :
  - `200 OK` : Partie rejointe, retourne l'état de la partie.
  - `404 Not Found` : Partie non trouvée.

### Statut d'une Partie

- **URL** : `/party/status`
- **Méthode** : `GET`
- **Description** : Obtenir le statut actuel de la partie.
- **Paramètres** :
  - `token` : Token de l'utilisateur.
- **Réponse** :
  - `200 OK` : Retourne le statut de la partie.
  - `404 Not Found` : Partie non trouvée.

### Tester un Nombre

- **URL** : `/party/test`
- **Méthode** : `POST`
- **Description** : Tester un nombre dans la partie.
- **Paramètres** :
  - `token` : Token de l'utilisateur.
  - `num` : Nombre à tester.
- **Réponse** :
  - `200 OK` : Réponse du test (trop grand, trop petit ou victoire).
  - `403 Forbidden` : Ce n'est pas le tour du joueur.
  - `404 Not Found` : Partie non trouvée.

### Parties Publiques

- **URL** : `/parties/public`
- **Méthode** : `GET`
- **Description** : Obtenir la liste des parties publiques disponibles.
- **Réponse** :
  - `200 OK` : Retourne la liste des parties publiques.

### Partie Aléatoire

- **URL** : `/party/random`
- **Méthode** : `GET`
- **Description** : Rejoint une partie publique aléatoire.
- **Paramètres** :
  - `token` : Token de l'utilisateur.
- **Réponse** :
  - `200 OK` : Partie trouvée et rejointe.
  - `404 Not Found` : Aucune partie publique disponible.

---

## Classement

### Obtenir le Classement

- **URL** : `/rankings`
- **Méthode** : `GET`
- **Description** : Retourne le classement des joueurs basé sur le nombre de victoires.
- **Paramètres** :
  - `token` : Token de l'utilisateur.
- **Réponse** :
  - `200 OK` : Retourne le classement des 20 meilleurs joueurs ainsi que le rang du joueur connecté.

---

## Commandes Serveur

Les commandes suivantes peuvent être exécutées directement dans le terminal du serveur :

- **`exit`** : Arrête le serveur.
- **`tps`** : Affiche le temps d'exécution moyen.
- **`users`** : Affiche la liste des utilisateurs et leur nombre de victoires.
- **`tokens`** : Affiche la liste des tokens et leurs utilisateurs associés.
- **`parties`** : Affiche la liste des parties et leur statut.
- **`save`** : Sauvegarde manuellement les données des utilisateurs et des tokens.

---

## Sauvegarde Automatique

Les données sont sauvegardées automatiquement toutes les 120 secondes. Les parties sans joueurs actifs sont supprimées toutes les 10 secondes.

