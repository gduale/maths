# Les petits génies

Application Django et Tailwind CSS pour pratiquer deux catégories : addition et soustraction, multiplication et division, tables de 2 à 9. Chaque nouvelle série mélange aléatoirement cinq questions de chaque opération.

## Démarrer

```sh
uv venv --python 3.14 .venv
uv pip install --python .venv/bin/python -r requirements.txt
./start-dev.sh
```

Pour les démarrages suivants, lance simplement `./start-dev.sh`. Le script applique les migrations puis démarre le serveur sur localhost avec rechargement automatique. Arrête-le avec Ctrl+C.

Ouvrir http://127.0.0.1:8000 et se connecter avec un compte Django actif, puis créer un profil et choisir une catégorie et une table. Toutes les pages de l’application nécessitent une connexion, y compris les accès directs aux exercices et à l’historique.

Pour créer le premier compte administrateur :

```sh
.venv/bin/python manage.py createsuperuser
```

Les autres comptes peuvent être créés dans `/admin/` (Utilisateurs). Un compte actif ordinaire suffit pour utiliser l’application. Aucun envoi d’e-mail, inscription publique ou formulaire de réinitialisation de mot de passe n’est proposé.

Les profils restent liés au navigateur par sa session ; utiliser le même navigateur pour les retrouver. Ils ne sont pas synchronisés entre appareils.

Dix calculs distincts par session, correction côté serveur et protection contre les doubles validations. Le chronométrage commence à la création de la série et se termine à la dixième réponse (pauses comprises). Les durées sont uniquement visibles dans l’historique.
Les additions et soustractions travaillent les déplacements de la table choisie ; les divisions sont exactes, sans zéro au diviseur. Les trous sont répartis aléatoirement entre le premier terme, le deuxième terme et le résultat, avec trois ou quatre questions par position dans chaque série.

## Styles

```sh
pnpm install
pnpm run build:css
```

Le CSS compilé est versionné et fonctionne sans service externe.

## Vérification

```sh
.venv/bin/python manage.py test
```

La configuration fournie est destinée au développement local. Pour une mise en ligne, configurer une clé secrète privée, DEBUG=False, les hôtes autorisés et HTTPS.
