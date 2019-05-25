# drunkare-server

The drunkare-server collects data from the smartwatch (drunkare-tizen) and the smartphone (drunkare-android). The server is written in python3. We use django for the web server and also sklearn for machine learning.

1. install requirements (virtualenv recommended)
`$ python3 -m pip install -r requirements.txt`

2. migrate sqlite3 DB schema via django migrations
`$ python3 manage.py makemigrations`
`$ python3 manage.py migrate`

3. initialize DB with prewritten scripts via django shell
`$ . db_init.sh`

4. run server
`$ python3 manage.py runserver 0:{port}`

(+) for accessing django admin page,
`$ python3 manage.py createsuperuser`
now login at localhost:{port}/admin
