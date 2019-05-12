# drunkare-server

The drunkare-server collects data from the smartwatch (drunkare-tizen) and the smartphone (drunkare-android). The server is written in python3. We use django for the web server and also sklearn for machine learning.

1. install requirements
`$ python3 -m pip install -r requirements.txt`

2. run server
`$ python3 manage.py runserver 0:{port}`
