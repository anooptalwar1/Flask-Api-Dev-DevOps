# Dockerfile-flask
FROM ubuntu:latest

# Install Packages
RUN apt-get update && apt-get install -y python3 python3-pip

# Set an environment variable with the directory
ENV APP /app

# Create the directory and instruct Docker to operate
RUN mkdir $APP
WORKDIR $APP

# Copy the Python dependencies
COPY requirements.txt ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all the files and folders in the working directory of container from your local file system
COPY . .

# Run the app
#python app.py {DB_USER} {DB_PASSWORD} {DB_HOST} {DB_PORT} {DB_NAME}
CMD [ "python3", "app.py", "root", "Passw0rd", "mysqldb", "3306", "procedure_management_db" ]
