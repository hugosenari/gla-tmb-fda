Gla Tmb Fda
===========

AWS Lambda API for GTFS

Requirements
------------

This project uses [pipenv](https://docs.pipenv.org/) to manage its dependencies, it can be installed
on macOS using [Homebrew](https://brew.sh) by typing `$ brew install pipenv`.

Installation
------------

This project uses [Zappa](https://github.com/Miserlou/Zappa) to deploy to AWS
lambda. Zappa is installed in an isolated environment by running:

    ```
    pipenv install
    ```

Testing
-------

Uses pytest. To run the whole test suite:

    ```
    pipenv run pytest
    ```

Deployment
----------

See [Zappa documentation](https://github.com/Miserlou/Zappa),
you will need to have your AWS credentials setup, and then you can run Zappa inside of your
virtualenv:

    ```
    pipenv run zappa deploy
    ```

Credits
-------

This project has been generated with [Cookiecutter](https://github.com/audreyr/cookiecutter)
using the [Lambda function template](https://github.com/browniebroke/cookiecutter-lambda-function)
