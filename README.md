# EscapeFromLinux

A small container to test skills of linux adminsys
## installation 

`docker-compose up -d`

## usage

`docker exec -itw /escape docker-escapefromlinux-efl-1 bash`

connect to `http://localhost:8080` and follow the steps ;)

## customization and features

you can modify all files in the `exos` folder : the engine permit 2 or 3 things:
* installation function to prepare task
* verify task
* hint if task is to hard
* todo graph
* [TODO] a timer
 