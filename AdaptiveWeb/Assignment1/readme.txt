#Install the following packages:
1.flask-sqlalchemy,
2.flask _migratge
3.flask
4.flask_wtf
5.Wtforms
6.flask-login
7.flask-table
8.python 2.7

#to run the application:
Navigate to the /app folder and run
export  FLASK_APP=main.py
flask run

#To open the application:
http://127.0.0.1:5000/login

#User info:
five users have been created already - aaa, bbb, ccc, ddd, eee
all passwords are 123
For new user registration, user the registration link

#ANY database schema changes : Using flask migrate:
Flask db init (do only once)
Flask db migrate - m ”some commit message”
Flask db upgrade (incorporates schema changes)
FlasK db downgrade ( reverts to previous schema)

#IMPORTANT STEPS TO SEE THE PROJECT

Structure of the project:
Project(A1)
|----app
        |---static
        |	|---css and .js scripts
        |---templates
        |	|---html pages
        |---python scripts
|----aw_extension
        |---manifest.json
        |---js
        |---images
|---migrations (initially not created)
|---app.db (initially not created)
|---config.py
|---main.py


Instructions for using the below project:
Please install the google chrome extension provided with the repository. The extension is compatible on chrome 64 bit windows 10 machine. Please refer the google chrome developers site for instructions to install the extension. For the current repository, the extension is stored under the folder name 'aw_extension'

The system is designed to run on localhost. Navigate to the folder which contains app, aw_extension and other files. Type the below commands in the given order:
1)	flask db init
2)	flask db migrate –m “commit-message”
3)	flask db upgrade
A folder migrations and a database app.db is created upon the successful execution of the above commands.
-Home/Login page: 127.0.0.1:5000. Create three users with login usernames: aaa, bbb, ccc Login password: 123 for all accounts. Login with a user and navigate to /user/<username> page by clicking on ‘Profile’ There is a ‘Logout’ if the user wants to logout. Here on the Profile page there is a link to navigate to stackoverflow page. It is given along with the past 20 recent activities done by the user on the stackoverflow page. User’s, ‘about me’ information as well as a link for interactive social visualization is given. User’s behavior is tracked on the website. A number of tracking features such as, checking if the user votes for an answer, asks a question, shares an answer etc. are done with the use of this project. 
Steps for creating 3 accounts:
Install the required packages and run the three given flask command above. Type in 127.0.0.1:5000 in one of the modern browsers (Google Chrome is advised since the extension is for google chrome). Click on ‘Register’. Enter the details of the new user, you are then redirected to the ‘Login’ page. Here you may log into the system.
