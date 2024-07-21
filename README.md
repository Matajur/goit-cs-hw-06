# Tier 2. Module 1: Computer Systems and Their Fundamentals

## Topic 11 - Basics of computer networks and protocols
## Topic 12 - Socket Programming and real-time communications
## Homework

### Technical task

You need to implement the simplest web application without using a web framework.

### Instructions and requirements for implementation

Create a web application with routing for two html pages: `index.html` and `message.html`. Take the [following files](https://drive.google.com/file/d/19JPeOCRcW8qG90xW4bCl7A2XvqSfmkpG/view?usp=sharing) as a basis.

Also:
* handle static resources during program operation: `style.css`, `logo.png`;
* organize work with the form on the `message.html` page;
* if a `404 Not Found` error occurs, return the `error.html` page.
* your HTTP server must be running on port `3000`.

To work with the form, create a Socket server on port `5000`. The work algorithm should be as follows:
* enter data into the form,
* they get into the web application, which forwards it further for processing using a socket (UDP or TCP protocol of your choice) to the Socket server,
* The Socket server translates the received byte string into a dictionary and stores it in the MongoDb database.

The MongoDB document record format should be as follows:

```python
{
  "date": "2022-10-29 20:20:58.020261",
  "username": "krabaton",
  "message": "First message"
},
{
  "date": "2022-10-29 20:21:11.812177",
  "username": "Krabat",
  "message": "Second message"
}
```

The `"date"` key of each message is the time the message was received: `datetime.now()`. That is, each new message from the web application must be added to the database with the time of receipt.

### Acceptance criteria

1. One `main.py` file was used to create the web application. The HTTP server and the Socket server are running in different processes.
2. A `Dockerfile` is created and the application is launched as a Docker container.
3. Wrote `docker-compose.yaml` with configuration for application and MongoDB.
4. Used Docker Compose to build the environment, `docker-compose up` command to start the environment.
5. With the help of the `voluemes` mechanism, data from the database is saved outside the container.
6. Static resources processed: `style.css`, `logo.png`.
7. If a `404 Not Found` error occurs, the `error.html` page is returned.
8. Work with the form is organized according to the above requirements.
9. The MongoDB document record format meets the above requirements.
