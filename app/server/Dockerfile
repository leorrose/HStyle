# set base image (host OS)
FROM tensorflow/tensorflow:latest-gpu

# set the working directory in the container
WORKDIR /server

# copy files to the working directory
COPY . server/

# install missing libraries
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get install python3.8 -y

# update pip
RUN python3.8 -m pip install --upgrade pip

# install dependencies
RUN python3.8 -m pip install -r server/requirements.txt

# command to run on container start
CMD [ "python3.8", "-m", "uvicorn", "server.controllers.main:app", "--port", "5000", "--host", "0.0.0.0"]
