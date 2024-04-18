# User Management REST API

User Management REST API (Python - Back end)

# How To Run Application

Open command prompt and run the below command with exact sequence of information and pass actual values of DB instead of variables without {}

python app.py {DB_USER} {DB_PASSWORD} {DB_HOST} {DB_PORT} {DB_NAME}

Example: python app.py root Passw0rd 127.0.0.1 3306 user_management_db

# How To Test APIs through Postman tool

Import the collection file "WCC User Management.postman_collection.json" in the Postman tool. You'll get all the developed APIs.

Now, you can test all the APIs.

# Docker build 

docker build -t umflask .

# Kubernetes Deployment

kubectl create -f umflask.yaml

# Comments for Docker Images :
Mysql Database should be running with DB_HOST=mysqldb instead of localhost while docker build
Dockerfile has been tested with flask(port=5002) and mysql(port=3306) both running on docker containers and linked together

command used : docker run -it --name=umtestflask -h=umtestflask --link=mysqldb:mysqldb -p 5002:5000 -d umtestflask

