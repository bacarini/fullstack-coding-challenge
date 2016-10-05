#Instructions

##Running on Docker's containers

You will need to use docker-compose, that can be installed following 
this documentation [Docker Installation](https://docs.docker.com/engine/installation/)

    git clone  git@github.com:gustavoalmeida/fullstack-coding-challenge.git
    cd ./fullstack-coding-challenge
    docker-compose up


##Running on localhost

For this project you need to have a little knowledge of Redis and Mongo. 
Because both servers will have to stay running before to run this app 

To run on localhost you will need Python 2.7+, 
[Virtualenv](https://virtualenv.pypa.io/en/stable/), 
[Redis](http://redis.io/topics/quickstart), 
[MongoDB](https://docs.mongodb.com/manual/administration/install-community/)

To start the project, first you need to ensure that the redis server and the mongoDb is running.

We created a autorun that will to configure your unbabel api credentials, 
install requirements of environment and start Flask App, Celery Beat and Flower Monitor
This will configure also your Unbabel Sandbox credentials in ~/.unbabel file

So clone the project repository and run run_app.sh file

    git clone git@github.com:gustavoalmeida/fullstack-coding-challenge.git
    cd ./fullstack-coding-challenge
    source run_app.sh

##Celery

We use [Celery](http://www.celeryproject.org/) to work with our asynchronous task queue/job.
It's very easy to use. And do the job very well.

####To run celery

    git clone git@github.com:gustavoalmeida/fullstack-coding-challenge.git
    cd ./fullstack-coding-challenge
    source run_celery.sh


##Flower Monitor

[Flower](http://flower.readthedocs.io/en/latest/) is a very nice monitor 
for to see what is happening with celery workers.

####To run flower

    git clone git@github.com:gustavoalmeida/fullstack-coding-challenge.git
    cd ./fullstack-coding-challenge
    source run_celery.sh

To access Flower Monitor, put your prowser on http://127.0.0.1:5555/


## Testing

Run the tests by using this code
Make sure that you have configured your Unbabel credentials at ~/.unbabel. 
If you have not done that, please first use run_app.sh before this.

    git clone git@github.com:gustavoalmeida/fullstack-coding-challenge.git
    cd ./fullstack-coding-challenge/hackernews/hackernewsclone
    virtualenv .venv
    source ./venv/bin/activate
    pip install -r requirements.txt
    pytest
    


## To Do

1. Put translations in separate collection
2. Improve performance for comments and translations
3. Show nested comments







