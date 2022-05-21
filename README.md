# spotcloud

# Create Local Enviroment
command = virtualenv nombreEntorno

# Execute Reqirements
command = pip install -r requeriments.txt

# Run Server
command = python manage.py runserver

# Execute URL for upload data to database
postman method GET = http://127.0.0.1:8000/v1/upload/

this response  {'upload': True} -> Upload full dataset to database
this response  {'upload': False, 'message': 'any message'} -> ocurred error


# Document and Postman Colection
url_documentation = https://documenter.getpostman.com/view/10748947/Uyxoi4WK
