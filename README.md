# OC Projet 10 - Créez une API sécurisée RESTful en utilisant Django REST

Ce projet vise à créer une API RESTful *(Application Programming Interface)*
Cette API a pour but de permettre à une équipe de développement d'échanger
sur un projet en cours, faire remonter des problèmes et les commenter.

Cette API a été écrite en utilisant **Django Rest Framework** et **JWT**.
Et pour ce projet nous utiliserons **postman**

**L'API doit permettre les actions suivantes:**

- L'utilisateur doit pouvoir se créer un compte
- L'utilisateur doit pouvoir se connecter *(avec JWT)*
- L'authentification est nécessaire pour acceder à l'API
- Seul le créateur d'un projet peut créer / modifier / supprimer un projet.
- Seul le créateur d'un projet peut ajouter ou supprimer un contributeur sur un projet qu'il a créé
- Les contributeurs n'ont accès qu'en lecture au projet.
- Seul le créateur d'un problème peut le modifier / supprimer
- Les contributeurs peuvent créer des problèmes sur les projets auxquels ils sont associés
- Les problèmes peuvent être commentés

## Installation de l'API:

1. Installez la derniere version de python , disponible ici : https://www.python.org/downloads/


2. Importez le projet depuis git:
`git clone https://github.com/thomas-barbato/projet-10.git`

3. Créez un environnement virutel:
`python3 -m venv /path/to/new/virtual/environment`
 Ou `python -m virtualenv venv`

4. Activez l'environnement virtuel:
1.`cd Venv\Scripts\ ; .\activate.bat ;`
2.`cd .. `
3.`cd .. `

5. Installez les dépendances:
`pip install -r requirements.txt`

6. lancez le serveur:
`python manage.py runserver`

7. Installez postman:
``https://www.postman.com/downloads/``

8. Lancez postman


## Acceder à l'interface admin:

Pour accéder à l'interface d'administration, rendez-vous à l'url suivante:

(assurez vous que le serveur local soit actif)

``http://127.0.0.1:8000/admin``

``Email : admin@test.com``
``Password: Thomas404*``

## Acceder à postman

**Pour pouvoir lancer des requetes à l'API, nous utilisons donc POSTMAN
et maintenant qu'il est lancé, veuillez importer la collection qui se trouve
à cette url :**

``https://github.com/thomas-barbato/projet-10/blob/main/projet-10.postman_collection.json``

**Ensuite:**

1. Cliquez sur "importer"
2. Importer la collection précédemment téléchargée
3. Connectez-vous via l'un des comptes utilisateurs déjà créés (ou créez le vôtre) 
- via la collection: Dossier : User , fichier : login
- via l'url:``http://127.0.0.1:8000/api/login`` 

**Un exemple d'utilisateur déjà créé que vous pouvez utiliser :** 

- email: ``test9@test.com`` , password : ``Thomas404*``

**Une fois connecté :**

l'API vous génèrera un jeton (token) d'identification, **pour vous en servir:**

Copier-coller le contenu de **"access"**, dans la variable d'environnement de postman nommée ``jwt_token``

A partir de maintenant, vous êtes connecté et vous pouvez vous servir de ma collection.



