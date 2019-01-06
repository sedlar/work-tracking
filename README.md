[![Build Status](https://travis-ci.com/sedlar/work-tracking.svg?branch=master)](https://travis-ci.com/sedlar/work-tracking)

# Backend for work tracking tool

Build

```bash
make build
```

Run
```bash
make up
```

Add user
```bash
docker-compose run --rm work-tracking python /app/wt/app.py add-user --username=username --password=password
```

swagger specification is available on url http://localhost:8080/v1/ui


Run tests
```bash
make test
make test-coverage
```
