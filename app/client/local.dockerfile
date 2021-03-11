# get node base image
FROM node:14 as build

# creare folder for app
RUN mkdir -p /usr/src/client

# set workdir
WORKDIR /usr/src/client

# copy angular project
COPY . /usr/src/client

# install node moudles
RUN npm install
RUN npm install -g @angular/cli@11.2.2

# build angular project
RUN ng build

# Stage 2 - nginx for serving
FROM nginx:1.17.1-alpine

# copy files for nginx setup
COPY nginx.conf /etc/nginx/nginx.conf

# move angular build to nginx file
COPY --from=build /usr/src/client/dist/client /usr/share/nginx/html
