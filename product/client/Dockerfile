# set base image (host OS)
FROM node:14

# set the working directory in the container
WORKDIR /frontend

# copy files to the working directory
COPY dist ./dist
COPY server.js .
COPY package.json .

# install dependencies
RUN npm install

# command to run on container start
CMD [ "node", "server.js"]
