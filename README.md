# Django-HTMX-app

## Prupose

This app is a blog like app where users can create their accounts, update their profile info, and create post by passing urls from flicker


## How to use

- Create a virtual environment
- Run "pip install -r requirements.txt"
- Create a .env file
- Run "python manage.py makemigrations" then "python manage.py migrate" to apply all the migrations needed to your newly  created database
- Generate a secret key the create SECRET_KEY environment variable and set in the generated secret key
- Create a DEBUG environment variable and set it to True
- Run "python manage.py runserver" and go to "http://localhost:8000/" to view the webapp

## Functionalities

### Users can perform the following actions:

- Create an account
- login into your account
- Edit your profile info
- Create new posts
- Edit the posts created by the user
- Like the post made by other users
- Create comments on any post
- Like the comments made by other users
- Reply to comments

## Technologies used

### The technologies used in building this app are:

- Django: The framework for perfectionists with deadlines. It is the main backend of the application used to structure the ORM of the applications
- Postgres: Sql database used when working locally
- Sqlite
- HTMX: For seamless requests and replies to and from the server
- Hyperscript: To add JS like interactivity directly in the HTML without the need of a seperate JS file
- Tailwind CSS: It is a CSS framework that helps create mind blowing frontend designs without the use of an external CSS file
- Alpine js: It is used to add interactivity to the application and trigger popups or dropdowns
- Beautifulsoup: To scrape data from the flicker plateform when creating a post and fill in the required data automatically