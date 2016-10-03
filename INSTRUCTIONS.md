#Instructions

##Running on Docker's containers

You will need to use docker-compose, that can be installed following this documentation [Docker Installation](https://docs.docker.com/engine/installation/)

    git clone  git@github.com:gustavoalmeida/fullstack-coding-challenge.git
    cd ./fullstack-coding-challenge
    docker-compose up


##Running on localhost

For this project you need to have a little knowledge of Redis and Mongo. Because both servers will have to stay running before to run this app 

To run on localhost you will need Python 2.7+, [Virtualenv](https://virtualenv.pypa.io/en/stable/), [Redis](http://redis.io/topics/quickstart), [MongoDB](https://docs.mongodb.com/manual/administration/install-community/)

To start the project, first you need to ensure that the redis server and the mongoDb is running.

Then clone the project repository

    git clone git@github.com:gustavoalmeida/fullstack-coding-challenge.git
    cd ./fullstack-coding-challenge
    source run.sh






