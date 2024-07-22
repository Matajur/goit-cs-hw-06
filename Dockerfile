# The base container image - Linux with python-3.12 preinstalled
FROM python:3.12

# Environment variable APP_HOME = /web_app
ENV APP_HOME /web_app

# Working directory inside the container
WORKDIR $APP_HOME

# Copy files to the working directory of the container
# First . means all files in the same folder as the Dockerfile
# Second . means the root directory in the container (/app)
COPY . .

# Setting dependencies inside the container
RUN pip install -r requirements.txt

# Port where the application is running inside the container
EXPOSE 3000

# Running an application inside a container
ENTRYPOINT ["python", "main.py"]
