# Engineering For Data Science

Welcome ODSC 2018 Attendees!

There is a PDF available to prepare for running this repo on AWS. It's available at this [link](https://mailchi.mp/0d95fe282fdb/getting-started-eng-for-datasci),
although I will ask you to sign up for my mailing list. 

There are videos for launching a Jupyter Notebook Server available on YouTube [here](https://www.youtube.com/playlist?list=PLR3z_fOlGTXK0tq-qG_CMhWqHQHSMBbbv). 

## Run This repo using Docker Compose

You can simply run this entire repo using the tool Docker Compose. From within this directory in bash, run

```
$ docker-compose up -d
```

## Basics

### SSH Key Pair

To work on AWS, you will need to set up an SSH Key Pair. On your local system run

```
$ ssh-keygen
```

**Note:** If you are on Windows, you will need some way to operate a Bash shell. I recommend [Git Bash](https://git-scm.com/downloads).

You will need to add this key to AWS. The default key pair created is `id_rsa` and `id_rsa.pub`. 
You should add the content of `id_rsa.pub` to AWS.

### Create a Security Group
This security group should open ports 22, 8888, 5432, 27017 with a Source of anywhere.

## Launch a Jupyter Notebook Server

1. launch a t2.micro with 30 GB storage on our security
2. get public IP
3. connect over ssh to your new instance

   ```
   $ ssh ubuntu@your-intance-public-ip
   ```
4. install Docker

   ```
   $ curl -sSL https://get.docker.com | sh
   ```
   
5. add the `ubuntu` user to the `docker` group

   ```
   $ sudo usermod -aG docker ubuntu
   ```
   
6. disconnect and reconnect from the instance
7. pull the Jupyter Scipy-Notebook image. More info on these images [here](https://github.com/jupyter/docker-stacks)

   ```
   $ docker pull jupyter/scipy-notebook
   ```
   
8. launch the server as a Docker container

   ```
   $ docker run -d -v `pwd`:/home/jovyan -p 8888:8888 jupyter/scipy-notebook
   ```
   
9. obtain the container id for your jupyter server

   ```
   $ docker ps
   ```
   
10. obtain the token for your Jupyter Notebook Server

   ```
   $ docker exec <yourcontainerid> jupyter notebook list
   ```
   
11. visit the server in your browser at `<yourip>:8888`
12. use your token as the password

## Launch a Postgres Notebook

1. launch a t2.micro with 30 GB storage on our security
2. get public IP
3. connect over ssh to your new instance

   ```
   $ ssh ubuntu@your-intance-public-ip
   ```
   
4. install Docker

   ```
   $ curl -sSL https://get.docker.com | sh
   ```
   
5. add the `ubuntu` user to the `docker` group

   ```
   $ sudo usermod -aG docker ubuntu
   ```
   
6. disconnect and reconnect from the instance
7. clone this repo
8. navigate to `odsc-west-2018/docker/postgres`
9. build a new postgres image

   ```
   $ docker build -t my_postgres .
   ```
   
10. create a volume for data persistence

   ```
   $ docker volume create pgdata
   ```
8. launch the server as a Docker container

   ```
   $ docker run -d -v pgdata:/var/lib/postgresql/data -p 5432:5432 my_postgres
   ```   
