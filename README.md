# TAKE HOME PROJECT BLANKON TECHNOLOGY SOLUTIONS

First of all, congratulations on reaching this step in the interview series. The take-home project is mainly designed to assess how well you structure your code and how efficiently you build a solution for the given task.

## Requirements for the take home project:
- 🫙 Please utilize Docker for easy setup and testing on our side 🫙 
- 🧪 minimum 80% test coverage 🧪 
- 🐍 The project must be written in Python and utilize Django REST framework🐍
- ❗️ You must use your own third-party credentials, such as a Google API Key or LinkedIn API Key, for your local testing. However, please do not share them in any of these files; we will use our own credentials to test it. ❗️ 

# Simple Backend Todo App
## Create a backend service for a Todo App with the following specifications:
- user can login/signup using Linkedin SSO and Google SSO
- user can login/signup using an email and password combination
- user can list,add,update and delete their todos
- If a user is logged in with the same credentials on two or more browsers, when they add, update, or delete a todo in one browser, it should sync to all browsers via socket (push mechanism)
- Except for login/signup, other APIs and socket connections must be protected.



## When you are done
- 🫸 push your code to this repository, or if you put it in different branch please merge to main branch 🫸
- 🏷️ Go to issues tab, you will have 1 open issue please label that issue to Ready to Review 🏷️ 


## How to run it?
- copy .env.example into .env (fill it based on your data)
- run `docker-compose up --build`
- run `docker ps` to get container id
- run `docker exec -it <container id> bash`
- run  `python manage.py migrate`
- run `python manage.py createsuperuser`, input username and password
- access `http://localhost:8000/admin/`
- click `Social Applications` menu
- add social application for linked in (provider: OpenID Connect, Provider ID: oidc_linkedin, Name: LinkedIn OIDC, Client id: <your client id>, Secret Key: <your secret key>)
- add social application for google (provider: Google, Provider ID: google, Name: Google, Client id: <your client id>, Secret Key: <your secret key>)
- click logout
- access http://localhost:8000/accounts/login/ for login/signup using an email and password combination
- access http://localhost:8000/accounts/google/login/ for  login/signup using Google SSO
- access http://localhost:8000/accounts/oidc/linkedin-server/login/ for login/signup using LinkedIn SSO
- after login, it will redirect to page todo http://localhost:8000/todo/
- you can do create, update, delete and get todo

## test websocket
- open browser and access http://localhost:8000/websocket
- open another browser and access http://localhost:8000/websocket
- input data, example ({"action":"update","data":{"id":"wVJD63p","title":"test10","description":"desc","completed":false}})
- another browser should be synced with the latest data

## Unit Test
- run `docker exec -it <container id> bash`
- run `coverage run --source='.' manage.py test tests/`
- run `coverage report`