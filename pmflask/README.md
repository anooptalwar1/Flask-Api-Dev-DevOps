# Procedure Management REST API

Procedure Management REST API (Python)

# How To Run Application

Open command prompt and run the below command with exact sequence of information and pass actual values of DB instead of variables without {}

python app.py {DB_USER} {DB_PASSWORD} {DB_HOST} {DB_PORT} {DB_NAME}

Example: python app.py root Passw0rd 127.0.0.1 3306 procedure_management_db

# How To Test APIs through Postman tool

Import the collection file "WCC Procedure Management.postman_collection.json" in the Postman tool. You'll get all the developed APIs.

Now, you can test all the APIs.

# Docker build

docker build -t pmflask .

# Deployment Kubernetes

kubectl create -f pmflask.yaml