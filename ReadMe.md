# Monarch 61 Scheduling System
Monarch 61 scheduling system was designed for a non-profit in the Van Buren area, it's main objective is to improve their event scheduling system. It contains a modern calendar, as well as a list view that provides the members with a better user-experience.

## Table of Contents
- Tech Stack
- Installation 
- Future Work

## Stack
Frontend [Vue, Nuxt, and TailwindCSS]
Backend [ Django ]
Database [ MySql ]

## Installation
Begin by cloning the project.
Create an env file wherever the manage.py is, add an element called
SECRET_KEY and your SENDGRID_KEY.
### Backend
1. Start by creating a Virtual Environment
```
cd backend
pip install pipenv
pipenv shell
```
2. Later install the requirements
```
pip install -r requirements.txt
```
3. Add the database information to the settings. Check the Django documentation on how to do this.
4. Migrate the existing models to the database.
```
python manage.py makemigrations
python manage.py migrate
```
5. Run the program
```
python manage.py runserver
```
### Frontend
1. Start by accessing the frontend
```
cd frontend
```
2. Install the dependencies
```
npm install
```
3. Run the program
```
npm run dev
```
## Future Work
- The app is missing work on the security side of it.
