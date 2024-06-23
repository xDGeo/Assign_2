## Trivia Game

This is a Django-Based, trivia game that allows 2 players to compete against each other in a quiz game.
As per this implementation, the game features questions about European capitals, but the questions can be easily modified.
Once the players invite/accept the invitation, they are transferred to a room where they go head to head against each other for 9 rounds.
Users have to be registered and logged in to play the game.

## Features

- User registration and login
- Sending and receiving invitations
- Accepting or rejecting invitations
- Game can be quit and rejoined at anytime, keeping the score
- Score tracking in real time
- Page is updated dynamically using AJAX and JavaScript for the front end

## Requirements

- Python 3.10
- Django 5.0.6
- Channels
- Daphne
- ASGIRef
- SQLite3 (for the database)

## Setup

### Clone the Repository
git clone <repository-url>
cd trivia-game

## Create VENV
python -m venv venv
venv\Scripts\activate

## Install the requirements
pip install -r requirements.txt

## Apply the migrations
python manage.py migrate

## Create a superuser
python manage.py createsuperuser

## Run the server
python manage.py runserver

Open the link: "http://127.0.0.1:8000/"

## File Structure

- trivia/: app directory
- admin.py: admin configuration
- apps.py: app configuration
- consumers.py: handles the websocket connections
- forms.py: forms for the registration/login
- models.py: database models
- views.py: handles the http requests
- urls.py: URL routing 
- templates/trivia/: HTML templates 
- static/trivia/: static files 
- styles.css: CSS for page customization and design
- scripts.js: JavaScript for  AJAX and websockets (update the page elements dynamically without refreshing the whole browser)
- tests.py: tests
- manage.py

