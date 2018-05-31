## Introduction
interface-lium est une inteface web pour utiliser la transcription et la traduction automatiques, deux modules élaborés par le Laboratoire Informatique de l'Université du Mans (LIUM).

Ce projet a été réalisé par 4 membres :
- Duran Alizée
- Yassine M'Chaar
- Mariia Prostiak
- Maymouna Sy

## Installation :computer:
Ce dépôt utilise le framework Flask, un framework écrit sous Python. Voici la démarche à suivre selon l'OS que vous avez

### Sous Linux
Il faut effectuer ces commandes sur un terminal afin de faire l'installation de Flask :
```
sudo apt-get install python-pip #ou pip seul
sudo pip install flask
```
### Sous Windows
Installer Flask sous Windows nécessite d'abord de télécharger pip à cette [adresse](https://bootstrap.pypa.io/get-pip.py) (si vous ne le possédez pas)

Puis suivre ces instructions :
```
pip install --upgrade pip setuptools #S’il faut mettre à jour pip
pip install virtualenv
cd lien_vers/projet/
virtualenv venv
venv\Scripts\activate #Activer virtualenv
pip install Flask
deactivate #Pour quitter virtualenv une fois fini avec Flask
```
### Sous MacOS
On peut tout à fait effectuer ces instructions :
```
curl -O http://python-distribute.org/distribute_setup.py
python distribute_setup.py
easy_install pip
pip install flask
```
## Lancement
Après avoir installé le dépôt, il faut se rendre sur l'adresse `localhost:5000` pour pouvoir obtenir la page suivante :
![Page d'accueil](/static/img/accueil.jpg?raw=true "Accueil")

## Avancement :
- [x] Prise en compte de la transcription anglaise
- [ ] Insérer le système de suivi de la transcription entre l'audio et le texte 