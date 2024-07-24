# Sample FS App Boilerplate
## Development setup

Requirements:

-   Docker

Requirements (dev):

-   Python 3.10+
-   Poetry
-   npm

Project is using Makefile to simplify the process. Every shell command starts with `make` prefix and should be run from main project directory.

Installation:

-   `make init` 
- replace params in `.env` with your own values
-   `make build`
-   to set up Python env for IDE to work properly, run `poetry install` from main directory

Running project:

-  `make it_run` [Vite will probably complain about http proxy error as it tries to connect to backend before it's up, just refresh the page after backend is up]

You can run backend and frontend on separate tabs in terminal.
-  `make backend_up`
    `make frontend_up`

Running tests:

-   `make test`

## API Documentation

Running project exposes Swagger interface at http://localhost:8008/docs





