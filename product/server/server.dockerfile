# set base image (host OS)
FROM tensorflow/tensorflow:latest-gpu

# set the working directory in the container
WORKDIR /server

# copy files to the working directory
COPY . .

# install missing libraries
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y


# install dependencies
RUN python -m pip install -r requirements.txt

# command to run on container start
CMD [ "python", "controllers.main:app", "--port", "5000", "--host", "0.0.0.0"]
