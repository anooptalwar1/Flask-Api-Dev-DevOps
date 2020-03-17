# Dockerfile-flask
FROM ubuntu:latest

# Install Packages
RUN apt-get update && apt-get install -y python3 python3-pip

# Set an environment variable with the directory
ENV APP /app

# Create the directory and instruct Docker to operate
RUN mkdir $APP
RUN mkdir /app/uploads
WORKDIR $APP

# Expose the port uWSGI will listen on
EXPOSE 5678

# Copy the Python dependencies
COPY requirements.txt ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5678

# Run the app
CMD [ "python3", "upload.py"]
