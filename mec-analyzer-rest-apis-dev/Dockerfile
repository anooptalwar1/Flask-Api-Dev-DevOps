# Dockerfile-flask
FROM ubuntu:latest

#Api URL Initialization
ARG API_URL
ENV API_URL=$API_URL

# Install Packages
RUN apt-get update && apt-get install -y python3 python3-pip iputils-ping libjpeg-dev libfreetype6-dev zlib1g-dev libpng-dev

# Set an environment variable with the directory
ENV APP /app

# Create the directory and instruct Docker to operate
RUN mkdir $APP
WORKDIR $APP

# Expose the port uWSGI will listen on
EXPOSE 5210

# Copy the Python dependencies
COPY requirements.txt ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5210

#Configure Backend Api Urls from where FrontEnd can communicate
RUN sed -i "s/API_URL/$API_URL/g" "/app/controllers/database_controller.py"

# Run the app
CMD [ "python3", "./app.py"]
# docker build -t speedanalyse --build-arg API_URL=`hostname -I | awk '{print $1}'` .
