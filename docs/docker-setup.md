So you want a dev environment?

### Setup

1. Install Docker
2. Clone the repo
3. Run the following commands
`docker compose up`
4. Your docker is now running (in the background)!
- This is the first iteration so the server is hosted at http://localhost:80 or http://127.0.0.1:80.
(If you can't connect. Something has gone wrong!)
- This should be fine if you want to test out the server. But if for some reason you want to connect to it...

### Interactive Shell
- `docker container ps`
- You want to grab the relevant container id
- `docker run -it YOUR-CONTAINER-ID /bin/bash