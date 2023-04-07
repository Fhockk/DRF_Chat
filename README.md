## About
- This application was created as a result of a test task
- The purpose of the application is to build a simple chat using Python and DRF

## Technical Requirements
- Use PEP8 for your Python code
- Python 3
- Django
- DRF
- JWT-Auth

## First:
```shell
git clone https://github.com/Fhockk/DRF_Chat.git
```

## How to run this project?
- Make sure you have python installed
- Open the terminal and hit the following command -

```shell
mkvirtualenv --python=python3.10 <virtualenv_name>
```
Change the directory:
```shell
cd DRF_Chat/
```
Install the requirements
```shell
pip install -r requirements.txt
```

## Run the server
```shell
python manage.py runserver
```

And then open browser, go to [127.0.0.1:8000/api/token/](http://127.0.0.1:8000/api/token/)

First, you need to login:


user1 = {
"username":"first"
"password":"password123"
}


user2 = {
"username":"second"
"password":"password123"
}

- (GET)Endpoint which show all threads to this User [http://127.0.0.1:8000/api/threads/](http://127.0.0.1:8000/api/threads/)
- (POST)Endpoint which allow to create thread [http://127.0.0.1:8000/api/threads/](http://127.0.0.1:8000/api/threads/)

"participants": [(first_id), (second_id)]

### ALL endpoints see in the chat.urls.py