# Useful notes

### Getting started with Docker

+ [What is Docker](https://www.youtube.com/watch?v=YFl2mCHdv24)
+ [Docker compose](https://www.youtube.com/watch?v=Qw9zlE3t8Ko)
+ [Learn Docker](https://www.youtube.com/watch?v=wCTTHhehJbU)
+ [Installation on Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
+ [Postgres](https://hub.docker.com/_/postgres/)
+ Postgres + Docker [video 1](https://www.youtube.com/watch?v=AVGjN28E760), [video 2](https://www.youtube.com/watch?v=q5J3rtAGGNU), [video 3](https://www.youtube.com/watch?v=A8dErdDMqb0), [video 4](https://www.youtube.com/watch?v=aHbE3pTyG-Q)

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

### Setting up database visualiser
1. Get [Sqlectron](https://sqlectron.github.io/)
2. Configure user data and ports [for example](https://github.com/EgorOs/osinkin_hw12/blob/master/docker-compose.yml#L7):

    ```    
    ports: 
      - "5431:5432"
    environment:
      POSTGRES_USER: "root"
      POSTGRES_PASSWORD: "password"
      POSTGRES_DB: "database"
    ```
3. Run Sqlectron, add new connection
    ![Connection setup](https://raw.githubusercontent.com/EgorOs/osinkin_hw12/master/imgs/connection_setup.png)

4. Connect to database, all tables will be stored in database/tables/public, if you wish to initialize with .sql check out [this section](https://github.com/EgorOs/osinkin_hw12#initialize-with-sql).

### Additional
+ [MySQL workbench](https://linode.com/docs/databases/mysql/install-and-configure-mysql-workbench-on-ubuntu/)
+ [SQL Tutorial](https://www.w3schools.com/sql/)
+ [Basics of SQL (video)](https://www.youtube.com/watch?v=bEtnYWuo2Bw)
+ [DROP TABLE](https://www.w3schools.com/sql/sql_drop_table.asp)

### Known issues

###### [Log-in problem](https://stackoverflow.com/questions/29580798/docker-compose-environment-variables)

    docker-compose rm
    docker-compose up

###### [Initialize with .sql](https://gist.github.com/onjin/2dd3cc52ef79069de1faa2dfd456c945)

    volumes:
      - ./data/01-init.sql:/docker-entrypoint-initdb.d/01-init.sql