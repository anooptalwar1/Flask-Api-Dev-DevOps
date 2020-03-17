# Dockerfile-flask
FROM ubuntu:latest

# Install Packages
RUN apt-get update && apt-get install -y python3 python3-pip

# Set an environment variable with the directory
ENV APP /app

# Create the directory and instruct Docker to operate
RUN mkdir $APP
WORKDIR $APP

# Expose the port uWSGI will listen on
EXPOSE 5000

# Copy the Python dependencies
COPY requirements.txt ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Run the app
#python app.py {DB_USER} {DB_PASSWORD} {DB_HOST} {DB_PORT} {DB_NAME}
CMD [ "python3", "./app.py", "root", "Passw0rd", "mysqldb", "3306", "user_management_db" ]
