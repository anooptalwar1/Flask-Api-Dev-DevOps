# MEC Analyzer REST API

MEC Analyzer REST API (Python - Back end, MongoDB - DataBase)

## How To Run Application on Local Machine

Open command prompt and run the below command with exact sequence of information and pass actual values of DB instead of variables without {}

- pip install -r requirements.txt
- python app.py


## How To Test APIs through Postman tool

Import the collection file "mec-analyzer-rest-apis.postman_collection.json" in the Postman tool. You'll get all the developed APIs.

## Mongo DB Base Images
docker pull mongo


## How To Run Application in Kubernetes Pods

### Docker build

- docker build -t speedanalyse --build-arg API_URL=`hostname -I | awk '{print $1}'` .

### Kubernetes Deployment

- kubectl create -f mongoserv.yaml
- kubectl create -f speedanalyse.yaml