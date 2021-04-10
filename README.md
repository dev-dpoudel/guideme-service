# guideme-service
GuideMe-service provides server protocols for GuideMe. Guide Me is a Yellow pages alike platform where people can enlist thei business, create discussion forums and share thoughts and rating for the listed business.

Following functionality are planned to be included in further version
1) IRC Web Sockets


Usage Notes:
-------------------------------------------------------
MongoDb is exposed via podman containers, use DockerFile to build contatiner with builah.
Run the server instance with proper configuration file in .env. Be sure to set all required settings i.e. dbname user and password
