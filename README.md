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
1. Get [DBeaver](https://dbeaver.io/download/) or [Sqlectron](https://sqlectron.github.io/)
    ```
    # Download .deb package and run
    sudo dpkg -i <filename>.deb 
    ```
2. Configure user data and ports [for example](https://github.com/EgorOs/osinkin_hw12/blob/master/docker-compose.yml#L7):

    ```
    ports: 
      - "5431:5432"
    environment:
      POSTGRES_USER: "root"
      POSTGRES_PASSWORD: "password"
      POSTGRES_DB: "database"
    ```
3. Run DBeaver or Sqlectron, add new connection, accourding to your docker-compose file
    ![Connection setup](https://raw.githubusercontent.com/EgorOs/osinkin_hw12/master/imgs/connection_setup.png)

4. Run the docker container, connect to database, all tables will be stored in tables/public, if you wish to initialize with .sql check out [this section](https://github.com/EgorOs/osinkin_hw12#initialize-with-sql).

### Additional
+ [MySQL workbench](https://linode.com/docs/databases/mysql/install-and-configure-mysql-workbench-on-ubuntu/)
+ [SQL Tutorials](https://www.w3schools.com/sql/)
+ [Basics of SQL (video)](https://www.youtube.com/watch?v=bEtnYWuo2Bw)

### Known issues

###### [Log-in problem](https://stackoverflow.com/questions/29580798/docker-compose-environment-variables)

    docker-compose rm
    docker-compose up

###### [Initialize with .sql](https://gist.github.com/onjin/2dd3cc52ef79069de1faa2dfd456c945)

    volumes:
      - ./data/01-init.sql:/docker-entrypoint-initdb.d/01-init.sql

### Report

In order to reduce processing time the following improvements were made:
+ Parallelized SQL queries in **4_stat_to_join.py**
+ Table insertions in **3_import_csv.py** replaced with [copying](http://initd.org/psycopg/docs/cursor.html#cursor.copy_from).

##### Import optimization


##### 1st attempt [code](https://github.com/EgorOs/osinkin_hw12/blob/master/unoptimized/3_import_csv_v1.py)
Initially data from csv table has been devided into chunks (of 200k records) and inserted into table via *INSERT INTO employee VALUES(200k records)*.

Processing time: 56.86241841316223 sec. 

##### 2nd attempt [code](https://github.com/EgorOs/osinkin_hw12/blob/master/unoptimized/3_import_csv_v2.py)
All the data was [copied](http://initd.org/psycopg/docs/cursor.html#cursor.copy_from) to the temporary table, then fixed and rearranged and the copied into employee table.

Processing time: 74.31883716583252 sec. 

##### 3rd attempt [code](https://github.com/EgorOs/osinkin_hw12/blob/dfbac5781c3a0267b5d5a9c9d5affeb35d6da8e0/3_import_csv.py)
In order to rearrange and prepare the data the temporary csv file is created; after all preparations data is copied straight to the employee table.

Processing time: 30.66781258583069 sec.

#### Queries optimization

In order to speed up queries threading was added, the time comparison is shown in a table below.

 Test    |  1 Thread time, sec  |  5 Threads time, sec  
 ------  |  ------------------  |  -------------------  
 1       |  6.508256435394287   |  8.425762176513672     
 2       |  6.007521867752075   |  8.277645587921143   
 3       |  6.007717370986938   |  8.546740531921387    


