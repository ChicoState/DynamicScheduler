### This is just running one command

`docker compose -f docker-compose.test.yml up`

Your output should look something like this:

```sh
❯ docker compose -f docker-compose.test.yml up
[+] Running 2/0
 ✔ Container test-mongo-db   Created                                                                                                      0.0s 
 ✔ Container test-flask-app  Created                                                                                                      0.0s 
Attaching to test-flask-app, test-mongo-db
test-flask-app  | ============================= test session starts ==============================
test-flask-app  | platform linux -- Python 3.10.12, pytest-8.3.4, pluggy-1.5.0
test-flask-app  | rootdir: /app
test-flask-app  | collected 3 items
test-flask-app  | 
test-flask-app  | tests/test_routes.py ...                                                 [100%]
test-flask-app  | 
test-flask-app  | ============================== 3 passed in 0.03s ===============================
```

If it doesn't reach out to Thomas