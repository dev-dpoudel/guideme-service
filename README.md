# guideme-service
GuideMe-service provides server protocols for GuideMe. Guide Me is a Yellow pages alike platform where people can enlist thei business, create discussion forums and share thoughts and rating for the listed business.

Following functionality are planned to be included in further version
1) Filter Support
2) Sorting Support
3) Authentication Support
4) File Stream responses
5) IRC Web Sockets

log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
uvicorn.run(app, log_config=log_config)
