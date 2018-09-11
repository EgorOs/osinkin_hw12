# Useful notes

### Getting started with Docker

+ [What is Docker](https://www.youtube.com/watch?v=YFl2mCHdv24)
+ [Docker compose](https://www.youtube.com/watch?v=Qw9zlE3t8Ko)
+ [Learn Docker](https://www.youtube.com/watch?v=wCTTHhehJbU)
+ [Installation for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
+ [Postgres](https://hub.docker.com/_/postgres/)

### Commands
Install *docker-compose*:

    sudo apt install docker-compose

Run the container, flag *-d* makes it background process

    sudo docker-compose up -d

Run with *-f* flag to specify the filename

    sudo docker-compose -f docker-compose.yml up -d

Getting info about current containers:

    sudo docker ps

Stopping background Docker process:

    sudo docker-compose stop

